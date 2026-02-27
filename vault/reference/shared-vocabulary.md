---
type: reference
title: "Shared Vocabulary"
date: 2026-02-27
decision: "[[decisions/scratch-collab-surface]]"
---

# Shared Vocabulary

Protocol compression layer — named concepts that govern recurring decision patterns. Each entry earns its slot by meeting the selection principle: **without this concept loaded, we'd make worse choices.**

Three source domains: software engineering, project management, our system-specific patterns.

---

## Software Engineering

### 1. Reversibility
*SWE general*

Prefer decisions that are cheap to undo. When something breaks, ask "how expensive is a reset?" before attempting surgical repair. S35: vault audit chose to flatten research dirs rather than fix them — rebuilding was cheaper than untangling. S19: reset main to pre-cookiecutter rather than fix broken state. Reversibility is a **tiebreaker, not a trump card** — when two approaches deliver similar quality, prefer the reversible one. Don't downgrade solution quality just to stay reversible.

*Anti-pattern:* Treating every decision as permanent. But also: choosing simplistic solutions over sophisticated ones solely because they're easier to undo.

### 2. Blast radius
*SWE general*

The scope of damage if something goes wrong. Checked *before* reversibility — a reversible action with massive blast radius still warrants a pause. Governs the confirmation-before-action stance in CLAUDE.md (git push, destructive ops). S50: parallel agents work because each has small blast radius (single file).

*Anti-pattern:* Only checking "can I undo this?" without asking "how much breaks if this goes wrong?"

### 3. YAGNI
*Extreme Programming*

"You Aren't Gonna Need It." Don't build for hypothetical futures. S1: Phase 5 research enhancements deferred — "solve with behavior not infrastructure." S48: scratch surface ships as foundation before broader PM system. Every parked item in state.md is a YAGNI call.

*Anti-pattern:* Building infrastructure "because we'll need it eventually." If friction hasn't appeared, the feature isn't needed.

### 4. Separation of concerns
*SWE general*

Each component does one thing. state.md captures *what*, scratch.md captures *why*, decisions/ captures *commitments*. Two modes (brainstorm vs build) separate thinking from doing. IO strategy separates native (known paths) from MCP (discovery). Not just code — applies to documents, protocols, roles.

*Anti-pattern:* A file/protocol/tool that does two jobs. The moment you say "this also handles..." — split it.

### 5. Idempotency
*SWE general*

Operations that can be safely repeated without side effects. Session numbering finds MAX (gaps are harmless). Template sync is always main→template (one direction). `/begin` reads state without modifying it. Enables fearless re-runs.

*Anti-pattern:* Operations that require "did I already do this?" tracking. If you have to check, it's not idempotent.

---

## Project Management

### 6. Focus as currency
*Our system (S37 breakthrough)*

"Speed is the superpower. Don't out-think the holes — out-build them." In human/AI collaboration, implementation is cheap — what traditional teams build in weeks, we build in minutes. Building and discarding costs almost nothing because you get real artifacts to inspect, immediate feedback, and evidence that accumulates. Exhaustive planning is the expensive move: it consumes focus on speculation instead of evidence, and AI sycophancy makes plans look polished while carrying unexamined assumptions. The scarce resource isn't time — it's **directional coherence.** Every protocol in the system is a focus-protection mechanism: appetite caps focus investment, WIP limits prevent fragmentation, kill rituals recover focus from dead ends, and the validation loop ensures we spike before we speculate. S37 proved this structurally — brainstorm's job got smaller because spikes do the heavy lifting.

*Anti-pattern:* "That would take too long to build." No it wouldn't. Also: assessing cost in hypothetical time ("two weeks of development") — always wrong in this context. Assess in focus impact instead.

### 7. Appetite
*Shape Up (Basecamp), reframed for human/AI collaboration*

A focus budget, not a time estimate. The tag on shaped items ([chore]/[small]/[large]) that caps attentional investment. [large] consumes focus across sessions. [chore] runs alongside without diverting attention. If the work exceeds its appetite, the approach is wrong — reshape it, don't extend the budget.

*Anti-pattern:* Measuring appetite in time ("this [small] took two sessions"). Time is cheap. The question is whether the work held or scattered focus.

### 8. Shaping
*Shape Up (Basecamp)*

The gate between "idea" and "work." Three requirements: appetite + approach + done-definition. An unshaped item is not ready to work on — period. S52: triaged 6 inbox items, 4 got shaped, 2 got parked. Shaping is a living gate, not a contract — minor gaps discovered during work update the shape in place. Major gaps (scope change, wrong appetite) trigger the kill ritual.

