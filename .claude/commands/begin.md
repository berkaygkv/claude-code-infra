# Session Begin Command

This command loads context from state.md + last session handoff and activates the specified mode.

## Schema Reference

**IMPORTANT:** All files follow `vault/schemas.md`. Reference it for field definitions.

## Usage

```
/begin              → Quick fix mode (minimal protocols)
/begin brainstorm   → Brainstorm mode (alignment before action)
/begin build        → Build mode (ship artifacts)
```

## Paths

All paths relative to project root:

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
- `last_session` — link to previous session (e.g., "[[sessions/session-21]]")
- `active_plan` — current plan if any
- `focus` — what we're working on (1 line)
- `plan_summary` — current plan summary (1 line)

Extract from content:
- Tasks — checkbox list (Obsidian format: `- [ ] task #status`)
- Constraints — linked decisions to honor

### Step 2: Read Last Session Handoff

Parse the `last_session` wikilink to get the file path (e.g., `[[sessions/session-21]]` → `vault/sessions/session-21.md`).

Read the last session file using native Read.

Extract:
- `topics` — what the session covered
- `outcome` — successful/blocked/abandoned
- **Context** section — what was worked on
- **Decisions** section — LOCKED and OPEN items
- **Memory** section — facts to persist
- **Next Steps** section — where to pick up

This provides the rich narrative context for cold start.

### Step 3: Handle First Run

If state.md doesn't exist or is empty:
- Create state.md with session: 1
- Display first-run welcome
- Skip to Step 6

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

### Step 4: Acknowledge Mode

State which mode is active:
- No argument → "Quick fix mode — minimal overhead, direct execution"
- `brainstorm` → "Brainstorm mode — alignment before action"
- `build` → "Build mode — executing approved plan"

### Step 5: Display Current State

```
## Resuming Session {N+1}

**Phase:** {phase}
**Focus:** {focus from frontmatter}
**Plan:** {plan_summary from frontmatter, or "none"}

### Last Session ({N})
**Topics:** {topics from last session}
**Outcome:** {outcome}

**Context:**
{Context section from last session handoff}

**Decisions:**
{Decisions section from last session handoff}

**Memory:**
{Memory section from last session handoff}

### Active Tasks
{tasks as checkbox list from state.md content}

### Constraints
{constraints from state.md}

### Next Steps (from last session)
{Next Steps section from last session handoff}
```

### Step 6: Mode-Specific Prompt

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

### Step 7: Confirm Session Start

After user responds:
```
Session {N+1} started. [{mode} mode]
```

## Notes

- Two files read for cold start: state.md (structure) + last session (narrative)
- state.md frontmatter provides: phase, focus, plan_summary
- state.md content provides: tasks (checkbox format), constraints
- Last session provides: context, decisions, memory, next steps
- If previous session outcome was `blocked`, highlight the blocker prominently
- Mode protocols are in `protocols/` — edit those files to change cognitive behavior
- scratch.md is prepared by `/wrap` at end of each session
- All vault files follow `vault/schemas.md` — reference it for field definitions
