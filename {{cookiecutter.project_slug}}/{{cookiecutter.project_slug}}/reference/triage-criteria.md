---
type: reference
title: "Triage Criteria"
date: 2026-02-24
decision: "[[decisions/pm-lifecycle]]"
---

# Triage Criteria

Quick reference for PM lifecycle gating — appetite sizing, shaping gates, kill triggers.

## Appetite Sizing

| Tag | Scope | WIP Slot | Notes |
|-----|-------|----------|-------|
| `[chore]` | Sub-session | None consumed | Mechanical, low-risk. Runs alongside other work. |
| `[small]` | Single session | 1 slot | — |
| `[large]` | Multi-session | 1 slot | ==Requires plan file in `{{cookiecutter.project_slug}}/plans/`.== |

**WIP limit:** 1 large OR 2 small/chore simultaneously.

## Shaping Checklist (Inbox → Shaped)

Item is shaped when it has **all three:**

- [ ] **Appetite** — chore / small / large
- [ ] **Approach** — how (not a full plan, but enough to start)
- [ ] **Done-definition** — what "done" looks like

Missing any one → stays in inbox.

## Kill Ritual Triggers

| Signal | Action |
|--------|--------|
| Same failure pattern after 3 iterations | Structural problem — escalate to brainstorm mode |
| Scope change / new requirement mid-build | Stop — return to plan mode |
| Large item fails | Back to inbox or parked, with failure narrative in session handoff |

## Chore Exception Rule

- No WIP slot consumed — can run alongside a large or small item
- ==Still needs shaping== (appetite + approach + done-def) but the bar is lower
- Sub-session scope — if it grows, re-tag it

## Conventional Commits Reference

Our `[chore]` appetite tag borrows from the **Conventional Commits** taxonomy — same spirit (mechanical, low-risk housekeeping), different context (task sizing vs. commit categorization).

| Prefix | Meaning |
|--------|---------|
| `feat` | New feature (user-facing) |
| `fix` | Bug fix |
| `chore` | Maintenance, no user-visible change |
| `refactor` | Code restructure, same behavior |
| `docs` | Documentation only |
| `style` | Formatting, whitespace, semicolons |
| `test` | Adding/fixing tests |
| `ci` | CI/CD pipeline changes |
| `perf` | Performance improvement |
| `build` | Build system or dependency changes |