*Anti-pattern:* Starting work on something because it "seems clear enough." If it lacks all three gates, it's not shaped.

### 9. WIP limit
*Kanban / Lean*

Hard capacity constraint: 1 large OR 2 small/chore simultaneously. Prevents focus fragmentation — the most expensive failure mode in our system. Forces prioritization: you can't start something new without finishing or parking something current. Chores don't consume WIP but still need shaping.

*Anti-pattern:* Carrying 4 "active" items and making progress on none.

### 10. Kill ritual
*Our system, inspired by Shape Up circuit breakers*

Structured failure protocol. Three triggers: same failure pattern after 3 iterations → structural problem, escalate to brainstorm. Scope change mid-build → stop, return to plan. Large item fails → back to inbox/parked with failure narrative. S40: formalized after testing validation system across 6 sessions. Killing is cheap (focus as currency) — grinding is expensive.

*Anti-pattern:* Grinding through a failing approach because you've invested time in it. Sunk cost is not a reason to continue.

---

## System-Specific

### 11. Cold start
*Our system*

The problem of resuming work with zero context. Every session begins from nothing — no memory, no continuity, no implicit knowledge. The entire vault architecture (state.md, session handoffs, decision files, scratch surface) exists to solve this single problem. Every artifact earns its place by answering: "does this make cold starts faster?"

*Anti-pattern:* Creating artifacts that serve the current session but provide no cold-start value.

### 12. Scratch surface
*Our system*

Shared working surface where reasoning survives chat scroll and context compression. state.md captures *what* (tasks, decisions); scratch captures *why* (rejected alternatives, active thinking). Both parties write and annotate. Rewrite, don't append — keep only what's live. S48: designed and dogfooded in same session.

*Anti-pattern:* Keeping reasoning in chat and hoping it survives context compression. If it matters tomorrow, it belongs on the surface.

### 13. Reason first, verdict last
*Our system (stance rule)*

Autoregressive generation creates lock-in: once Claude states a verdict, subsequent reasoning bends to justify it. Leading with reasoning produces more honest analysis. Build the full case — evidence, analysis, tradeoffs — before the conclusion. But once reasoning is done, commit. No menus, no hedging.

*Anti-pattern:* "I think we should do X. Here's why: [rationalization]." The verdict poisons the reasoning.

### 14. Evidence over abstraction
*Our system (stance rule)*

Cite specific files, quote actual data, use real numbers. "The decision file says 16 dirs, zero referenced" beats "there may be discoverability concerns." S35: vault audit mapped every folder and document before making any decision. S52: parallel research agents before triage, not gut-feel sizing.

*Anti-pattern:* "There may be concerns about..." — either cite the concern concretely or admit you don't have evidence.

### 15. Validation loop
*Our system (S37 decision)*

Spike the riskiest assumption before committing to a full plan. Build fast, inspect output, align on direction, iterate. Qualitative-first: the gate is user alignment ("does this match what we're building?"), not metrics. Plans accumulate findings as evidence, not just checkmarks. S37-S40: designed after recognizing that behavioral instructions to "be more critical" don't survive contact with model tendencies — structural intervention required.

*Anti-pattern:* Planning exhaustively without empirical feedback. Polished plans that carry unexamined assumptions.

### 16. Actionable specificity
*Our system (S10 decision)*

Items must be specific enough to act on without asking "what does this mean?" S10: discovered "linking conventions" was untraceable — a placeholder for a feeling, not a defined task. Test: can future-you start working immediately? If not, it's still a thought, not a task. Applies to next steps, shaped items, and commit messages.

*Anti-pattern:* "Improve the documentation." Improve what? For whom? To what standard?

### 17. Call the meta-work
*Our system (stance rule)*

Infrastructure serves product. If sessions are refining the system instead of shipping with it, flag it explicitly. Not "don't do meta-work" — sometimes the system genuinely needs improvement. But name it. Don't let system polishing masquerade as productive work.

### 18. Playbook over menu
*Our system (S45)*

Compose from principles, don't select from templates. S45: video research skill uses a playbook of composable atoms instead of static template selection. Claude composes the right prompt from principles, not picks from a menu. Applies beyond prompts — to decisions, to design approaches, to skill architecture.

*Anti-pattern:* "Pick option A, B, or C." If the options don't cover the actual situation, the menu is the problem.
