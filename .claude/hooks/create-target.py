#!/usr/bin/env python3
"""
Create a research TARGET file efficiently.

Usage:
    echo '{"topic": "...", "question": "...", "why": "...", "needs": ["...", "..."]}' | python create-target.py

Or with minimal input (question only):
    echo '{"question": "What are the best practices for X?"}' | python create-target.py

Output (stdout): TARGET ID for use in subsequent operations
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


# ============================================================================
# Configuration - Relative paths from project root
# ============================================================================

def get_project_root() -> Path:
    """Get project root (parent of .claude/hooks/)."""
    return Path(__file__).parent.parent.parent


def get_research_paths() -> tuple[Path, Path]:
    """Get research paths relative to project root.

    Returns (vault_root, targets_dir).
    """
    project_root = get_project_root()
    vault_root = project_root / "vault"
    targets_dir = vault_root / "research" / "targets"
    return vault_root, targets_dir


# Load paths
OBSIDIAN_VAULT, RESEARCH_TARGETS_DIR = get_research_paths()
ACTIVE_TARGET_FILE = Path("/tmp/claude-active-research-target.txt")


def generate_slug(text: str, max_len: int = 40) -> str:
    """Generate URL-friendly slug from text."""
    text = re.sub(r'^(Research|Investigate|What|How|Why)\s+', '', text, flags=re.IGNORECASE)
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', text.lower())
    slug = re.sub(r'\s+', '-', slug.strip())
    if len(slug) > max_len:
        slug = slug[:max_len].rsplit('-', 1)[0]
    return slug or "research"


def extract_topic(question: str) -> str:
    """Extract topic from question if not provided."""
    # Remove common question prefixes
    topic = re.sub(
        r'^(What are|What is|How to|How do|Why does|Research|Investigate)\s+',
        '', question, flags=re.IGNORECASE
    )
    # Take first 60 chars, break at word boundary
    if len(topic) > 60:
        topic = topic[:60].rsplit(' ', 1)[0]
    return topic.strip() or "Research Topic"


def create_target(data: dict) -> str:
    """Create TARGET file and return target ID."""
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d-%H%M%S")
    date_str = now.strftime("%Y-%m-%d")

    # Extract fields with defaults
    question = data.get("question", "").strip()
    if not question:
        raise ValueError("Question is required")

    topic = data.get("topic", "").strip() or extract_topic(question)
    why = data.get("why", "").strip() or "Research needed for current task"
    needs = data.get("needs", [])
    if not needs:
        needs = ["Key findings", "Best practices", "Recommendations"]

    # Generate IDs and paths
    target_id = f"TARGET-{timestamp}"
    slug = generate_slug(topic)
    filename = f"{target_id}-{slug}.md"

    # Build needs list
    needs_md = "\n".join([f"- {need}" for need in needs])

    # Build content
    content = f"""---
type: research-target
id: {target_id}
status: open
created: {date_str}
output: null
tags:
  - research
---

# Research Target: {topic}

## Question
{question}

## Why
{why}

## What We Need
{needs_md}

## Related
- Session: Current session

## Status Notes
**{date_str}**: Created, research initiated
"""

    # Ensure directory exists
    RESEARCH_TARGETS_DIR.mkdir(parents=True, exist_ok=True)

    # Write file
    target_path = RESEARCH_TARGETS_DIR / filename
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Set as active target
    ACTIVE_TARGET_FILE.write_text(target_id)

    return target_id


def main():
    """Entry point."""
    try:
        data = json.load(sys.stdin)
        target_id = create_target(data)
        # Output target ID to stdout for capture
        print(target_id)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
