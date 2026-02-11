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
- Re-read the approved plan (if exists)
- Confirm: "Executing Plan: {name}. Starting Phase {N}."
- If plan seems stale or scope unclear: Propose returning to Brainstorm

### 2. Phase Execution
- State which phase you're starting
- Break into working tasks (ephemeral by default)
- **Delegate:** Spawn sub-agents for exploration, bash ops, isolated coding
- **Contextualize:** Give sub-agents "Why" and "Constraints", not just "What"
- On phase completion: check off phase in plan file, brief status

### 3. Deviation Handling

| Situation | Response |
|-----------|----------|
| Minor friction (typo, small refactor) | Fix and continue |
| Unexpected complexity | Voice it, propose refinement, continue if approved |
| Scope change / new requirement | **Stop.** "This is new. Return to Plan mode?" |
| Blocker (dependency missing, unclear req) | **Stop.** Flag blocker, propose next step |

### 4. Completion
- All phases checked off
- Success criteria verified
- Update plan status to `complete`
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
