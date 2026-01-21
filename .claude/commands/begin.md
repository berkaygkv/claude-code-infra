# Session Begin Command

This command loads context from the previous session and prepares the session scratch file.

## Design Rationale

**What we read and why:**
- **Session handoff** — Continuity from last session (context, decisions, memory, next steps)
- **runbook.md** — Operational state (active tasks, knowledge gaps, blockers)
- **locked.md** — Fundamental constraints and committed decisions

**What we don't read at /begin:**
- **overview.md** — Obsidian dashboard for human navigation; redundant for Claude
- **schemas.md** — Reference documentation; structures are inline in skills where needed

## Instructions

When the user invokes `/begin`, perform these steps in order:

### Step 1: Find Most Recent Session

Scan the Sessions folder to find the latest session note:

```bash
ls -1 /home/berkaygkv/Dev/Docs/.obs-vault/notes/Sessions/session-*.md 2>/dev/null | grep -oP 'session-\d+' | sort -t- -k2 -n | tail -1
```

### Step 2: Read Previous Session Handoff

Use native Read for the session note (consistent with Vault I/O Strategy):
- Path: `/home/berkaygkv/Dev/Docs/.obs-vault/notes/Sessions/session-{N}.md`

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

### Step 4: Read Operational State

Load current state from project documents (use native Read):
- `/home/berkaygkv/Dev/Docs/.obs-vault/notes/runbook.md` — tasks, knowledge gaps, blockers
- `/home/berkaygkv/Dev/Docs/.obs-vault/notes/locked.md` — committed decisions/constraints

### Step 5: Summarize Current State

Provide a brief summary:

```
## Current State

**Phase:** {from runbook frontmatter}
**Blockers:** {from runbook frontmatter, or "none"}

**Active Tasks:**
{incomplete tasks from runbook Active section}

**Knowledge Gaps:**
{from runbook Knowledge Gaps table, or "None"}
```

Note: locked.md is read for Claude's context (constraints/guardrails) but not displayed — the user already knows the locked decisions.

### Step 6: Prepare Session Scratch

Reset and prepare `scratch.md` for the new session using native Write:
- Path: `/home/berkaygkv/Dev/headquarter/kh/scratch.md`

**Template content** (with session number filled in):

```markdown
# Session Scratch

## Meta
- session: {N+1}

## Decisions
<!-- LOCKED: decision — rationale -->
<!-- OPEN: question still unresolved -->

## Memory
<!-- Facts, preferences, constraints to persist -->

## Tasks
<!-- New tasks, completed tasks, blockers -->

## Notes
<!-- Anything else to capture -->
```

Where `{N+1}` is the next session number (previous session number + 1).

### Step 7: Prompt for Session Focus

```
Ready to continue. What's the focus of this session?

Suggested (from previous session):
- {first next step}
- {second next step}
```

After the user provides direction, confirm:

```
Session {N+1} initialized. Scratch file ready.
```

**Note:** Topic is not set upfront—it emerges during the session and gets captured at `/wrap` time.

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

**Knowledge Gaps:** None

---

Ready to continue. What's the focus of this session?

Suggested (from previous session):
- Define session handoff schemas
- Create session templates
```

**User:** Working on session templates

**Claude:** Session 3 initialized. Scratch file ready.

## Notes

- If no previous session exists, inform the user and offer to start fresh (session 1)
- If the previous session outcome was `blocked`, highlight the blocker prominently
- The handoff context should be enough to resume work without reading the full transcript
- scratch.md is the staging area for vault writes during the session
- schemas.md is reference documentation; skills have structures inline where needed
