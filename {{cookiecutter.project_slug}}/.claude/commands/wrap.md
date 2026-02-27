# Session Wrap-up Command

End-of-session tasks: process {{cookiecutter.project_slug}}/scratch.md, update state.md, capture inbox items, create session handoff, create decision files.

## Design Rationale

**I/O Strategy:**
- Native Read/Write for all content operations
- MCP only for metadata operations if needed (frontmatter-only updates, search, tags)

**Documents updated:**
- `{{cookiecutter.project_slug}}/state.md` — Current state, lifecycle sections
- `{{cookiecutter.project_slug}}/inbox.md` — Raw idea capture (appended)
- `{{cookiecutter.project_slug}}/decisions/*.md` — New LOCKED decisions (created)
- `{{cookiecutter.project_slug}}/sessions/session-{N}.md` — Session handoff note (created)
- `{{cookiecutter.project_slug}}/scratch.md` — Reset for next session

## Paths

All paths relative to project root:

- Vault: `{{cookiecutter.project_slug}}/`
- State: `{{cookiecutter.project_slug}}/state.md`
- Inbox: `{{cookiecutter.project_slug}}/inbox.md`
- Sessions: `{{cookiecutter.project_slug}}/sessions/session-{N}.md`
- Transcripts: `{{cookiecutter.project_slug}}/sessions/transcripts/session-{N}.md`
- Decisions: `{{cookiecutter.project_slug}}/decisions/`
- Scratch: `{{cookiecutter.project_slug}}/scratch.md`

## Instructions

When the user invokes `/wrap`, perform these steps:

### Step 0: Resolve Vault Path

The vault is the directory containing `.obsidian/` inside the project root. All `{{cookiecutter.project_slug}}/` references below use this as the default — substitute with the actual vault directory name if different.

### Step 1: Read Scratch Pad

Read `{{cookiecutter.project_slug}}/scratch.md`. Use the Problem section, reasoning bullets, and any `## Decided` section or callout annotations to understand the *why* behind session decisions — not just what was decided, but the reasoning, rejected alternatives, and context.

If scratch.md is empty or objective is still `[TBD]`, synthesize from conversation context.

### Step 2: Determine Session Number

Get session number from scratch.md header (`# Scratch — Session {N}`).

If not found, read {{cookiecutter.project_slug}}/state.md to get current_session, use that.

### Step 3: Synthesize Session Work

Combine scratch.md reasoning with conversation context:
- What items were completed? (These will be removed from state.md)
- What decisions were made (LOCKED vs OPEN)?
- What items are still in progress, and at what sub-phase?
- What new ideas or future work surfaced but weren't acted on? (These go to inbox)
- What items got shaped during the session? (These go to Shaped)
- What should the next session start with?
- What are the key topics/themes?

### Step 4: Create Decision Files

For each LOCKED decision identified from scratch.md and conversation:

**Granularity rule:** One decision file per distinct decision. Related decisions made together may be bundled into one file with sub-sections (e.g., "MVP Scope" containing D1-D7), but each bundle gets ONE file.

1. Generate slug from decision title (lowercase, hyphens)
2. Read `{{cookiecutter.project_slug}}/decisions/{slug}.md` first (it may already exist from a prior session — if so, update rather than overwrite). If it doesn't exist, the Read attempt satisfies the read-before-write guard.
3. Write decision file at `{{cookiecutter.project_slug}}/decisions/{slug}.md`

```yaml
---
type: decision
title: {title}
status: locked
date: {YYYY-MM-DD}
session: "[[sessions/session-{N}]]"
supersedes: {only if applicable, otherwise omit}
tags: [decision]
---

# {Title}

{Free-form: rationale, context, alternatives — whatever's relevant}
```

Skip this step if no new LOCKED decisions.

### Step 5: Inbox Capture

Review the session for ideas, issues, or future work that surfaced but weren't acted on. Append each as a bullet to `{{cookiecutter.project_slug}}/inbox.md`:

```markdown
- {idea description} — {brief context, session reference}
```

These are raw captures — no appetite tags, no formatting beyond a plain bullet. Read the file first, then append new items after the existing content.

Skip if nothing new to capture.

### Step 6: Update State

Read and update `{{cookiecutter.project_slug}}/state.md`:

