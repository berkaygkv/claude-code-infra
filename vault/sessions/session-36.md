---
type: session
session: 36
date: 2026-02-13
mode: brainstorm
topics: [plan-protocol]
outcome: successful
continues_from: "[[sessions/session-35]]"
decisions: ["[[decisions/plan-protocol]]"]
---

# Session 36: Plan Protocol

## Context
Audited all 5 existing plans and found zero format consistency — different frontmatter fields, different status values, different body structures. Designed and implemented a standard plan protocol: fixed frontmatter schema, four mandatory body sections (Goal, Scope, Phases, Decisions), clear status lifecycle (draft→active→completed|abandoned), and creation/consumption instructions baked into both brainstorm and build protocols.

## Decisions

### Locked
- Plan protocol — standard format (frontmatter + 4 body sections), lifecycle, creation in brainstorm.md, consumption in build.md

### Open
- None

### Parked
- Amendment protocol — deviation handling covers it for now, formalize when friction appears

## Memory
- 5 existing plans in vault/plans/ are all inconsistent — not worth migrating, just follow the new format going forward
- clawbot-coordination.md in plans/ is not actually a plan (it's a Telegram message) — could be moved or left
- Plan protocol is written directly into protocols/brainstorm.md and protocols/build.md, not as a separate file

## Next Steps
1. Mark superseded decisions (vault-io-strategy.md, research-pipeline-v2.md) with `status: superseded`
2. Resume pending verification tasks (hooks, excalidraw, upgrade skill)
3. Implement research format v2 — modify capture-research hook + update CLAUDE.md (do last)
