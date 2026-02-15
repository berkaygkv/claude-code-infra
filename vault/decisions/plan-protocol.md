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

**Frontmatter:** `type`, `title`, `status` (draft→active→completed|abandoned), `date`, `session`, `phases_total`, `phases_done`. Optional: `assumptions_total`, `assumptions_validated` (for plans with assumptions to validate).

**Body (five sections, this order):**
1. Goal — what and why, 3 sentences max
2. Scope — includes / excludes
3. Assumptions _(optional, for plans with unknowns)_ — each assumption has:
   - **ID + statement + risk level** (e.g., "A1: Entity resolution works — CRITICAL")
   - **Spike** — what to build to test it
   - **Inspectable output** — the concrete artifact the user will see and react to (not a metric, but the actual output: extracted entities, generated graph, API response, etc.)
   - **Findings** — narrative log, each entry tagged with session. Appended on each iteration attempt. ("extraction captures X well, misses Y, merge handles Z but not W")
   - **Impact** — task / phase / direction level, populated after spike
4. Phases — numbered, ordered, each with name + description + task checkboxes + deliverables. Spike phases reference which assumptions they target.
5. Decisions — wikilinks to LOCKED decisions the plan depends on

**Findings are narrative, not numeric.** The question is "does this output match what we're trying to build?" — answered by user inspection, not a score.

## Lifecycle

- `draft` — written during brainstorm, not yet approved
- `active` — user approved, build mode executes
- `completed` — all phases done
- `failed` — approach didn't work, findings preserved as evidence
- `abandoned` — killed before execution, file stays as history

## Threshold

Dependent phases or multi-session work → plan. Single-session independent tasks → just do them.

## Phase sizing

Each phase should complete in one session. If it won't fit, break it down.

## Where it lives

Creation protocol in `protocols/brainstorm.md`. Consumption protocol in `protocols/build.md`.

## Parked

Amendment protocol — deviation handling in build.md covers the spirit for now. Formalize if friction appears.
