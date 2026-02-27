---
type: schema
created: 2025-02-05
---

# Vault Schemas

Canonical schema definitions for all vault file types. Dashboard queries and `/wrap` command must follow these specifications.

---

## State (`{{cookiecutter.project_slug}}/state.md`)

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

## Objective
{Project-level anchor — 1-2 sentences describing what we're building and why}

## Active
- {Item} [{appetite}] — {description} ([[plans/{slug}]] if large)

## Shaped
- {Item} [{appetite}] — {description with approach and done-definition}

## Parked
- {Item} — {reason for parking}

## Constraints
- [[decisions/decision-slug]] — description
```

### Task Lifecycle

Items flow through: **Inbox → Shaped → Active → Done/Parked**

- **Inbox** (`{{cookiecutter.project_slug}}/inbox.md`) — raw ideas, append-only
- **Shaped** — has all three gates: appetite + approach + done-definition
- **Active** — WIP-limited: 1 large OR 2 small/chore simultaneously
- **Done** — removed from state.md at `/wrap`; session handoff is the record
- **Parked** — explicitly deprioritized, no SLA

### Appetite Tags

| Tag | Scope | WIP Slot |
|-----|-------|----------|
| `[chore]` | Sub-session | None consumed |
| `[small]` | Single session | 1 slot |
| `[large]` | Multi-session | 1 slot (requires plan file) |

---

## Session (`{{cookiecutter.project_slug}}/sessions/session-{N}.md`)

One file per session. Handoff context for cold start.

### Frontmatter

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | yes | Always `session` |
| `session` | number | yes | Session number |
| `date` | date | yes | Session date (YYYY-MM-DD) |
| `mode` | string | yes | Mode: `brainstorm`, `build`, `direct` |
| `topics` | list | yes | Topics covered |
| `outcome` | string | yes | `successful`, `blocked`, `abandoned` |
| `continues_from` | wikilink | no | Link to previous session |
| `decisions` | list | no | Links to decisions made |

### Content

```markdown
# Session {N}: {Title}

## Context
{Narrative of what was worked on — key outcomes, breakthroughs, blockers}

## Decisions
### Locked
- {decision} — {rationale}
(or prose: "None — {reason}")

### Open
- {question / unresolved item}

## Memory
- {fact to persist across sessions}

## Next Steps
- **Active continuing:** {item} [{appetite}] — {what carries forward}
- **Shaped for next session:** {items available to pick up}
- **Inbox captured:** {items added during session} or "None"
```

---

## Decision (`{{cookiecutter.project_slug}}/decisions/{slug}.md`)

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
| `tags` | list | yes | Tags including `decision` |

### Content

Free-form. No forced body sections — structure the content as the decision demands.

---

## Plan (`{{cookiecutter.project_slug}}/plans/{slug}.md`)

One file per plan.

### Frontmatter

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | yes | Always `plan` |
| `title` | string | yes | Plan title |
| `status` | string | yes | `draft`, `active`, `completed`, `failed` |
| `date` | date | yes | Date (YYYY-MM-DD) |
| `session` | wikilink | no | Link to originating session |
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

## Research (`{{cookiecutter.project_slug}}/research/{YYYYMMDD}-{slug}.md`)

Flat research files with inline sources.

### Frontmatter

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | yes | Always `research` |
| `date` | date | yes | Creation date (YYYY-MM-DD) |
| `topic` | string | yes | Research topic |

### Content

```markdown
# {Topic}

**Question:** {query}

---

## Findings
{content}

---

## Sources
1. [Title](url)
```
