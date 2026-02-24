---
type: session
session: 48
date: 2026-02-24
mode: brainstorm
topics: [collaborative-scratch-surface, project-management-gaps, obsidian-callouts, markup-convention, shared-language]
outcome: successful
continues_from: "[[sessions/session-47]]"
decisions: ["[[decisions/scratch-collab-surface]]"]
---

# Session 48: Design collaborative scratch surface

## Context

Started with a broad question: does the current project management setup properly handle PM? Identified 6 systemic gaps (no shared language, no quality gate for tracked items, nuance decay in handoffs, no idea lifecycle, flat task list, no strategic layer). User added 3 supporting observations: nuance loss is real but manageable, low-quality items pollute state without a gateway, and the biggest gap is communication — no shared vocabulary for intent between sessions.

Mid-session breakthrough: realized the core friction is that chat turns are one-directional — user can't annotate Claude's output inline. Designed a collaborative scratch surface using Obsidian callouts, then dogfooded it immediately during the session (wrote proposals to vault/scratch.md, user annotated in Obsidian). Resolved all design questions and wrote an implementation plan.

## Decisions

### Locked

- **Collaborative scratch surface** — scratch.md moves to `vault/scratch.md`, becomes shared working surface with Obsidian callout convention (4 types: question/warning/tip/info), silence = agree, bidirectional. Supersedes scratch-pad-v2. Reference card at `vault/reference/scratch-convention.md`. Objective lifecycle and rewrite-not-append survive. Decision: `vault/decisions/scratch-collab-surface.md`.

### Open

- **Project management lifecycle** — idea funnel, prioritization, strategic layer. Identified as gaps but not designed yet. Foundation piece (scratch surface) comes first.
- **Shared language / operational glossary** — named operations for precise intent ("stress-test", "weight-check", "distill"). Identified as the root cause of communication drift. Deferred to future brainstorm.
- **Task list restructuring** — flat checklist with no priorities, categories, or archival. Needs design.
- **Quality gate for tracked items** — no weight assessment before things enter state.md. Needs design.

## Memory

- Dogfooded the collaborative scratch surface during the session — user annotated proposals in Obsidian using callouts. Pattern worked well. Low friction, high signal.
- User copied scratch.md to vault/ to open in Obsidian — this motivated the "file must live in vault" decision.
- Root `scratch.md` still exists alongside `vault/scratch.md` — root gets deleted during build.
- `vault/reference/` already exists with `prompt-dictionary.md` — convention card fits there.
- The broader PM discussion (lifecycle, shared language, quality gates, strategic layer) is parked — scratch surface is the foundation piece, others layer on top.
- User explicitly values: the ability to edit/annotate Claude's output, content surviving context compression, and a shared vocabulary for intent.

## Next Steps

1. `/begin build` — execute `vault/plans/scratch-collab-surface.md` (single phase: 7 files updated, 2 created, 1 deleted)
2. After build: brainstorm shared language / operational glossary (root cause of communication drift)
3. After language: brainstorm project management lifecycle (idea funnel, prioritization, strategic layer)
4. Carried: bulk template sync (S42 + S44 + S46 + S47 + S48), test /upgrade on another machine, test excalidraw, Catalyst purchase
