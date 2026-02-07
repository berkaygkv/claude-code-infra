---
type: schema
created: 2025-02-05
---

# Vault Schemas

Canonical schema definitions for all vault file types. Dashboard queries and `/wrap` command must follow these specifications.

---

## State (`vault/state.md`)

Single file. Tracks current session state.

### Frontmatter

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | yes | Always `state` |
| `project` | string | yes | Project name |
| `phase` | string | yes | Current phase: `idle`, `brainstorm`, `build` |
| `current_session` | number | yes | Current session number |
| `updated` | date | yes | Last update date (YYYY-MM-DD) |
| `last_session` | wikilink | yes | Link to last session file |
| `active_plan` | wikilink | no | Link to current plan file |
| `focus` | string | yes | Current focus (1 line) |
| `plan_summary` | string | no | Current plan summary (1 line) |

### Content

```markdown
# State

## Tasks
- [ ] Task description #pending
- [ ] Task description #blocked/task-id
- [x] Completed task #done

## Constraints
- [[decisions/decision-slug]] — description

## Open Design Work
| Item | Notes |
|------|-------|
| ... | ... |
```

### Task Format

Tasks use Obsidian checkbox format for Dataview compatibility:
- `- [ ] Task #pending` — not started
- `- [ ] Task #blocked/other-task` — blocked by another task
- `- [/] Task #in-progress` — in progress
- `- [x] Task #done` — completed

---

## Session (`vault/sessions/session-{N}.md`)

One file per session. Handoff context for cold start.

### Frontmatter

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | yes | Always `session` |
| `session` | number | yes | Session number |
| `date` | date | yes | Session date (YYYY-MM-DD) |
| `mode` | string | yes | Mode: `brainstorm`, `build`, `quick-fix` |
| `topics` | list | yes | Topics covered |
| `outcome` | string | yes | `successful`, `blocked`, `abandoned` |
| `continues_from` | wikilink | no | Link to previous session |
| `decisions` | list | no | Links to decisions made |

### Content

```markdown
# Session {N}: {Title}

## Context
{What we worked on}

## Decisions
### Locked
- {decision} — {rationale}

### Open
- {question}

## Memory
- {fact to persist}

## Next Steps
1. {action item}
```

---

## Decision (`vault/decisions/{slug}.md`)

One file per decision (or cohesive bundle).

### Frontmatter

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | yes | Always `decision` |
| `title` | string | yes | Decision title |
| `status` | string | yes | `locked`, `superseded` |
| `date` | date | yes | Decision date (YYYY-MM-DD) |
| `session` | wikilink | yes | Link to session where decided |
| `supersedes` | wikilink | no | Link to decision this replaces |
| `superseded_by` | wikilink | no | Link to decision that replaced this |
| `related` | list | no | Links to related decisions |
| `tags` | list | yes | Tags including `decision` |

### Content

```markdown
## Decision
{the decision}

## Rationale
{why we chose this}

## Alternatives Considered
{what we rejected}
```

---

## Plan (`vault/plans/{slug}.md`)

One file per plan.

### Frontmatter

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | yes | Always `plan` |
| `title` | string | yes | Plan title |
| `status` | string | yes | `draft`, `approved`, `in_progress`, `completed`, `abandoned` |
| `created` | date | yes | Creation date (YYYY-MM-DD) |
| `project` | string | yes | Project name |
| `phases_total` | number | yes | Total number of phases |
| `phases_done` | number | yes | Completed phases count |

### Content

```markdown
# {Title}

## Problem Statement
...

## Solution Overview
...

## Implementation Phases

### Phase 1: {Name}
- [ ] Deliverable 1
- [ ] Deliverable 2

### Phase 2: {Name}
...
```

---

## Research Target (`vault/research/targets/TARGET-{timestamp}-{slug}.md`)

Research request before investigation.

### Frontmatter

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | yes | Always `research-target` |
| `status` | string | yes | `open`, `in_progress`, `complete` |
| `created` | date | yes | Creation date (YYYY-MM-DD) |
| `topic` | string | yes | Research topic (short) |
| `confidence` | string | no | `low`, `medium`, `high` (after completion) |
| `output` | wikilink | no | Link to findings (after completion) |

### Content

```markdown
# Research Target: {Topic}

## Question
{What we need to learn}

## Context
{Why this matters}

## Key Areas
1. ...

## Output
{Link to findings once complete}
```

---

## Research Output (`vault/research/{timestamp}-{slug}/findings.md`)

Research results.

### Frontmatter

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | yes | Always `research-output` |
| `target_link` | wikilink | yes | Link back to TARGET |
| `created` | date | yes | Creation date |
| `topic` | string | yes | Research topic |
| `confidence` | string | yes | `low`, `medium`, `high` |

---

## Dashboard Queries Reference

The dashboard expects these exact fields. Any schema changes must update both the file templates AND the dashboard queries.

| Section | Source | Fields Used |
|---------|--------|-------------|
| Current State | `state.md` frontmatter | `phase`, `focus`, `plan_summary` |
| Tasks | `state.md` content | `file.tasks` (checkbox format) |
| Recent Decisions | `decisions/*.md` | `title`, `status`, `date` |
| Session History | `sessions/*.md` | `date`, `outcome`, `topics` |
| Open Research | `research/targets/*.md` | `topic`, `confidence`, `status="open"` |
| Plan Progress | `plans/*.md` | `title`, `status`, `phases_done`, `phases_total` |
