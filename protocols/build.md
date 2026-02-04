# Build Protocol

## Trigger
Plan approved. User says "go", "LGTM", "approved".

## Purpose
Execute the plan. Ship working artifacts.

## Cognitive Stance

| Aspect | Build Mode |
|--------|------------|
| Primary question | "Am I doing this right?" |
| Default action | Execute, fix, continue |
| Output target | Shipped artifacts |
| Code writes | **Full access** — codebase, vault, anywhere |

## Phases

### 1. Pre-flight
- Read the approved plan
- Confirm scope: "Executing Plan: {name}. Starting Phase {N}."
- If plan stale or unclear: Propose returning to Brainstorm

### 2. Execute
- State which phase you're starting
- Break into working tasks (ephemeral by default)
- Delegate to sub-agents for exploration, bash ops, isolated coding
- Give sub-agents "Why" and "Constraints", not just "What"
- On phase completion: check off in plan file

### 3. Deviate
| Situation | Response |
|-----------|----------|
| Minor friction (typo, small refactor) | Fix and continue |
| Unexpected complexity | Voice it, propose refinement, continue if approved |
| Scope change / new requirement | **Stop.** "This is new. Return to Brainstorm?" |
| Blocker (dependency missing, unclear req) | **Stop.** Flag blocker, propose next step |

### 4. Complete
- All phases checked off
- Success criteria verified
- Update plan status to `complete`
- Report: "Plan complete. {summary}."

## Constraints
- Stay within approved scope
- No silent expansion
- Deviations flagged immediately
- Commits at checkpoints only (or /wrap)

## Outputs
- Working code/artifacts
- Updated plan (phases checked off)
- Deviation log (if any)

## Writes Allowed

| Target | Allowed | Notes |
|--------|---------|-------|
| Codebase | Yes | Full access |
| plans/ | Yes | Update progress, check off phases |
| Vault | Yes | Session notes via /wrap |
| scratch.md | Yes | Stage wrap content |

## Adaptive Sub-task Tracking
- **Default:** Sub-tasks are ephemeral (Claude's working memory)
- **Persist if:** Session ends mid-phase, blocker discovered, unexpected complexity
- **Action:** Add explicit checkpoints to plan phase
- **Principle:** Phases sized to complete in one session. Sub-tasks in plan are exception handlers.

## Guard

No execution without:
1. Stated understanding of what we're building
2. Explicit user go-ahead

## Exit Condition

All phases complete OR blocked OR scope explosion

**Then:** `/wrap` to close session
