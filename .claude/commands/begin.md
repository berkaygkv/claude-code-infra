# Session Begin Command

This command loads context from the previous session to enable seamless handoff.

## Instructions

When the user invokes `/begin`, perform these steps in order:

### Step 1: Find Most Recent Session

Scan the Sessions folder to find the latest session note:

```bash
ls -1 /home/berkaygkv/Dev/Docs/.obs-vault/notes/Sessions/session-*.md 2>/dev/null | grep -oP 'session-\d+' | sort -t- -k2 -n | tail -1
```

### Step 2: Read Previous Session Handoff

Use Obsidian MCP to read the session note:
- Path: `notes/Sessions/session-{N}.md`
- Use `mcp__obsidian__read_note`

### Step 3: Display Handoff Context

Present the handoff information clearly:

```
## Resuming from Session {N}

**Date:** {date}
**Topics:** {topics}
**Outcome:** {outcome}

### Context
{context from handoff}

### Decisions
{decisions from handoff}

### Memory
{memory from handoff}

### Next Steps
{next steps from handoff}
```

### Step 4: Read Key Project Documents

Load current state from project documents:
- Read `notes/runbook.md` for current tasks/phase
- Read `notes/overview.md` for project state
- Optionally read `notes/locked.md` if decisions are referenced

### Step 5: Summarize Current State

Provide a brief summary:

```
## Current State

**Phase:** {from runbook frontmatter}
**Blockers:** {from runbook frontmatter}

**Active Tasks:**
{incomplete tasks from runbook}
```

### Step 6: Set Session Context

Prompt for session focus:

```
Ready to continue. What's the focus of this session?

Suggested (from previous session):
- {first next step}
- {second next step}
```

After the user provides a topic, write session context to temp file:

```bash
cat > /tmp/kh-session.json << 'EOF'
{"session_number": {N+1}, "topic": "{user-provided-topic}", "date": "{YYYY-MM-DD}"}
EOF
```

Where:
- `{N+1}` is the next session number (previous session number + 1)
- `{user-provided-topic}` is a kebab-case slug from the user's response (e.g., "meta-journal-system")
- `{YYYY-MM-DD}` is today's date

Confirm with:

```
Session 8: {topic} initialized.
```

## Example Output

```
## Resuming from Session 2

**Date:** 2026-01-19
**Topics:** project-documents, symlink-setup, dataview-tasks
**Outcome:** successful

### Context
This session focused on creating core project documents and establishing
the symlink structure for git versioning.

### Decisions
- LOCKED: Files live in kh/notes/, symlinked into Obsidian vault
- OPEN: Obsidian doesn't auto-refresh when files created externally

### Memory
- Vault path: /home/berkaygkv/Dev/Docs/.obs-vault
- MCP search doesn't work through symlinks (use Grep instead)

### Next Steps
- Define session handoff schemas
- Create session templates

---

## Current State

**Phase:** infrastructure
**Blockers:** none

**Active Tasks:**
- [ ] Define session handoff schemas [priority:: 1]
- [ ] Create session templates [priority:: 2]

---

Ready to continue. What's the focus of this session?

Suggested (from previous session):
- Define session handoff schemas
- Create session templates
```

**User:** Working on session templates

**Claude:**
```bash
cat > /tmp/kh-session.json << 'EOF'
{"session_number": 3, "topic": "session-templates", "date": "2026-01-19"}
EOF
```

```
Session 3: session-templates initialized.
```

## Notes

- If no previous session exists, inform the user and offer to start fresh
- If the previous session outcome was `blocked`, highlight the blocker prominently
- The handoff context should be enough to resume work without reading the full transcript
