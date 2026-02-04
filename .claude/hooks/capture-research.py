#!/usr/bin/env python3
"""
Claude Code SubagentStop Hook: Capture deep-research agent findings.

This hook runs when any subagent finishes but only captures deep-research
(web-research) agents, exporting findings to the Obsidian vault.

Output structure (folder per output):
  research/{timestamp}-{slug}/
    ├── findings.md   (main output + top sources)
    └── sources.md    (full source list)

Features:
- Only captures web-research agents (filters out Explore, Bash, Plan)
- Creates research folder with findings.md and sources.md
- Parses agent's own source ranking (High/Medium/Low) if present
- Falls back to domain-based ranking when agent doesn't provide structured sources
- Links to session in frontmatter
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


# ============================================================================
# Configuration (hardcoded for dev environment)
# ============================================================================

KH_DIR = Path("/home/berkaygkv/Dev/headquarter/kh")
RESEARCH_DIR = KH_DIR / "vault" / "research"
PROCESSED_AGENTS_FILE = Path("/tmp/claude-processed-agents.json")

# How many high-relevance sources to include inline in findings
MAX_INLINE_SOURCES = 5


def extract_target_id(initial_prompt: str) -> str | None:
    """Extract TARGET ID from agent's initial prompt if present."""
    match = re.search(r'TARGET-(\d{8}-\d{6})', initial_prompt)
    return f"TARGET-{match.group(1)}" if match else None

# Domain authority tiers for fallback ranking
HIGH_AUTHORITY_DOMAINS = {
    "docs.anthropic.com", "code.claude.com", "anthropic.com",
    "docs.python.org", "developer.mozilla.org", "docs.github.com",
    "react.dev", "nextjs.org", "vuejs.org", "angular.io",
    "kubernetes.io", "docs.docker.com", "aws.amazon.com",
    "cloud.google.com", "learn.microsoft.com",
}
MEDIUM_AUTHORITY_DOMAINS = {
    "github.com", "stackoverflow.com", "stackexchange.com",
    "medium.com", "dev.to", "hackernews.com", "reddit.com",
    "pypi.org", "npmjs.com", "crates.io",
}


def load_processed_agents() -> set[str]:
    """Load set of already-processed agent IDs."""
    if PROCESSED_AGENTS_FILE.exists():
        try:
            with open(PROCESSED_AGENTS_FILE, "r") as f:
                data = json.load(f)
                return set(data.get("processed", []))
        except (json.JSONDecodeError, IOError):
            pass
    return set()


def save_processed_agents(processed: set[str]) -> None:
    """Save set of processed agent IDs."""
    with open(PROCESSED_AGENTS_FILE, "w") as f:
        json.dump({"processed": list(processed), "updated": datetime.now().isoformat()}, f)


def find_new_agent(subagents_dir: Path, processed: set[str]) -> Path | None:
    """Find the newest agent file that hasn't been processed yet."""
    if not subagents_dir.exists():
        return None

    agent_files = list(subagents_dir.glob("agent-*.jsonl"))
    unprocessed = [f for f in agent_files if f.stem not in processed]

    if not unprocessed:
        return None

    return max(unprocessed, key=lambda f: f.stat().st_mtime)


def get_domain_tier(url: str) -> str:
    """Get authority tier for a URL based on domain."""
    try:
        domain = urlparse(url).netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]

        if domain in HIGH_AUTHORITY_DOMAINS:
            return "high"
        if domain in MEDIUM_AUTHORITY_DOMAINS:
            return "medium"

        for high_domain in HIGH_AUTHORITY_DOMAINS:
            if domain.endswith("." + high_domain):
                return "high"
        for med_domain in MEDIUM_AUTHORITY_DOMAINS:
            if domain.endswith("." + med_domain):
                return "medium"

        return "low"
    except Exception:
        return "low"


