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

**Core principle:** Build fast, inspect output, align on direction, iterate. Spike the riskiest assumption before committing to a full plan. Let validated findings — not brainstorming narratives — drive direction and session context.

**The validation loop (inside build mode):**

1. Identify the riskiest unvalidated assumption in the current phase
2. State it in the plan before building (no retroactive "I knew that")
3. Spike it — smallest possible code that tests the assumption (`spike/{slug}` branch)
4. **Present the output** — show the inspectable artifact to the user (extracted data, graph structure, generated output — whatever the spike produces)
5. **Align** — user reviews and reacts: "on track", "off track", "close but needs X". This is the gate, not a metric.
6. Record the finding as narrative in the plan, next to the assumption
7. Assess impact: task-level (adjust tasks), phase-level (restructure phase), or direction-level (return to brainstorm)
8. Continue or loop

**Validation is qualitative-first.** Building a project is not like training a model. You can't reduce "is this working?" to a number most of the time. The gate is alignment — user inspects output, reacts, provides direction. Metrics (accuracy, counts, performance) may inform the review when they're meaningful, but they are never the sole gate. The question is always: "does this output match what we're trying to build?" — and that's a judgment call.

**What changes:**

- **Brainstorm** gets lighter. Its output is: direction, riskiest assumptions, and what the user will inspect at each spike. Not exhaustive plans with metrics criteria.
- **Plans** become living documents. Each assumption carries: spike design → inspectable output → finding (narrative) → impact. Plans accumulate evidence, not just checkmarks.
- **Build mode** gains the validation loop with an inspect & align checkpoint. You build, present, align, then proceed.
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

Formalized in session 39. Protocol changes applied to brainstorm.md, build.md, and plan-protocol decision based on the insight that project validation is primarily qualitative — inspect and align, not measure and gate.
