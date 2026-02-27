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

### Step 0: Resolve Vault Path

The vault is the directory containing `.obsidian/` inside the project root. All `vault/` references below use this as the default — substitute with the actual vault directory name if different.

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
- Objective — project-level anchor (§ Objective section)
- Active — items currently being worked on (§ Active section)
- Shaped — items ready to execute with appetite + approach (§ Shaped section)
- Parked — explicitly deprioritized items (§ Parked section, only if non-empty)
- Constraints — linked decisions to honor

### Step 1b: Check Inbox

Read `vault/inbox.md`. Count the number of items (lines starting with `- `).
If count > 5, flag: "Inbox has {N} items — triage recommended."

### Step 1c: Load reference cards

Read these silently (cold-start awareness — do not display card content):

- `vault/reference/triage-criteria.md` — appetite sizing, shaping checklist, kill ritual triggers, chore exception rule. Used implicitly when triaging inbox items or assessing whether shaped items are ready for Active.
- `vault/reference/shared-vocabulary.md` — 18 named concepts governing recurring decision patterns. Internalize at cold start, never display to user.

### Step 2: Load scratch surface

Read `vault/scratch.md` and `vault/reference/scratch-convention.md` silently (cold-start awareness — do not display convention card).

**Scratch is reset by `/wrap`, not `/begin`.** If scratch has content from a previous session (e.g., `/wrap` wasn't run, or a session was abandoned), preserve it — that reasoning is valuable cold-start context. Mention surviving content in the state summary (Step 6).

**Initialize only if scratch is empty or missing.** In that case, write:

```markdown
# Scratch — Session {N+1}

Session objective: [TBD]
```

Where `{N+1}` is current_session + 1 from state.md.

**Objective lifecycle:** Objective starts as `[TBD]`. Once session direction is aligned through conversation, update to `[LOCKED] {objective}` and write the `## Problem` section. The Problem section anchors all reasoning bullets below it.

**Maintaining vault/scratch.md during the session:**
- Write the Problem section (2-4 sentences, plain english) once the objective locks
- Add reasoning bullets below it: rejected alternatives, key insights, anchoring context
- Rewrite, don't append — remove resolved items, keep only what's live
- On mid-session topic shift: rewrite the Problem section, carry forward relevant bullets
- Filter: "Would losing this reasoning to scroll-away hurt the rest of the session?"
- **Both parties write and annotate.** Use Obsidian callouts (question/warning/tip/info) for positional feedback. Silence = agree.
- For structured proposals (3+ related points): write to surface, signal "ready for marks". User annotates in Obsidian, signals "read it". Respond only to marked items.
- `## Decided` section added on-demand when items are resolved — not part of the init template.

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
- **Active:** items from § Active section, each shown with appetite tag. If an item was Active in the previous session, prefix with "↳ Continuing:"
- **Shaped:** items from § Shaped section (show appetite tags)
- **Parked:** items from § Parked section (only show if non-empty)
- **Inbox:** show count. If > 5, add "(triage recommended)"
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

Run `/output-style kh-brainstorm` for optimized formatting.
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

For both build prompts, append:
```
Run `/output-style default` if not already active.
```

### Step 8: Confirm Session Start

After user responds:
```
Session {N+1} started. [{mode} mode]
```
