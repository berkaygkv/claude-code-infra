# Session Begin Command

This command loads context from state.md + last session handoff and activates the specified mode.

## Usage

```
/begin              → Direct execution (no protocol loaded)
/begin brainstorm   → Brainstorm mode (alignment before action)
/begin build        → Build mode (ship artifacts)
```

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

### Step 2: Initialize scratch.md

Read scratch.md first (it may already exist from a previous session), then overwrite with the session changelog format:

```markdown
# Session Changelog

## Meta
- session: {N+1}
- mode: {brainstorm|build|direct}
- objective: {focus from state.md or user's stated goal}

## Events
- Session started — {objective}
```

Where:
- `{N+1}` is current_session + 1 from state.md
- `mode` is `brainstorm`, `build`, or `direct` (for no argument)
- `objective` comes from state.md `focus` field or the user's first message

### Step 3: Read Last Session Handoff

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

### Step 4: Handle First Run

If state.md doesn't exist or is empty:
- Create state.md with session: 1
- Initialize scratch.md with session: 1
- Display: "Session 1 (First Run) — Welcome to kh. No previous sessions. Ready to begin."
- Skip to Step 7

### Step 5: Acknowledge Mode

State which mode is active:
- No argument → "Direct execution — no protocol loaded"
- `brainstorm` → "Brainstorm mode — alignment before action"
- `build` → "Build mode — executing approved plan"

### Step 6: Display Current State

Show a summary with these sections:
- **Header:** "Resuming Session {N+1}" with phase, focus, plan from state.md frontmatter
- **Last Session ({N}):** topics, outcome, then the Context, Decisions, and Memory sections from the handoff
- **Active Tasks:** checkbox list from state.md
- **Constraints:** decision links from state.md
- **Next Steps:** from last session handoff

If previous session outcome was `blocked`, highlight the blocker prominently.

### Step 7: Mode-Specific Prompt

**Direct execution (no argument):**
```
Ready. What needs doing?
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

### Step 8: Confirm Session Start

After user responds:
```
Session {N+1} started. [{mode} mode]
```
