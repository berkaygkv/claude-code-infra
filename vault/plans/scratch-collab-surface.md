---
type: plan
title: "Implement collaborative scratch surface"
status: active
date: 2026-02-24
session: "[[sessions/session-48]]"
phases_total: 1
phases_done: 0
---

# Implement Collaborative Scratch Surface

## Goal

Move scratch.md from project root to vault/, evolve it from a Claude-only reasoning surface to a shared working surface with Obsidian callout annotations, and update every file that references it. One session of work.

## Scope

**Includes:**
- New reference card (`vault/reference/scratch-convention.md`)
- New decision file (`vault/decisions/scratch-collab-surface.md`)
- CLAUDE.md updates (5 locations)
- begin.md updates (2 locations)
- wrap.md updates (5 locations)
- brainstorm.md updates (2 locations)
- build.md update (1 location)
- Delete root scratch.md

**Excludes:**
- Template sync (batched with S42/S44/S46/S47 syncs)
- Build mode protocol changes (path update only)
- Project management lifecycle design (separate brainstorm topic)
- Shared language / glossary design (separate brainstorm topic)

## Phase 1: Implement all changes

Single phase — all changes are independent enough to execute in sequence within one session.

### Tasks

- [ ] Create `vault/reference/scratch-convention.md` — the reference card
- [ ] Create `vault/decisions/scratch-collab-surface.md` — decision file, supersedes scratch-pad-v2
- [ ] Update `vault/decisions/scratch-pad-v2.md` — set `status: superseded`
- [ ] Update CLAUDE.md — 5 locations:
  - [ ] Section 3 vault table: add scratch.md row
  - [ ] Section 3 Scratch Pad subsection: full rewrite (path, framing, convention reference)
  - [ ] Section 7 line 148: remove `scratch.md` from main branch file list
  - [ ] Section 7 line 177: remove `scratch.md` from "What NOT to sync"
  - [ ] Section 9 Key Paths: `scratch.md` → `vault/scratch.md`
- [ ] Update begin.md — 2 locations:
  - [ ] Step 2: path to `vault/scratch.md`, add convention read instruction
  - [ ] "Maintaining scratch.md": rewrite for shared surface (both parties write, "ready for marks" / "read it" protocol, Decided section on-demand, 3+ point threshold)
- [ ] Update wrap.md — 5 locations:
  - [ ] Paths section: `vault/scratch.md`
  - [ ] Documents updated: `vault/scratch.md`
  - [ ] Step 1: path + add note about Decided section and callouts in synthesis
  - [ ] Step 7: reset path
  - [ ] Step 10: confirmation table path
- [ ] Update brainstorm.md — 2 locations:
  - [ ] Writes Allowed: `vault/scratch.md`
  - [ ] Drive to Consensus: add sub-point about scratch surface for multi-point proposals
- [ ] Update build.md — 1 location:
  - [ ] Writes Allowed: `vault/scratch.md`
- [ ] Delete root `scratch.md`
- [ ] Verify: read all updated files, confirm no stale `scratch.md` references remain

### Deliverables

- All 7 existing files updated with correct paths and new instructions
- 2 new files created (reference card + decision)
- 1 old decision marked superseded
- Root scratch.md deleted
- Zero remaining references to root `scratch.md` in the codebase

## Decisions

- [[decisions/scratch-collab-surface]] (to be created in this plan)
- Supersedes [[decisions/scratch-pad-v2]]
