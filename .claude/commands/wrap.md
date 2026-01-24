# Session Wrap-up Command

This command performs end-of-session tasks: process the session scratch file, update vault documents, create session handoff note, and commit changes.

## Design Rationale

**I/O Strategy (per locked decision):**
- **Native Read/Write** for all content operations (scratch.md, runbook.md, overview.md, locked.md, session notes)
- **MCP** only for metadata operations if needed (frontmatter-only updates, search, tags)

**Documents updated:**
- `runbook.md` — Task state, phase, blockers
- `overview.md` — Dashboard state, recent sessions
- `locked.md` — New LOCKED decisions (if any)
- `session-{N}.md` — Session handoff note (created)
- `scratch.md` — Reset and prepared for next session (N+1)
- `CLAUDE.md` — Evolved patterns (if any)

## Configuration

First, read the KH config to get paths:
- Config file: `kh/.kh-config.json`

Extract:
- `vault_root` → Base path for vault operations
- `vault_path` → Path to notes folder
- `kh_path` → Path to kh repository

All paths below use these config values:
- Session notes: `{vault_path}/Sessions/session-{N}.md`
- Transcripts: `{vault_path}/Sessions/transcripts/session-{N}.md`
- Runbook: `{vault_path}/runbook.md`
- Overview: `{vault_path}/overview.md`
- Locked decisions: `{vault_path}/locked.md`
- Scratch: `{kh_path}/scratch.md`

## Instructions

When the user invokes `/wrap`, perform these steps in order:

### Step 0: Load Configuration

Read `kh/.kh-config.json` to get vault and kh paths. If config missing, show error and abort.

### Step 1: Read Session Scratch

Read the session scratch file using native Read (consistent with Vault I/O Strategy):
- Path: `{kh_path}/scratch.md`

Extract:
- **Session number** from Meta section
- **Decisions** (LOCKED and OPEN items)
- **Memory** items to persist
- **Tasks** (new, completed, blockers)
- **Notes** (additional context)

If scratch.md is empty or only has the template, synthesize from conversation context instead.

### Step 2: Determine Session Number

If session number is in scratch.md Meta section, use that.

Otherwise, scan the Sessions folder to find the next session number:

```bash
ls -1 {vault_path}/Sessions/*.md {vault_path}/Sessions/transcripts/*.md 2>/dev/null | grep -oP 'session-\d+' | sort -t- -k2 -n | tail -1
```

Use N+1 as the session number.

### Step 3: Synthesize Session Work

Combine scratch.md content with conversation context to synthesize:
- What tasks were completed?
- What decisions were made (LOCKED vs OPEN)?
- What new tasks or blockers emerged?
- What is the current phase and next action?
- What should the next session start with?
- What are the key topics/themes of this session?

This synthesis informs all document updates below.

### Step 4: Update Runbook

Read and update runbook using native Read/Write (consistent with Vault I/O Strategy):
- Path: `{vault_path}/runbook.md`

1. **Mark completed tasks:** Change `- [ ]` to `- [x]` and add completion date `✅YYYY-MM-DD`
2. **Add new tasks:** From scratch.md Tasks section, add to Active with `[phase:: x] [priority:: n]`
3. **Update frontmatter:**
   - `updated`: Today's date
   - `phase`: Current phase (infrastructure, validation, research, etc.)
   - `blockers`: Any blockers from scratch.md, or "none"
4. **Update Progress section:** Link to this session
5. **Update Knowledge Gaps:** Add any gaps discovered during the session

Use native Read to get current content, Edit for surgical updates, or Write for full replacement.

### Step 5: Update Overview

Read and update overview using native Read/Write:
- Path: `{vault_path}/overview.md`

1. **Update frontmatter:**
   - `updated`: Today's date
   - `current_phase`: Current phase
   - `next_action`: First item from Next Steps
2. **Update Current State table:** Phase, Next Action, Blockers
3. **Update Recent Sessions table:** Add this session (keep last 5 sessions)
   - Format: `| [[Sessions/session-{N}\|Session {N}]] | {date} | {outcome} | {primary topic} |`
4. **Update Active Research:** If research tasks are in progress

### Step 6: Update Locked Decisions (if applicable)

If any LOCKED decisions are in scratch.md or were made this session, update locked.md using native Read/Write:
- Path: `{vault_path}/locked.md`
- Add to Decisions table with Area, Decision, Rationale

Skip this step if no new LOCKED decisions were made.

### Step 7: Generate Session Note (Handoff Document)

Create a session note using scratch.md content and conversation synthesis:

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
[From scratch.md Decisions section + any decisions from conversation]
- LOCKED: [decision] — [rationale]
- OPEN: [question still unresolved]

