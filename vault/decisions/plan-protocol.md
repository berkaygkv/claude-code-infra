---
type: decision
title: "Plan protocol — standard format and lifecycle"
status: locked
date: 2026-02-13
session: "[[sessions/session-36]]"
tags: [decision]
---

# Plan Protocol

Plans are the bridge between brainstorm and build. Every plan follows a standard format so build mode can consume them without guessing.

## Format

**Frontmatter:** `type`, `title`, `status` (draft→active→completed|abandoned), `date`, `session`, `phases_total`, `phases_done`.

**Body (four sections, this order):**
1. Goal — what and why, 3 sentences max
2. Scope — includes / excludes
3. Phases — numbered, ordered, each with name + description + task checkboxes + deliverables
4. Decisions — wikilinks to LOCKED decisions the plan depends on

## Lifecycle

- `draft` — written during brainstorm, not yet approved
- `active` — user approved, build mode executes
- `completed` — all phases done
- `abandoned` — killed, file stays as history

## Threshold

Dependent phases or multi-session work → plan. Single-session independent tasks → just do them.

## Phase sizing

Each phase should complete in one session. If it won't fit, break it down.

## Where it lives

Creation protocol in `protocols/brainstorm.md`. Consumption protocol in `protocols/build.md`.

## Parked

Amendment protocol — deviation handling in build.md covers the spirit for now. Formalize if friction appears.
