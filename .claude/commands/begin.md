# Session Begin Command

This command loads context from the previous session and activates the specified mode.

## Usage

```
/begin              → Quick fix mode (minimal protocols)
/begin brainstorm   → Plan mode (alignment before action)
/begin build        → Execution mode (ship artifacts)
```

## Mode Protocol

!`/home/berkaygkv/Dev/headquarter/kh/scripts/load-protocol.sh $ARGUMENTS`

---

## Session Context

Last session: !`/home/berkaygkv/Dev/headquarter/kh/scripts/last-session.sh`

## Instructions

When the user invokes `/begin [mode]`, perform these steps:

### Step 1: Acknowledge Mode

State which mode is active:
- No argument → "Quick fix mode — minimal overhead, direct execution"
- `brainstorm` → "Brainstorm mode — alignment before action"
- `build` → "Build mode — executing approved plan"

### Step 2: Read Previous Session Handoff

Use native Read for the session note:
- Path: `/home/berkaygkv/Dev/Docs/.obs-vault/notes/Sessions/session-{N}.md`

### Step 3: Display Handoff Context

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

### Step 4: Read Operational State

Load current state (use native Read):
- `/home/berkaygkv/Dev/Docs/.obs-vault/notes/runbook.md` — tasks, knowledge gaps, blockers
- `/home/berkaygkv/Dev/Docs/.obs-vault/notes/locked.md` — committed decisions/constraints

### Step 5: Summarize Current State

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

### Step 6: Mode-Specific Prompt

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
- List `/home/berkaygkv/Dev/Docs/.obs-vault/notes/plans/` for in-progress plans

```
Ready to build.

**Active Plan:** {plan name or "none"}
**Current Phase:** {phase number and name}

Continuing from where we left off. Confirm to proceed.
```

### Step 7: Confirm Session Start

After user responds:
```
Session {N+1} started. [{mode} mode]
```

## Notes

- If no previous session exists, offer to start fresh (session 1)
- If previous session outcome was `blocked`, highlight the blocker prominently
- scratch.md is prepared by `/wrap` at the end of each session
- Mode protocols are loaded from `kh/protocols/` — edit those files to change cognitive behavior
