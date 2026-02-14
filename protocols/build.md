# Build Protocol (Execution Mode)

You are in **build** mode. Execute the plan.

## Cognitive Stance

| Aspect | Build Mode |
|--------|------------|
| Primary question | "Am I doing this right?" |
| Default action | Execute, fix, continue |
| Output target | Shipped artifacts |
| Code writes | **Full access** — codebase, vault, anywhere |

## Protocol

### 1. Pre-flight Check
- Read the active plan from `state.md` → `active_plan`
- Find current phase: first phase with unchecked tasks
- Confirm: "Executing Plan: {name}. Starting Phase {N}."
- If plan seems stale or scope unclear: stop, return to brainstorm

### 2. Phase Execution
- State which phase you're starting
- Break into working tasks (ephemeral by default)
- **Delegate:** Spawn sub-agents for exploration, bash ops, isolated coding
- **Contextualize:** Give sub-agents "Why" and "Constraints", not just "What"
- On phase completion: check off tasks, increment `phases_done` in frontmatter, brief status

### 2b. Inspect & Align (after spike phases or significant output)
- **Present the output** — show the inspectable artifact to the user. Not a summary, not a score — the actual output (extracted data, generated structure, built artifact).
- **User reviews and reacts** — "on track" / "off track" / "close but X needs to change". This is the validation gate.
- **Record finding** as narrative in the plan, next to the assumption. What worked, what didn't, what surprised us.
- **Assess impact** and proceed:
  - Task-level → adjust remaining tasks, continue
  - Phase-level → restructure phase, may need new spike
  - Direction-level → stop, return to brainstorm
- **Iterate if needed** — if output is close but not right, adjust and re-present. Don't move on until aligned.

### 3. Deviation Handling

| Situation | Response |
|-----------|----------|
| Minor friction (typo, small refactor) | Fix and continue |
| Unexpected complexity | Voice it, propose refinement, continue if approved |
| Spike output doesn't match expectations | Iterate the approach, not the metric. Re-present adjusted output. |
| Scope change / new requirement | **Stop.** "This is new. Return to Plan mode?" |
| Blocker (dependency missing, unclear req) | **Stop.** Flag blocker, propose next step |

### 4. Completion
- All phases checked off
- Set plan `status: completed`, `phases_done` = `phases_total`
- Clear `state.md` → `active_plan: null`
- Report: "Plan complete. {summary}."

## Adaptive Sub-task Tracking

- **Default:** Sub-tasks are ephemeral (Claude's working memory)
- **Triggers to persist:** Session ends mid-phase, blocker discovered, unexpected complexity
- **Action:** Add explicit checkpoints to that phase in the plan file
- **Principle:** Phases are sized to complete in one session. Sub-tasks in plan file are exception handlers.

## Writes Allowed

| Target | Allowed | Notes |
|--------|---------|-------|
| Codebase | ✓ | Full access |
| Plan files | ✓ | Update progress, check off phases |
| Vault | ✓ | Session notes, runbook updates |
| scratch.md | ✓ | Session changelog |

## Guard

No execution without:
1. Stated understanding of what we're building
2. Explicit user go-ahead

## Exit Condition

All phases complete OR explicit stop OR blocker

**Then:** `/wrap` to close session