### Memory
[From scratch.md Memory section]
[Important things to remember across sessions - facts, preferences, constraints discovered]

### Next Steps
[Where to pick up, what's pending - actionable items for the next session]
```

**Guidelines for Handoff generation:**

- **topics**: Extract 2-5 key topics/themes from the session (derive from scratch.md and conversation)
- **outcome**:
  - `successful` = goals achieved, clear progress made
  - `partial` = some progress but incomplete
  - `blocked` = stuck on something, needs resolution
- **Context**: Brief summary of what the session focused on. This is what `/begin` will show to restore context.
- **Decisions**: Merge scratch.md Decisions with any decisions made in conversation
- **Memory**: Merge scratch.md Memory with important facts from conversation
- **Next Steps**: Concrete, actionable items. What should the next session start with?

### Step 8: Write Session Note

Write the session note using native Write:
- Path: `{vault_path}/Sessions/session-{N}.md`

### Step 9: Reset Session Scratch for Next Session

Reset scratch.md and prepare it for the next session using native Write:
- Path: `{kh_path}/scratch.md`
- Set session number to **N+1** (current session + 1)

**Template content:**

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

This ensures `/begin` doesn't need to write to scratch.md — it's already prepared.

### Step 10: Living CLAUDE.md Review

Review the session for patterns that should persist in CLAUDE.md:

**Look for:**
- Repeated corrections ("I said X, not Y" multiple times)
- Expressed preferences ("always do X", "never do Y")
- Workflow adjustments that improved the session
- Anti-patterns that caused friction

**If patterns found:**

Present them to the user:

```
## CLAUDE.md Candidates

I noticed these patterns this session that might be worth adding to CLAUDE.md:

1. **{pattern}** — {why it matters}
2. **{pattern}** — {why it matters}

Would you like me to add any of these to CLAUDE.md?
```

**If approved:**
- Read current CLAUDE.md
- Add to appropriate section (or create new section if needed)
- Keep additions concise — these are operational instructions, not documentation

**If no patterns or user declines:** Skip silently.

**Note:** This step is about evolving the system prompt based on observed friction. Not every session will have candidates.

### Step 11: Git Commit (Automatic)

Invoking `/wrap` signals approval to commit. Commit changes to the kh repo:

```bash
cd {kh_path}
git status
git add -A
git commit -m "Session {N}: {brief summary}"
```

Skip commit if no changes. Report commit hash in Step 12.

**Note:** Notes in Obsidian vault are not git-tracked. scratch.md is reset, not committed with content.

### Step 12: Confirm Completion

Report what was done in a summary table:

```
## Session {N} Wrap-up Complete

| Document | Action |
|----------|--------|
| runbook.md | Updated: {tasks completed}, phase: {phase} |
| overview.md | Updated: added session to recent, next action: {action} |
| locked.md | {Updated with N decisions / No changes} |
| session-{N}.md | Created with handoff |
| scratch.md | Reset to template |
| CLAUDE.md | {Updated with N patterns / No changes} |

**Topics:** {topics}
**Outcome:** {outcome}

**Next Steps:**
1. {first next step}
2. {second next step}

**Git:** {committed (hash) / no changes}

Transcript will export automatically when session ends.
Use `/begin` in next session to resume.
```

## Example Output

```
## Session 15 Wrap-up Complete

| Document | Action |
|----------|--------|
| runbook.md | Updated: 2 tasks completed, phase: validation |
| overview.md | Updated: added session to recent, next action: Test transcript export |
| locked.md | Updated with 1 decision |
| session-15.md | Created with handoff |
| scratch.md | Reset to template |
| CLAUDE.md | No changes |

**Topics:** [scratch-file-implementation, vault-staging]
**Outcome:** successful

**Next Steps:**
1. Test full session lifecycle with new scratch.md flow
2. Use framework for real project work

**Git:** Committed (abc1234)

Transcript will export automatically when session ends.
Use `/begin` in next session to resume.
```

## Scratch File Reference

The scratch file (`{kh_path}/scratch.md`) is a staging area for vault writes:

| Section | Purpose | Maps to |
|---------|---------|---------|
| Meta | Session number | Session note frontmatter |
| Decisions | LOCKED/OPEN items | locked.md + session handoff |
| Memory | Facts to persist | Session handoff Memory section |
| Tasks | Work items | runbook.md |
| Notes | Misc context | Session handoff Context/Notes |

If scratch.md is sparse, supplement with conversation context. The goal is to capture everything important before it's lost.
