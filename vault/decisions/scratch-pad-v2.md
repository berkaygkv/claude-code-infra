---
type: decision
title: "Scratch Pad v2 — Reasoning Surface"
status: superseded
date: 2026-02-23
session: "[[sessions/session-44]]"
supersedes_partial: "L2 from [[decisions/system-overhaul-v1]]"
tags: [decision]
---

# Scratch Pad v2 — Reasoning Surface

Redesign scratch.md from a session changelog (append-only event log) to an actively maintained reasoning document. The changelog format was redundant with session handoffs and didn't force thinking quality. The real gap: state.md captures *what* (tasks, decisions, constraints) but nothing captures *why* (reasoning, rejected alternatives, active thinking context). That reasoning dies when chat scrolls away or context compresses.

## Design

**Three-layer context onion:**
- `state.md` § Objective — project-wide anchor, rarely changes
- `scratch.md` header — session objective with `[TBD]`/`[LOCKED]` lifecycle
- `scratch.md` § Problem — current thinking thread, actively maintained

**Format:** Plain bullets under a Problem anchor section. No tags, no sections, no structure beyond the Problem statement and flat reasoning entries.

**Objective lifecycle:** Starts `[TBD]` at `/begin`. Locks (`[LOCKED] {objective}`) once session direction aligns through conversation. Problem section written after lock. On mid-session pivot, user signals and Problem section is rewritten.

**Maintenance protocol:** Rewrite, don't append. Remove resolved items. Keep only what's live. Filter: "Would losing this reasoning to scroll-away hurt the rest of the session?"

**What changed:** CLAUDE.md, begin.md, wrap.md, brainstorm.md, build.md, meta.md all updated. state.md gained § Objective section.

## Rejected alternatives
- scratch.md as live dashboard (duplicates state.md)
- Flat tagged list with DECISION/INSIGHT/OPEN/REJECTED tags (append-only log in disguise, tags overlap with state.md categories)
- Killing scratch.md entirely (loses the forcing function for thinking quality and the scroll-away survival)
