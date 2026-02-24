---
type: decision
title: "Project management lifecycle"
status: locked
date: 2026-02-24
session: "[[sessions/session-50]]"
tags: [decision]
---

# Project Management Lifecycle

Replace the flat task list in state.md with a Shape Up-inspired lifecycle: Inbox → Shaped → Active → Done/Parked. Introduces appetite tags, WIP limits, and explicit gating rules.

## Why

The flat task list in state.md grew to 45+ done items with zero signal. No distinction between "ready to build" and "half-baked idea." No WIP discipline. Cold starts wasted time parsing a graveyard of completed work that served no ongoing purpose.

## Design

**Core Lifecycle:** Inbox → Shaped → Active → Done/Parked

### Stages

**Inbox** (`vault/inbox.md`) — Append-only capture point. Raw ideas, no formatting required. Triage threshold: surface at /begin when count > 5.

**Shaped** — Item has three things: appetite tag, approach (how), and done-definition (what "done" looks like). Lives in state.md `## Shaped` section. Ready to pick up.

**Active** — Currently being worked on. Lives in state.md `## Active` section. WIP limit: 1 large OR 2 small/chore simultaneously. Large items require a plan file in `vault/plans/`.

**Done** — Removed from state.md entirely. Session handoffs in `vault/sessions/` are the historical record. No graveyard.

**Parked** — Explicitly deprioritized. Lives in state.md `## Parked` section. No SLA. Review when relevant context surfaces.

### Appetite Tags

- `[chore]` — Sub-session. No WIP slot consumed. Mechanical, low-risk.
- `[small]` — Single session. One WIP slot.
- `[large]` — Multi-session. Requires plan file. One WIP slot.

### Gating Rules

- **Inbox → Shaped:** Must define appetite + approach + done-definition.
- **Shaped → Active:** Must have WIP capacity. Large items need a plan file.
- **Active → Done:** Remove from state.md. /wrap handles this.
- **Active → Parked:** Explicit decision. Note why in session handoff.
- **Failed large item:** Goes back to inbox or parked, with failure narrative in session handoff.

### State.md Sections

`## Objective` / `## Active` / `## Shaped` / `## Parked` / `## Constraints`

### Operational Integration

- `/begin` reads Active + Shaped (not full graveyard), checks inbox count.
- `/wrap` removes completed items, appends new ideas to inbox.
- Mid-session: append raw ideas to inbox anytime.

## Explicitly Deferred

- Strategic themes layer (revisit when needed)
- Decay/staleness automation (manual review for now)
- Automatic inbox triage prompts beyond count threshold

## Rejected alternatives

- Full graveyard in state.md — the whole problem. 45+ done items, zero signal, cold-start tax on every session.
- Kanban board / external tool — adds a dependency and breaks the vault-native constraint. Markdown files are the system.
- No WIP limits — without constraints, everything becomes "active" and nothing finishes. Shape Up's fixed appetite is the discipline mechanism.
- Automatic staleness decay — premature automation. Manual review is fine until the shaped queue actually grows large enough to warrant it.
