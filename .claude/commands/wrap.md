# Session Wrap-up Command

This command performs end-of-session tasks: create session note with Handoff, and optionally commit changes.

## Instructions

When the user invokes `/wrap`, perform these steps in order:

### Step 1: Determine Session Number

Scan the Sessions folder to find the next session number:
- Check both `Sessions/` and `Sessions/transcripts/` for `session-N.md` files
- Find the highest N and use N+1 (or N if transcript already exists for this session)
- Session naming: `session-1`, `session-2`, etc.

```bash
ls -1 /home/berkaygkv/Dev/Docs/.obs-vault/notes/Sessions/*.md /home/berkaygkv/Dev/Docs/.obs-vault/notes/Sessions/transcripts/*.md 2>/dev/null | grep -oP 'session-\d+' | sort -t- -k2 -n | tail -1
```

### Step 2: Read Current Session Context

Find the current session transcript to understand what happened:
- Location: `~/.claude/projects/-home-berkaygkv-Dev-headquarter-kh/`
- Find the most recently modified `.jsonl` file
- Read it to extract key information for the Handoff

### Step 3: Generate Session Note (Handoff Document)

Create a session note following this schema:

```yaml
---
session: {N}
date: {YYYY-MM-DD}
project: kh
topics: [topic1, topic2]
outcome: successful | partial | blocked
continues_from: session-{N-1}
transcript: "[[Sessions/transcripts/session-{N}]]"
tags:
  - session
---

## Handoff

### Context
[What we were working on this session - 2-3 sentences summarizing the main focus]

### Decisions
- LOCKED: [decision] — [rationale]
- OPEN: [question still unresolved]

### Memory
[Important things to remember across sessions - facts, preferences, constraints discovered]

### Next Steps
[Where to pick up, what's pending - actionable items for the next session]
```

**Guidelines for Handoff generation:**

- **topics**: Extract 2-5 key topics/themes from the session (free-form tags)
- **outcome**:
  - `successful` = goals achieved, clear progress made
  - `partial` = some progress but incomplete
  - `blocked` = stuck on something, needs resolution
- **Context**: Brief summary of what the session focused on. This is what `/begin` will show to restore context.
- **Decisions**:
  - LOCKED = decisions that are final, with rationale
  - OPEN = questions still unresolved, need future attention
- **Memory**: Important facts discovered that should persist (e.g., "User prefers X over Y", "The API has limitation Z")
- **Next Steps**: Concrete, actionable items. What should the next session start with?

### Step 4: Write Session Note to Obsidian

Use the Obsidian MCP to write the session note:
- Path: `/notes/Sessions/session-{N}.md`
- Use `mcp__obsidian__write_note`

### Step 5: Git Status & Commit (Optional)

1. Show `git status` to display uncommitted changes
2. Show `git diff --stat` for a summary of changes
3. Ask the user if they want to commit
4. If yes, generate an appropriate commit message and create the commit

### Step 6: Confirm Completion

Report what was done:
- Session note location: `Sessions/session-{N}.md`
- Topics extracted
- Next steps summary
- Git commit status (if applicable)

Remind the user:
- Transcript will be exported automatically when session ends (SessionEnd hook)
- Transcript will be saved to `Sessions/transcripts/session-{N}.md`
- Use `/begin` in next session to load this Handoff

## Example Output

```
Session note created: Sessions/session-15.md

Topics: [sessions-architecture, vault-cleanup, templates]
Outcome: successful

Next Steps:
- Create /begin command
- Test full session lifecycle

Transcript will be exported on session end.
```