1. Update frontmatter:
   - `current_session`: N (current session number)
   - `updated`: today's date
   - `last_session`: "[[sessions/session-{N}]]"
   - `active_plan`: update if plan status changed
   - `focus`: Next session's focus (1 line, from Next Steps)
   - `plan_summary`: Current plan summary (1 line) or empty

2. Update lifecycle sections:

   - **Completed items:** Remove the bullet line from state.md entirely. The session handoff file is the historical record — no need to keep done items in state.md.

   - **Items still in progress:** Keep in `## Active`. If the item is partially done, append a sub-phase note in parentheses:
     ```markdown
     - Implement PM lifecycle [large] → [[plans/pm-lifecycle]] (Phase 1 done, starting Phase 2)
     ```

   - **New items shaped during session:** Add to `## Shaped` with appetite tag and one-line approach:
     ```markdown
     - {description} [{appetite}] — {approach}
     ```

   - **Items explicitly parked:** Move to `## Parked` with a reason:
     ```markdown
     - {description} — parked: {reason}
     ```

   - **Constraints**: Add links to new decisions.

**Note:** state.md stays lean. Rich context lives in the session handoff, which `/begin` also reads.

### Step 7: Create Session Note

Create session handoff at `{{cookiecutter.project_slug}}/sessions/session-{N}.md`:

```yaml
---
type: session
session: {N}
date: {YYYY-MM-DD}
mode: {brainstorm | build | direct}
topics: [topic1, topic2]
outcome: successful | blocked | abandoned
continues_from: "[[sessions/session-{N-1}]]"
decisions: ["[[decisions/slug]]"]
---

# Session {N}: {Title}

## Context
{What we worked on - 2-3 sentences}

## Decisions

### Locked
- {decision} — {rationale}

### Open
- {question}

## Memory
- {fact to persist}

## Next Steps
- **Active continuing:** {items still in Active, note sub-phase if applicable}
- **Shaped for next session:** {items in Shaped recommended to pull into Active}
- **Inbox captured:** {count of items added to inbox, or "none"}
```

**Outcome guidelines:**
- `successful` = goals achieved, clear progress
- `blocked` = stuck, needs resolution
- `abandoned` = scope changed, work discarded

### Step 8: Reset Scratch

{{cookiecutter.project_slug}}/scratch.md was already read in Step 1, so the read-before-write guard is satisfied. Reset it for next session:

```markdown
# Scratch — Session {N+1}

Session objective: [TBD]
```

### Step 9: Living CLAUDE.md Review

Review session for patterns that should persist in CLAUDE.md:

**Look for:**
- Repeated corrections ("I said X, not Y" multiple times)
- Expressed preferences ("always do X", "never do Y")
- Workflow improvements
- Anti-patterns that caused friction

If patterns found, present to user:
```
## CLAUDE.md Candidates

I noticed these patterns that might be worth adding:

1. **{pattern}** — {why it matters}

Add to CLAUDE.md?
```

Skip if no patterns or user declines.

### Step 10: Git Commit

Invoking `/wrap` signals approval to commit:

```bash
git status
git add -A
git commit -m "Session {N}: {brief summary}"
```

Skip if no changes. Report hash in confirmation.

**Note:** All vault files are now git-tracked since they're inside the project.

### Step 11: Confirm Completion

```
## Session {N} Wrap-up Complete

| Document | Action |
|----------|--------|
| {{cookiecutter.project_slug}}/state.md | Updated: completed items removed, active items updated |
| {{cookiecutter.project_slug}}/inbox.md | {Appended N items / No new captures} |
| {{cookiecutter.project_slug}}/decisions/ | {Created N files / No new decisions} |
| {{cookiecutter.project_slug}}/sessions/session-{N}.md | Created with handoff |
| {{cookiecutter.project_slug}}/scratch.md | Reset for session {N+1} |
| CLAUDE.md | {Updated / No changes} |

**Topics:** {topics}
**Outcome:** {outcome}

**Next Steps:**
- **Active continuing:** {items and sub-phase}
- **Shaped for next:** {recommended items}
- **Inbox:** {count of new captures}

**Git:** {committed (hash) / no changes}

Transcript will export automatically when session ends.
Use `/begin` in next session to resume.
```
