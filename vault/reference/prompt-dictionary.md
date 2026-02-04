# Prompt Dictionary

> Personal reference for precise AI instruction. Better inputs → better outputs.

---

## Implementation Quality

| Vague | Precise Alternative |
|-------|---------------------|
| "Be thorough" | "Cover edge cases, error states, and the unhappy path—not just the golden path." |
| "Plan before coding" | "Show me your approach first: what files you'll touch, what order, what could go wrong. No code until I approve." |
| "Do it properly" | "Production-grade: error handling, input validation, logging, and tests where appropriate." |
| "Think it through" | "Walk me through your reasoning before executing. What are the trade-offs? What did you consider and reject?" |
| "Be careful" | "Identify risks before acting. If something is destructive or hard to reverse, pause and confirm." |

---

## Scope Control

| Vague | Precise Alternative |
|-------|---------------------|
| "Keep it simple" | "Minimum viable solution. No abstractions, no future-proofing, no 'nice to haves'—just what's needed now." |
| "Don't over-engineer" | "Solve the stated problem only. If you're tempted to add configurability or generalization, don't." |
| "Stay focused" | "If you discover adjacent issues or improvements, note them but don't act. Scope is locked." |
| "Just fix the bug" | "Surgical fix only. Don't refactor surrounding code, don't add comments to unchanged lines, don't 'improve' what works." |

---

## Communication & Process

| Vague | Precise Alternative |
|-------|---------------------|
| "Explain yourself" | "After each decision, give me a one-sentence rationale. Not what you did—why you chose it over alternatives." |
| "Keep me informed" | "Surface blockers, assumptions, and uncertainties as you encounter them—don't bundle them at the end." |
| "Ask questions" | "If a requirement is ambiguous or you're choosing between valid approaches, stop and ask. Don't assume." |
| "Check your work" | "Before declaring done: re-read the original request, verify each requirement is met, test the unhappy path." |

---

## Research & Exploration

| Vague | Precise Alternative |
|-------|---------------------|
| "Look into this" | "I need to understand X before deciding. Give me: what it is, trade-offs, and your recommendation with reasoning." |
| "Find out how" | "Research the standard/idiomatic way to do X in this codebase/framework. Show me examples from authoritative sources." |
| "Explore options" | "Give me 2-3 distinct approaches with pros/cons. Don't pick one yet—I want to see the landscape first." |
| "Be creative" | "I'm open to unconventional solutions. Show me the obvious approach AND one alternative I might not have considered." |

---

## Execution Mode

| Vague | Precise Alternative |
|-------|---------------------|
| "Just do it" | "This is straightforward—execute without checkpoints. I trust your judgment on implementation details." |
| "Be autonomous" | "Make reasonable decisions without asking. Only pause for: destructive actions, ambiguous requirements, or architectural choices." |
| "Work independently" | "Complete the full task including verification. Come back when it's done, not when each step is done." |
| "Go slow" | "Checkpoint after each logical unit of work. Show me progress before continuing to the next phase." |

---

## Quality Gates

| Vague | Precise Alternative |
|-------|---------------------|
| "Make sure it works" | "Verify: does it compile/run? Does it handle the stated inputs? Does it fail gracefully on bad inputs?" |
| "Test it" | "Write tests for: the happy path, at least one edge case, and at least one error condition." |
| "Review before finishing" | "Before marking complete: re-read the original request, diff your changes, verify nothing unintended was modified." |
| "Double-check" | "State your assumptions explicitly, then verify each one is actually true in this context." |

---

## Compound Instructions (Templates)

### "Design-First Implementation"
> "This requires careful implementation. Phase 1: Explore the relevant code and propose an approach. Phase 2: I'll review and approve. Phase 3: Execute. No code until Phase 2 is complete."

### "Surgical Fix"
> "Fix only the stated issue. Don't refactor, don't add tests unless the bug is a missing test case, don't touch unrelated code. Show me exactly what changed and why."

### "Exploratory Research"
> "I don't know enough to make a decision yet. Research X and give me: (1) what it is in plain terms, (2) 2-3 approaches with trade-offs, (3) your recommendation with reasoning. No implementation—just inform me."

### "Autonomous Execution"
> "This is well-defined. Execute end-to-end without checkpoints. Make reasonable judgment calls. Come back when it's done or if you hit a genuine blocker."

### "High-Stakes Change"
> "This is risky/hard to reverse. Before any action: (1) state what you're about to do, (2) state what could go wrong, (3) wait for my explicit 'proceed'."

---

## Anti-Patterns to Avoid

| Don't Say | Why It Fails | Say Instead |
|-----------|--------------|-------------|
| "Be smart about it" | Undefined standard | State the specific quality you want |
| "Use best practices" | Vague, context-dependent | Name the specific practice or pattern |
| "Make it good" | No measurable criteria | Define what "good" means for this task |
| "Think harder" | Not actionable | "Reconsider X specifically" or "What did you miss?" |
| "Be more careful" | Doesn't identify the gap | "Specifically check for Y before proceeding" |

---

*Last updated: 2026-01-22*