def extract_ranked_sources_from_summary(summary: str) -> dict[str, list] | None:
    """Extract sources from agent's own ranking sections in the summary."""
    if not summary:
        return None

    ranked = {"high": [], "medium": [], "low": []}
    found_any = False

    # Pattern to find section headers
    section_pattern = r'(?:^|\n)(?:#{2,4}\s*|\*\*)(High|Medium|Low)(?:\*\*)?[:\s]*\n(.*?)(?=(?:\n(?:#{2,4}\s*|\*\*)(High|Medium|Low)|\n#{1,2}\s+[^#]|\Z))'
    matches = re.findall(section_pattern, summary, re.IGNORECASE | re.DOTALL)

    for match in matches:
        tier = match[0].lower()
        content = match[1]

        if tier not in ranked:
            continue

        link_pattern = r'\[([^\]]+)\]\((https?://[^\)]+)\)'
        links = re.findall(link_pattern, content)

        for title, url in links:
            ranked[tier].append({"title": title.strip(), "url": url})
            found_any = True

    if found_any:
        return ranked

    # Alternative: look for Sources section
    sources_section = re.search(
        r'(?:^|\n)#{1,3}\s*Sources?\s*\n(.*?)(?=\n#{1,2}\s+[^#]|\Z)',
        summary, re.IGNORECASE | re.DOTALL
    )

    if sources_section:
        section_content = sources_section.group(1)
        for tier in ["high", "medium", "low"]:
            tier_pattern = rf'(?:^|\n)(?:#{2,4}\s*|\*\*|-)?\s*{tier}[:\s]*(?:\*\*)?\n?(.*?)(?=(?:\n(?:#{2,4}\s*|\*\*|-)?\s*(?:high|medium|low)|\Z))'
            tier_match = re.search(tier_pattern, section_content, re.IGNORECASE | re.DOTALL)
            if tier_match:
                links = re.findall(r'\[([^\]]+)\]\((https?://[^\)]+)\)', tier_match.group(1))
                for title, url in links:
                    ranked[tier].append({"title": title.strip(), "url": url})
                    found_any = True

    return ranked if found_any else None


def extract_sources_from_text(text: str) -> list[dict]:
    """Extract all markdown links from text."""
    sources = []
    seen = set()
    for match in re.finditer(r'\[([^\]]+)\]\((https?://[^\)]+)\)', text):
        title, url = match.groups()
        if url not in seen:
            seen.add(url)
            sources.append({"title": title.strip(), "url": url})
    return sources


def rank_sources_by_domain(sources: list[dict]) -> dict[str, list]:
    """Rank sources by domain authority."""
    ranked = {"high": [], "medium": [], "low": []}
    for source in sources:
        tier = get_domain_tier(source.get("url", ""))
        ranked[tier].append(source)
    return ranked


