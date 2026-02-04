# Session Begin Command

This command loads context from state.md and activates the specified mode.

## Usage

```
/begin              → Quick fix mode (minimal protocols)
/begin brainstorm   → Brainstorm mode (alignment before action)
/begin build        → Build mode (ship artifacts)
```

## Paths

All paths relative to kh directory:

- Vault: `vault/`
- State: `vault/state.md`
- Sessions: `vault/sessions/session-{N}.md`
- Decisions: `vault/decisions/`
- Plans: `vault/plans/`
- Scratch: `scratch.md`

## Mode Protocol

!`scripts/load-protocol.sh $ARGUMENTS`

---

## Instructions

When the user invokes `/begin [mode]`, perform these steps:

### Step 1: Read State

Read `vault/state.md` using native Read.

Extract from frontmatter:
- `phase` — current mode (brainstorm/build/idle)
- `current_session` — session number
- `last_session` — link to previous session
- `active_plan` — current plan if any

Extract from content:
- Focus — what we're working on
- Plan — current plan summary
- Tasks — active tasks table
- Constraints — linked decisions to honor
- Context — background information

### Step 2: Handle First Run

If state.md doesn't exist or is empty:
- Create state.md with session: 1
- Display first-run welcome
- Skip to Step 5

**First-run welcome:**
```
## Session 1 (First Run)

Welcome to kh. No previous sessions found.

**Vault:** vault/

This is a fresh installation. The following are ready:
- vault/state.md — session state
- vault/dashboard.md — Dataview queries
- vault/decisions/ — committed decisions
- vault/sessions/ — session handoffs

Ready to begin. What are we working on?
```

### Step 3: Acknowledge Mode

State which mode is active:
- No argument → "Quick fix mode — minimal overhead, direct execution"
- `brainstorm` → "Brainstorm mode — alignment before action"
- `build` → "Build mode — executing approved plan"

### Step 4: Display Current State

```
## Resuming Session {N+1}

**Phase:** {phase}
**Focus:** {focus}
**Plan:** {plan or "none"}

### Active Tasks
{tasks from state.md or "none"}

### Constraints
{constraints from state.md or "none"}

### Context
{context from state.md}
```

### Step 5: Mode-Specific Prompt

**Quick fix mode (no argument):**
```
Ready. What needs fixing?
```

**Brainstorm mode:**
```
Ready to brainstorm. What are we thinking through?
```

**Build mode:**
If `active_plan` exists, read the plan file and display:
```
Ready to build.

**Active Plan:** {plan name}
**Current Phase:** {next incomplete phase}

Confirm to proceed.
```

If no active plan:
```
Build mode requested but no active plan found.
Switch to brainstorm mode to create a plan, or specify what to build.
```

### Step 6: Confirm Session Start

After user responds:
```
Session {N+1} started. [{mode} mode]
```

## Notes

- vault/state.md is the ONLY file read for cold start (minimal token overhead)
- If previous session was blocked, the Context section should highlight the blocker
- Mode protocols are in `protocols/` — edit those files to change cognitive behavior
- scratch.md is prepared by `/wrap` at end of each session
