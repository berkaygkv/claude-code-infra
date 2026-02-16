#!/usr/bin/env python3
"""
Claude Code SubagentStop Hook: Capture deep-research agent findings.

Runs when any subagent finishes but only captures deep-research (web-research)
agents, exporting findings to the Obsidian vault.

Output structure (research format v2):
  {vault}/research/{YYYYMMDD}-{slug}.md    — flat file, frontmatter, inline sources
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


# ============================================================================
# Configuration
# ============================================================================

def get_project_root() -> Path:
    """Get project root (parent of .claude/hooks/)."""
    return Path(__file__).parent.parent.parent


def find_vault(project_root: Path) -> Path:
    """Find the Obsidian vault directory (contains .obsidian/).

    Searches immediate children of project root. Falls back to 'vault/'.
    """
    for child in project_root.iterdir():
        if child.is_dir() and (child / ".obsidian").exists():
            return child
    return project_root / "vault"


PROJECT_ROOT = get_project_root()
OBSIDIAN_VAULT = find_vault(PROJECT_ROOT)
RESEARCH_DIR = OBSIDIAN_VAULT / "research"
PROCESSED_AGENTS_FILE = Path("/tmp/claude-processed-agents.json")


# ============================================================================
# Dedup tracking
# ============================================================================

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


# ============================================================================
# Agent discovery & parsing
# ============================================================================

def find_new_agent(subagents_dir: Path, processed: set[str]) -> Path | None:
    """Find the newest agent file that hasn't been processed yet."""
    if not subagents_dir.exists():
        return None
    agent_files = list(subagents_dir.glob("agent-*.jsonl"))
    unprocessed = [f for f in agent_files if f.stem not in processed]
    if not unprocessed:
        return None
    return max(unprocessed, key=lambda f: f.stat().st_mtime)


def parse_agent_transcript(agent_file: Path) -> dict[str, Any]:
    """Parse agent JSONL transcript and extract key information."""
    entries = []
    tool_calls = []

    with open(agent_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                entries.append(entry)
                if entry.get("type") == "assistant":
                    for block in entry.get("message", {}).get("content", []):
                        if isinstance(block, dict) and block.get("type") == "tool_use":
                            tool_calls.append(block.get("name"))
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
    if any(t in ["WebSearch", "WebFetch"] for t in tool_calls):
        agent_type = "web-research"
    elif any(t in ["Glob", "Grep", "Read"] for t in tool_calls):
        agent_type = "explore"
    elif "Bash" in tool_calls:
        agent_type = "bash"

    return {
        "initial_prompt": initial_prompt,
        "final_summary": final_summary,
        "agent_type": agent_type,
        "tool_count": len(tool_calls),
    }


def should_capture_agent(parsed: dict) -> bool:
    """Only capture web-research agents."""
    return parsed["agent_type"] == "web-research"


# ============================================================================
# Source extraction & slug generation
# ============================================================================

def generate_slug(text: str, max_len: int = 40) -> str:
    """Generate a clean 2-4 word slug from text."""
    text = re.sub(r'^(Research|Investigate|Look into|Find out about)\s+', '', text, flags=re.IGNORECASE)
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', text.lower())
    slug = re.sub(r'\s+', '-', slug.strip())
    if len(slug) > max_len:
        slug = slug[:max_len].rsplit('-', 1)[0]
    return slug or "research"


def extract_sources_from_text(text: str) -> list[dict]:
    """Extract markdown links and bare URLs as a flat list."""
    sources = []
    seen: set[str] = set()

    def _clean(url: str) -> str:
        return url.rstrip(".,;:)'\">")

    # Markdown links [title](url)
    for m in re.finditer(r'\[([^\]]+)\]\((https?://[^\)]+)\)', text):
        title, url = m.group(1).strip(), _clean(m.group(2))
        if url not in seen:
            seen.add(url)
            sources.append({"title": title, "url": url})

    # "title - url" or "title: url"
    for m in re.finditer(r'(?:^|\n)\s*(?:\d+\.?\s+|-\s+)?(.+?)\s*[-\u2013\u2014:]\s+(https?://\S+)', text):
        title, url = re.sub(r'\*+', '', m.group(1)).strip(), _clean(m.group(2))
        if url not in seen and title:
            seen.add(url)
            sources.append({"title": title, "url": url})

    # Bare URLs
    for m in re.finditer(r'(https?://[^\s\)\]>]+)', text):
        url = _clean(m.group(1))
        if url not in seen:
            seen.add(url)
            sources.append({"title": urlparse(url).netloc, "url": url})

    return sources


# ============================================================================
# Markdown formatting (v2 — flat file, inline sources)
# ============================================================================

def format_research_markdown(parsed: dict[str, Any], sources: list[dict]) -> str:
    """Create single research file with frontmatter and inline sources."""
    now = datetime.now()
    query = parsed["initial_prompt"]
    topic = re.sub(r'^(Research|Investigate|.*?research\s+)', '', query, flags=re.IGNORECASE)[:80].strip() or "Research Findings"

    lines = [
        "---",
        "type: research",
        f"date: {now.strftime('%Y-%m-%d')}",
        f"topic: \"{topic}\"",
        "---",
        "",
        f"# {topic}",
        "",
        f"**Question:** {query[:200]}{'...' if len(query) > 200 else ''}",
        "",
        "---",
        "",
        "## Findings",
        "",
        parsed["final_summary"],
        "",
        "---",
        "",
        "## Sources",
        "",
    ]

    if sources:
        for i, s in enumerate(sources, 1):
            lines.append(f"{i}. [{s['title']}]({s['url']})")
    else:
        lines.append("*No sources identified*")

    lines.append("")
    return "\n".join(lines)


# ============================================================================
# Export
# ============================================================================

def export_agent_research(agent_file: Path) -> str | None:
    """Export agent research to vault as a single flat file.

    Returns the file path or None if skipped.
    """
    parsed = parse_agent_transcript(agent_file)

    if not should_capture_agent(parsed):
        return None
    if not parsed["final_summary"] and parsed["tool_count"] == 0:
        return None

    sources = extract_sources_from_text(parsed["final_summary"])

    slug = generate_slug(parsed["initial_prompt"])
    now = datetime.now()
    filename = f"{now.strftime('%Y%m%d')}-{slug}.md"

    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)

    content = format_research_markdown(parsed, sources)

    output_path = RESEARCH_DIR / filename
    output_path.write_text(content, encoding="utf-8")

    return str(output_path)


# ============================================================================
# Main
# ============================================================================

def main():
    """Entry point: capture research from deep-research subagent."""
    log_path = Path("/tmp/claude-research-hook.log")

    with open(log_path, "a") as log:
        log.write(f"\n=== SubagentStop at {datetime.now().isoformat()} ===\n")
        log.write(f"Vault: {OBSIDIAN_VAULT}\n")

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

            output_path = export_agent_research(new_agent)

            if output_path:
                log.write(f"Exported to: {output_path}\n")
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
