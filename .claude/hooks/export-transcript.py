#!/usr/bin/env python3
"""
Claude Code SessionEnd Hook: Export transcript to Obsidian vault.

This hook runs when a Claude Code session ends. It ONLY exports the transcript
if /wrap was run during the session (i.e., a session note exists without a
matching transcript). This makes /wrap the explicit signal to preserve a session.

Behavior:
- /wrap run → session note exists → export transcript to match
- /wrap NOT run → skip export (session discarded)

Naming: session-N.md (sequential numbering, matches session note)
Location: /notes/Sessions/transcripts/session-N.md

Usage: Configured in .claude/settings.json under hooks.SessionEnd
"""

import json
import re
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Any

# Configuration
OBSIDIAN_VAULT = Path("/home/berkaygkv/Dev/Docs/.obs-vault")
SESSIONS_DIR = OBSIDIAN_VAULT / "notes" / "Sessions"
TRANSCRIPTS_DIR = SESSIONS_DIR / "transcripts"


def get_session_number_if_wrapped() -> int | None:
    """Get session number ONLY if /wrap was run (session note exists without transcript).

    Returns:
        Session number if /wrap was run and transcript needed, None otherwise.

    Logic:
    - /wrap creates session note BEFORE session ends
    - If session note exists without matching transcript → return that number
    - If no unmatched session note → return None (skip export, /wrap wasn't run)
    """
    pattern = re.compile(r'^session-(\d+)[a-z]?\.md$')

    # Collect existing session notes and transcripts
    session_notes = set()
    transcripts = set()

    if SESSIONS_DIR.exists():
        for f in SESSIONS_DIR.iterdir():
            if f.is_file():
                match = pattern.match(f.name)
                if match:
                    session_notes.add(int(match.group(1)))

    if TRANSCRIPTS_DIR.exists():
        for f in TRANSCRIPTS_DIR.iterdir():
            # Only count non-empty files (Obsidian may create empty files when clicking wikilinks)
            if f.is_file() and f.stat().st_size > 0:
                match = pattern.match(f.name)
                if match:
                    transcripts.add(int(match.group(1)))

    # Check for session notes without matching transcripts (from /wrap)
    unmatched = session_notes - transcripts
    if unmatched:
        # Use the highest unmatched session number (most recent /wrap)
        return max(unmatched)

    # No /wrap was run — skip export
    return None


def parse_jsonl_transcript(transcript_path: str) -> list[dict[str, Any]]:
    """Read and parse the JSONL transcript file."""
    entries = []
    with open(transcript_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return entries


def format_message_content(content: Any) -> str:
    """Format message content for markdown output."""
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        # Handle content blocks (text, tool_use, tool_result, etc.)
        parts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    parts.append(block.get("text", ""))
                elif block.get("type") == "tool_use":
                    tool_name = block.get("name", "unknown")
                    tool_input = json.dumps(block.get("input", {}), indent=2)
                    parts.append(f"**Tool: {tool_name}**\n```json\n{tool_input}\n```")
                elif block.get("type") == "tool_result":
                    result = block.get("content", "")
                    if isinstance(result, list):
                        result = "\n".join(
                            str(r.get("text", r)) if isinstance(r, dict) else str(r)
                            for r in result
                        )
                    parts.append(f"**Tool Result:**\n```\n{result[:2000]}...\n```" if len(str(result)) > 2000 else f"**Tool Result:**\n```\n{result}\n```")
            elif isinstance(block, str):
                parts.append(block)
        return "\n\n".join(parts)
    elif isinstance(content, dict):
        return json.dumps(content, indent=2)
    return str(content)


def transcript_to_markdown(entries: list[dict[str, Any]], session_num: int) -> str:
    """Convert transcript entries to markdown format."""
    lines = []
    session_name = f"session-{session_num}"

    # Extract timestamps
    timestamps = [e.get("timestamp", "") for e in entries if e.get("timestamp")]
    time_start = timestamps[0][:16].replace("T", " ") if timestamps else ""
    time_end = timestamps[-1][:16].replace("T", " ") if timestamps else ""
    date = timestamps[0][:10] if timestamps else datetime.now().strftime("%Y-%m-%d")

    # Build frontmatter
    frontmatter = f"""---
session: {session_num}
date: {date}
time_start: "{time_start}"
time_end: "{time_end}"
project: kh
session_note: "[[Sessions/{session_name}]]"
tags:
  - session
  - transcript
---
"""
    lines.append(frontmatter)
    lines.append(f"# Session {session_num} Transcript\n")

    # Process each entry
    for entry in entries:
        entry_type = entry.get("type", "unknown")

        if entry_type == "human":
            # User message
            content = format_message_content(entry.get("message", {}).get("content", ""))
            if content.strip():
                lines.append(f"## User\n\n{content}\n")

        elif entry_type == "assistant":
            # Assistant message
            content = format_message_content(entry.get("message", {}).get("content", ""))
            if content.strip():
                lines.append(f"## Assistant\n\n{content}\n")

        elif entry_type == "summary":
            # Context summary (from compaction)
            summary = entry.get("summary", "")
            if summary:
                lines.append(f"## [Context Summary]\n\n{summary}\n")

    return "\n".join(lines)


def export_transcript(payload: dict[str, Any]) -> int:
    """Main export function. Returns the session number used, or 0 if skipped."""
    transcript_path = payload.get("transcript_path")

    if not transcript_path or not os.path.exists(transcript_path):
        print(f"Transcript file not found: {transcript_path}", file=sys.stderr)
        return 0

    # Check if /wrap was run (session note exists without transcript)
    session_num = get_session_number_if_wrapped()
    if session_num is None:
        print("No /wrap detected — skipping transcript export", file=sys.stderr)
        return 0

    # Parse transcript
    entries = parse_jsonl_transcript(transcript_path)
    if not entries:
        print("No entries found in transcript", file=sys.stderr)
        return 0

    session_name = f"session-{session_num}"

    # Convert to markdown
    markdown = transcript_to_markdown(entries, session_num)

    # Ensure output directory exists
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

    # Write to vault
    output_path = TRANSCRIPTS_DIR / f"{session_name}.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"Exported transcript to {output_path}", file=sys.stderr)
    return session_num


def main():
    """Entry point: read hook payload from stdin and export."""
    # Debug logging to file
    log_path = Path("/tmp/claude-hook-debug.log")
    with open(log_path, "a") as log:
        log.write(f"\n=== SessionEnd Hook at {datetime.now().isoformat()} ===\n")
        try:
            raw_input = sys.stdin.read()
            log.write(f"Raw input: {raw_input[:500]}...\n")
            payload = json.loads(raw_input)
            log.write(f"Parsed payload keys: {list(payload.keys())}\n")
            session_num = export_transcript(payload)
            log.write(f"Export completed: session-{session_num}\n")
        except json.JSONDecodeError as e:
            log.write(f"JSON decode error: {e}\n")
            print(f"Failed to parse hook payload: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            log.write(f"Exception: {e}\n")
            import traceback
            log.write(traceback.format_exc())
            print(f"Export failed: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
