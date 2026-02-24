---
type: plan
title: "Implement project management lifecycle"
status: active
date: 2026-02-24
session: "[[sessions/session-50]]"
phases_total: 2
phases_done: 1
---

# Implement Project Management Lifecycle

## Goal

Replace the flat task graveyard in state.md with a structured lifecycle: Inbox → Shaped → Active → Done/Parked. Appetite-gated, WIP-limited, with kill rituals. One concept per gate, zero wallpaper.

## Scope

**Includes:**
- state.md restructure (purge done, new sections)
- vault/inbox.md creation
- /begin updates (filtered display, inbox check)
- /wrap updates (done purge, inbox capture)
- dashboard.md Dataview queries
- Decision file for PM lifecycle
- CLAUDE.md updates (memory architecture, task references)

**Excludes:**
- Strategic themes (deferred — revisit when needed)
- Decay automation (manual for now)
- Template sync (separate chore)
- Scratch communication schema design (inbox item, separate work)
- Obsidian compliance audit (inbox item, separate work)

## Phase 1: Core infrastructure

Restructure state.md, create inbox, update operational commands.

### Tasks

- [x] Create `vault/decisions/pm-lifecycle.md` — lock the design
- [x] Restructure `vault/state.md`:
  - [x] Purge all `#done` items (45 items → session handoffs are the record)
  - [x] Batch 5 sync chores into one: "Batch template sync (S42–S49)"
  - [x] New sections: `## Objective` / `## Active` / `## Shaped` / `## Parked` / `## Constraints`
  - [x] Each item carries appetite tag: `[chore]` / `[small]` / `[large]`
- [x] Create `vault/inbox.md` — append-only capture point
- [x] Update `.claude/commands/begin.md`:
  - [x] Read only Active + Shaped sections (not full graveyard)
  - [x] Check inbox item count → surface if > 5: "Inbox has N items. Triage now or defer?"
  - [x] Active items from prior session shown as "Continuing"
- [x] Update `.claude/commands/wrap.md`:
  - [x] Remove completed items from state.md (don't just check them off)
  - [x] Append new ideas surfaced during session to vault/inbox.md
  - [x] Items staying Active → keep in Active, note sub-phase
- [x] Update `CLAUDE.md`:
  - [x] Memory Architecture table: add inbox.md row
  - [x] Describe lifecycle stages and appetite gating
  - [x] Update task-related references to match new state.md format
  - [x] Add mid-session inbox capture instruction
- [x] Verify: no stale `## Tasks` references remain in operational files

### Deliverables

- state.md restructured (5 sections, ~15 items max, zero done items)
- vault/inbox.md live with 2 items from this session
- /begin and /wrap working with new format
- Decision file locked

## Phase 2: Dashboard & observability

Update user-facing Obsidian views for the new structure.

### Tasks

- [ ] Update `vault/dashboard.md`:
  - [ ] Active items query (from state.md `## Active` section)
  - [ ] Shaped items query (from state.md `## Shaped` section)
  - [ ] Inbox count / recent items
  - [ ] Parked items (collapsed or separate section)
- [ ] Create `vault/reference/triage-criteria.md` — read silently at /begin:
  - [ ] Appetite sizing definitions (chore / small / large)
  - [ ] Shaping checklist (appetite + approach + done-def)
  - [ ] Kill ritual triggers
  - [ ] Chore exception rule (sub-session = no WIP slot)
- [ ] Verify Dataview queries render correctly in Obsidian

### Deliverables

- Dashboard shows Active, Shaped, Inbox, Parked as distinct views
- Triage reference card available for cold-start awareness
- All Dataview queries functional

## Decisions

- [[decisions/pm-lifecycle]] (to be created in Phase 1)
- Depends on: [[decisions/scratch-collab-surface]] (scratch surface is the collaboration medium)
- Informed by: [[decisions/io-strategy-v2]] (native Read for known paths, MCP for discovery)