def parse_agent_transcript(agent_file: Path) -> dict[str, Any]:
    """Parse agent JSONL transcript and extract key information."""
    entries = []
    tool_calls = []

    with open(agent_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entry = json.loads(line)
                    entries.append(entry)

                    if entry.get("type") == "assistant":
                        for block in entry.get("message", {}).get("content", []):
                            if isinstance(block, dict) and block.get("type") == "tool_use":
                                tool_calls.append({
                                    "tool": block.get("name"),
                                    "input": block.get("input", {})
                                })
                except json.JSONDecodeError:
                    continue

    # Extract initial prompt
    initial_prompt = ""
    for entry in entries:
        if entry.get("type") in ("human", "user"):
            content = entry.get("message", {}).get("content", "")
            if isinstance(content, str):
                initial_prompt = content
            elif isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        initial_prompt = block.get("text", "")
                        break
            break

    # Extract final summary
    final_summary = ""
    for entry in reversed(entries):
        if entry.get("type") == "assistant":
            content = entry.get("message", {}).get("content", [])
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        final_summary = block.get("text", "")
                        break
            elif isinstance(content, str):
                final_summary = content
            if final_summary:
                break

    # Detect agent type
    agent_type = "unknown"
    tool_names = [tc["tool"] for tc in tool_calls]
    if any(t in ["WebSearch", "WebFetch"] for t in tool_names):
        agent_type = "web-research"
    elif any(t in ["Glob", "Grep", "Read"] for t in tool_names):
        agent_type = "explore"
    elif "Bash" in tool_names:
        agent_type = "bash"

    return {
        "initial_prompt": initial_prompt,
        "final_summary": final_summary,
        "agent_type": agent_type,
        "tool_count": len(tool_calls)
    }


def generate_slug(text: str, max_len: int = 40) -> str:
    """Generate a URL-friendly slug from text."""
    # Take first meaningful words
    text = re.sub(r'^(Research|Investigate|Look into|Find out about)\s+', '', text, flags=re.IGNORECASE)
    # Remove special chars, lowercase
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', text.lower())
    slug = re.sub(r'\s+', '-', slug.strip())
    # Truncate at word boundary
    if len(slug) > max_len:
        slug = slug[:max_len].rsplit('-', 1)[0]
    return slug or "research"


def format_findings_markdown(
    parsed: dict[str, Any],
    ranked_sources: dict[str, list],
    output_folder: str,
    target_id: str | None = None
) -> str:
    """Create findings.md with minimal inline sources."""
    now = datetime.now()

    # Extract topic from query
    query = parsed['initial_prompt']
    topic_match = re.sub(r'^(Research|Investigate|.*?research\s+)', '', query, flags=re.IGNORECASE)
    topic = topic_match[:80].strip() if topic_match else "Research Findings"

    # Build target fields if present
    target_fields = ""
    if target_id:
        target_fields = f"\ntarget_id: {target_id}\ntarget_link: \"[[research/targets/{target_id}]]\""

    # Build frontmatter
    frontmatter = f"""---
type: research
topic: {topic}
status: open
created: {now.strftime('%Y-%m-%d')}
completed: null
session: null
confidence: medium
led_to_decision: null{target_fields}
tags:
  - research
---"""

    # Build content
    content_parts = [frontmatter, ""]
    content_parts.append(f"# Research: {topic}\n")
    content_parts.append(f"**Question:** {query[:200]}{'...' if len(query) > 200 else ''}\n")
    content_parts.append("---\n")

    # Findings section - the full summary
    content_parts.append("## Findings\n")
    content_parts.append(parsed['final_summary'])
    content_parts.append("\n---\n")

    # Key Sources section - only top N high-relevance sources inline
    content_parts.append("## Key Sources\n")

    high_sources = ranked_sources.get("high", [])[:MAX_INLINE_SOURCES]
    if high_sources:
        for s in high_sources:
            content_parts.append(f"- [{s['title']}]({s['url']})")
        content_parts.append("")
    else:
        content_parts.append("*No high-relevance sources identified*\n")

    # Link to sources file (same folder)
    content_parts.append(f"**Full sources:** [[research/{output_folder}/sources]]\n")

    return "\n".join(content_parts)


def format_sources_markdown(
    output_folder: str,
    ranked_sources: dict[str, list],
    query: str,
    created: str,
    target_id: str | None = None
) -> str:
    """Create sources.md with full source list."""
    target_field = f"\ntarget_id: {target_id}" if target_id else ""
    frontmatter = f"""---
type: research-sources
output-id: {output_folder}
created: {created}{target_field}
---
"""
    content_parts = [frontmatter]
    content_parts.append(f"# Sources: {query[:60]}{'...' if len(query) > 60 else ''}\n")
    content_parts.append(f"**Findings:** [[research/{output_folder}/findings]]\n")
    content_parts.append("---\n")

    total_sources = 0
    for tier in ["high", "medium", "low"]:
        sources = ranked_sources.get(tier, [])
        if sources:
            content_parts.append(f"## {tier.capitalize()} Relevance\n")
            for s in sources:
                content_parts.append(f"- [{s['title']}]({s['url']})")
                total_sources += 1
            content_parts.append("")

    if total_sources == 0:
        content_parts.append("*No sources extracted*\n")
    else:
        content_parts.append(f"---\n**Total sources:** {total_sources}\n")

    return "\n".join(content_parts)


def should_capture_agent(parsed: dict) -> bool:
    """Only capture web-research agents."""
    return parsed['agent_type'] == 'web-research'


def export_agent_research(agent_file: Path, session_id: str) -> tuple[str | None, str | None]:
    """Export agent research to Obsidian vault as folder with findings + sources.

    Creates: research/{timestamp}-{slug}/
               ├── findings.md
               └── sources.md

    Returns (findings_path, sources_path) or (None, None) if skipped.
    """
    parsed = parse_agent_transcript(agent_file)

    if not should_capture_agent(parsed):
        return None, None

    if not parsed['final_summary'] and parsed['tool_count'] == 0:
        return None, None

    # Extract TARGET ID from initial prompt if present
    target_id = extract_target_id(parsed['initial_prompt'])

    # Get sources - try agent's ranking first, fallback to domain-based
    agent_ranked = extract_ranked_sources_from_summary(parsed['final_summary'])
    if agent_ranked:
        ranked_sources = agent_ranked
    else:
        all_sources = extract_sources_from_text(parsed['final_summary'])
        ranked_sources = rank_sources_by_domain(all_sources)

    # Generate folder name (no OUTPUT- prefix)
    slug = generate_slug(parsed['initial_prompt'])
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d-%H%M%S")
    output_folder = f"{timestamp}-{slug}"

    # Create output folder
    folder_path = RESEARCH_DIR / output_folder
    folder_path.mkdir(parents=True, exist_ok=True)

    # Generate findings markdown
    findings_markdown = format_findings_markdown(
        parsed, ranked_sources, output_folder, target_id
    )

    # Generate sources markdown
    sources_markdown = format_sources_markdown(
        output_folder,
        ranked_sources,
        parsed['initial_prompt'],
        now.strftime('%Y-%m-%d'),
        target_id
    )

    # Write findings.md
    findings_path = folder_path / "findings.md"
    with open(findings_path, "w", encoding="utf-8") as f:
        f.write(findings_markdown)

    # Write sources.md
    sources_path = folder_path / "sources.md"
    with open(sources_path, "w", encoding="utf-8") as f:
        f.write(sources_markdown)

    return str(findings_path), str(sources_path)


def main():
    """Entry point: capture research from deep-research subagent."""
    log_path = Path("/tmp/claude-research-hook.log")

    with open(log_path, "a") as log:
        log.write(f"\n=== SubagentStop at {datetime.now().isoformat()} ===\n")

        try:
            payload = json.load(sys.stdin)
            session_id = payload.get("session_id", "unknown")
            transcript_path = payload.get("transcript_path", "")

            log.write(f"Session: {session_id}\n")

            if not transcript_path:
                log.write("No transcript path\n")
                return

            transcript_file = Path(transcript_path)
            session_dir = transcript_file.parent
            subagents_dir = session_dir / session_id / "subagents"

            if not subagents_dir.exists():
                subagents_dir = session_dir / "subagents"

            if not subagents_dir.exists():
                log.write("Subagents directory not found\n")
                return

            processed = load_processed_agents()
            new_agent = find_new_agent(subagents_dir, processed)

            if not new_agent:
                log.write("No new agent to process\n")
                return

            log.write(f"Processing: {new_agent.name}\n")

            findings_path, sources_path = export_agent_research(new_agent, session_id)

            if findings_path:
                log.write(f"Exported findings to: {findings_path}\n")
                log.write(f"Exported sources to: {sources_path}\n")
            else:
                parsed = parse_agent_transcript(new_agent)
                log.write(f"Skipped: agent_type={parsed['agent_type']}\n")

            processed.add(new_agent.stem)
            save_processed_agents(processed)

        except Exception as e:
            log.write(f"Error: {e}\n")
            import traceback
            log.write(traceback.format_exc())


if __name__ == "__main__":
    main()
