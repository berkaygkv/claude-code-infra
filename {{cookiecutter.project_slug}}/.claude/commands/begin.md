# Session Begin Command

This command loads context from the previous session and activates the specified mode.

## Usage

```
/begin              → Quick fix mode (minimal protocols)
/begin brainstorm   → Plan mode (alignment before action)
/begin build        → Execution mode (ship artifacts)
```

## Paths

- Session notes: `vault/Sessions/session-{N}.md`
- Runbook: `vault/runbook.md`
- Locked decisions: `vault/locked.md`
- Plans: `vault/plans/`
- Scratch: `scratch.md`

## Mode Protocol

!`scripts/load-protocol.sh $ARGUMENTS`

---

## Session Context

Last session: !`scripts/last-session.sh`

## Instructions

When the user invokes `/begin [mode]`, perform these steps:

### Step 1: Acknowledge Mode

State which mode is active:
- No argument → "Quick fix mode — minimal overhead, direct execution"
- `brainstorm` → "Brainstorm mode — alignment before action"
- `build` → "Build mode — executing approved plan"

### Step 2: Check for First Run

If last-session.sh returns "FIRST_RUN":
- Skip Steps 3-4 (no previous session to load)
- Initialize scratch.md with session: 1
- Display first-run welcome (see Step 2a)
- Continue from Step 5

### Step 2a: First-Run Welcome

Display:

```
## Session 1 (First Run)

Welcome to {{ cookiecutter.project_name }}. No previous sessions found.

**Vault:** vault/

This is a fresh installation. The following files are ready:
- locked.md — for committed decisions
- runbook.md — for task tracking
- overview.md — for project state

Ready to begin. What are we working on?
```

Then skip to Step 7 (confirm session start).

### Step 3: Read Previous Session Handoff

Use native Read for the session note:
- Path: `vault/Sessions/session-{N}.md`

### Step 4: Display Handoff Context

```
## Resuming from Session {N}

**Date:** {date}
**Topics:** {topics}
**Outcome:** {outcome}

### Context
{context from handoff}

### Decisions
{decisions from handoff}

### Memory
{memory from handoff}

### Next Steps
{next steps from handoff}
```

### Step 5: Read Operational State

Load current state (use native Read):
- `vault/runbook.md` — tasks, knowledge gaps, blockers
- `vault/locked.md` — committed decisions/constraints

### Step 6: Summarize Current State

```
## Current State

**Phase:** {from runbook frontmatter}
**Blockers:** {from runbook frontmatter, or "none"}

**Active Tasks:**
{incomplete tasks from runbook Active section}

**Knowledge Gaps:**
{from runbook Knowledge Gaps table, or "None"}
```

Note: locked.md is read for Claude's context but not displayed.

### Step 7: Mode-Specific Prompt

**Quick fix mode (no argument):**
```
Ready. What needs fixing?
```

**Brainstorm mode:**
```
Ready to brainstorm. What are we thinking through?

Suggested (from previous session):
- {first next step}
- {second next step}
```

**Build mode:**
Additionally, read the active plan file if one exists:
- Check runbook for active plan reference, or
- List `vault/plans/` for in-progress plans

```
Ready to build.

**Active Plan:** {plan name or "none"}
**Current Phase:** {phase number and name}

Continuing from where we left off. Confirm to proceed.
```

### Step 8: Confirm Session Start

After user responds:
```
Session {N+1} started. [{mode} mode]
```

## Notes

- If previous session outcome was `blocked`, highlight the blocker prominently
- scratch.md is prepared by `/wrap` at the end of each session
- Mode protocols are loaded from `protocols/` — edit those files to change cognitive behavior
