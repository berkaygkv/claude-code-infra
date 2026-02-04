# Session Wrap-up Command

End-of-session tasks: process scratch.md, update state.md, create session handoff, create decision files.

## Design Rationale

**I/O Strategy:**
- Native Read/Write for all content operations
- MCP only for metadata operations if needed (frontmatter-only updates, search, tags)

**Documents updated:**
- `vault/state.md` — Current state, tasks, context
- `vault/decisions/*.md` — New LOCKED decisions (created)
- `vault/sessions/session-{N}.md` — Session handoff note (created)
- `scratch.md` — Reset for next session

## Paths

All paths relative to project root:

- Vault: `vault/`
- State: `vault/state.md`
- Sessions: `vault/sessions/session-{N}.md`
- Transcripts: `vault/sessions/transcripts/session-{N}.md`
- Decisions: `vault/decisions/`
- Scratch: `scratch.md`

## Instructions

When the user invokes `/wrap`, perform these steps:

### Step 1: Read Session Scratch

Read `scratch.md` using native Read.

Extract:
- **Session number** from Meta section
- **Decisions** (LOCKED and OPEN items)
- **Memory** items to persist
- **Tasks** (new, completed, blockers)
- **Notes** (additional context)

If scratch.md is empty, synthesize from conversation context.

### Step 2: Determine Session Number

If session number is in scratch.md, use that.

Otherwise, read vault/state.md to get current_session, use that.

### Step 3: Synthesize Session Work

Combine scratch.md content with conversation context:
- What tasks were completed?
- What decisions were made (LOCKED vs OPEN)?
- What new tasks or blockers emerged?
- What is the current phase and next action?
- What should the next session start with?
- What are the key topics/themes?

### Step 4: Create Decision Files

For each LOCKED decision in scratch.md:

1. Generate slug from decision title (lowercase, hyphens)
2. Create decision file at `vault/decisions/{slug}.md`

```yaml
---
type: decision
title: {title}
status: locked
date: {YYYY-MM-DD}
session: "[[sessions/session-{N}]]"
supersedes: null
superseded_by: null
related: []
tags:
  - decision
---

## Decision
{the decision}

## Rationale
{why we chose this}

## Alternatives Considered
{what we rejected, if any}
```

Skip this step if no new LOCKED decisions.

### Step 5: Update State

Read and update `vault/state.md`:

1. Update frontmatter:
   - `current_session`: N (current session number)
   - `updated`: today's date
   - `last_session`: "[[sessions/session-{N}]]"
   - `active_plan`: update if plan status changed

2. Update content:
   - **Focus**: Next session's focus (first item from Next Steps)
   - **Plan**: Current plan summary or "None"
   - **Tasks**: Update task table (completed → done, new tasks added)
   - **Constraints**: Add links to new decisions

**Note:** state.md stays lean. Rich context lives in the session handoff, which `/begin` also reads.

### Step 6: Create Session Note

Create session handoff at `vault/sessions/session-{N}.md`:

```yaml
---
type: session
session: {N}
date: {YYYY-MM-DD}
project: {{ cookiecutter.project_slug }}
topics: [topic1, topic2]
outcome: successful | blocked | abandoned
continues_from: "[[sessions/session-{N-1}]]"
transcript: "[[sessions/transcripts/session-{N}]]"
decisions: ["[[decisions/slug]]"]
research_spawned: []
tags:
  - session
---

## Handoff

### Context
{What we worked on - 2-3 sentences}

### Decisions
{LOCKED and OPEN decisions from this session}

### Memory
{Facts to persist across sessions}

### Next Steps
{Actionable items for next session}
```

**Outcome guidelines:**
- `successful` = goals achieved, clear progress
- `blocked` = stuck, needs resolution
- `abandoned` = scope changed, work discarded

### Step 7: Reset Scratch

Reset scratch.md for next session:

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

### Step 8: Living CLAUDE.md Review

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

### Step 9: Git Commit

Invoking `/wrap` signals approval to commit:

```bash
git status
git add -A
git commit -m "Session {N}: {brief summary}"
```

Skip if no changes. Report hash in confirmation.

**Note:** All vault files are now git-tracked since they're inside the project.

### Step 10: Confirm Completion

```
## Session {N} Wrap-up Complete

| Document | Action |
|----------|--------|
| vault/state.md | Updated: phase={phase}, tasks updated |
| vault/decisions/ | {Created N files / No new decisions} |
| vault/sessions/session-{N}.md | Created with handoff |
| scratch.md | Reset for session {N+1} |
| CLAUDE.md | {Updated / No changes} |

**Topics:** {topics}
**Outcome:** {outcome}

**Next Steps:**
1. {first next step}
2. {second next step}

**Git:** {committed (hash) / no changes}

Transcript will export automatically when session ends.
Use `/begin` in next session to resume.
```
