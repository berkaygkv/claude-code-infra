# Brainstorm Protocol

## Trigger
New idea, unclear requirements, multiple approaches, need alignment.

## Purpose
Explore, challenge, converge on direction.

## Cognitive Stance

| Aspect | Brainstorm Mode |
|--------|-----------------|
| Primary question | "Is this the right thing to do?" |
| Default action | Challenge, clarify, explore alternatives |
| Output target | LOCKED decisions or approved plan |
| Code writes | **None** — no codebase changes until plan is approved |

## Phases

### 1. Understand
- Clarify user's intent
- Surface hidden assumptions
- Paraphrase back: "What I'm hearing is..."

### 2. Explore
- Generate options and approaches
- Identify trade-offs
- Research if needed (spawn deep-research agent)

### 3. Challenge
- Validate soundness of proposed approach
- Identify risks and edge cases
- Push back on flawed premises

### 4. Converge
- Mark decisions as OPEN or LOCKED
- Create plan file (if ready)
- Note parked items (explicitly "not doing")

## Constraints
- No codebase writes
- Decisions OPEN until explicitly LOCKED
- Route all staging through scratch.md

## Outputs
- Refined problem statement
- Decisions (OPEN/LOCKED)
- Plan (if ready)
- Research spawned (if needed)
- Parked items

## Writes Allowed

| Target | Allowed | Notes |
|--------|---------|-------|
| scratch.md | Yes | Stage decisions, notes, questions |
| plans/ | Yes | Create/update plan files |
| Codebase | No | No code until plan approved |
| Vault (other) | No | Route through scratch.md |

## Anti-Pattern Guards

| Trigger | Response |
|---------|----------|
| "Just fix it" | Pause. "Is this a symptom of a deeper design flaw?" |
| Unclear requirement | Halt. "I cannot proceed until we define X." |
| Silent assumption | Voice it. "I am assuming X. Is that correct?" |
| Scope creep | Flag it. "This is new. LOCK or PARK?" |

## Exit Condition

Plan is LOCKED + user approval ("LGTM", "go ahead", "approved")

**Then:** End session with `/wrap`, start next session with `/begin build`
