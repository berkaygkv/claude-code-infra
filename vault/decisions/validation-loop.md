---
type: decision
title: "Validation loop — spike assumptions, build from evidence"
status: locked
date: 2026-02-13
session: "[[sessions/session-37]]"
tags: [decision]
---

# Validation Loop

## Problem

The system optimizes for planning rigor but has no empirical feedback loop. Ideas get brainstormed, planned, and built — but never validated against reality until it's expensive to change. Context passed between sessions is built from intentions (what we thought, what we decided), not evidence (what we tested, what we learned). Claude's agreeable nature compounds this — plans look polished but carry unexamined assumptions.

## Decision

Speed is the superpower. Don't out-think the holes — out-build them.

**Core principle:** Build fast, fail fast, improve faster. Spike the riskiest assumption before committing to a full plan. Let validated findings — not brainstorming narratives — drive direction and session context.

**The validation loop (inside build mode):**

1. Identify the riskiest unvalidated assumption in the current phase
2. State it in the plan before building (no retroactive "I knew that")
3. Spike it — smallest possible code that tests the assumption (`spike/{slug}` branch)
4. Record the finding in the plan, next to the assumption
5. Assess impact: task-level (adjust tasks), phase-level (restructure phase), or direction-level (return to brainstorm)
6. Continue or loop

**What changes:**

- **Brainstorm** gets lighter. Its output is: direction, riskiest assumptions, first spike. Not exhaustive plans.
- **Plans** become living documents. Each phase carries assumption → spike → finding → adjusted tasks. Plans accumulate evidence, not just checkmarks.
- **Build mode** gains the validation loop. You validate before you execute, per phase.
- **Session context** is rebuilt from findings. `/begin` loads a plan full of ground truth, not speculation.
- **Git:** Spikes happen on `spike/{slug}` branches. Code is disposable. Findings are permanent.

**What doesn't change:**

- Session lifecycle (`/begin` → work → `/wrap`)
- Vault structure (no new directories or artifact types)
- Decision tracking (LOCKED/OPEN/PARKED)
- Two modes (brainstorm + build)

## Rationale

Emerged from structured debate (3 independent perspectives: staff engineer, product lead, cognitive systems researcher). All three converged on the same insight: behavioral instructions to "be more critical" don't survive contact with the model's base tendencies. Structural intervention is required. The cheapest structural intervention is empirical — test assumptions with code instead of trying to think harder about them.

## Implementation

Protocol changes (brainstorm.md, build.md, plan format) to be designed through manual testing — run the loop by hand for 2-3 sessions, then formalize what works. No protocol rewrites until we have evidence.
