---
type: session
session: 53
date: 2026-02-27
mode: brainstorm
topics: [shared-vocabulary, focus-as-currency, markup-review, concept-selection-criteria]
outcome: successful
continues_from: "[[sessions/session-52]]"
decisions: []
---

# Session 53: Design shared vocabulary card

## Context

Brainstormed and finalized the shared vocabulary card — a protocol compression layer of 18 named concepts across three domains (software engineering, project management, system-specific). Key breakthrough: "focus as currency" emerged as a standalone foundational concept, anchored to S37's "speed is the superpower" insight. The card isn't a glossary — it's named concepts that govern recurring decision patterns, where each entry earns its slot by the selection principle: without it loaded, we'd make worse choices.

Used the scratch surface markup flow: wrote 17 candidates to scratch, user annotated in Obsidian (4 callouts: reversibility risk question, appetite reframe warning, shaping lifecycle question, validation loop endorsement). Responded only to marked items, revised accordingly. Focus as currency added as 18th entry after user identified that time/effort aren't costs in human/AI collaboration — focus is.

Explore agent hallucinated an entire Neo4j project when asked to scan sessions — fabricated domain-specific content from a project that doesn't exist. Caught by user, redone with direct reads.

## Decisions

### Locked

None — card is a reference artifact, not a locked design choice. Plan approved for build.

### Open

- Vocabulary loading strategy — full load vs selective/on-demand. Parked: structure-first, mechanism later.
- /vocab slash command design — how to capture terms mid-session.

## Memory

- Explore agent hallucinated project content when given too many files to scan. Fabricated Neo4j/NVIDIA/extraction pipeline data from sessions that contain none of it. Root cause likely context limits + confabulation. Mitigation: direct reads over sweeping agent scans for evidence-gathering.
- "Focus as currency" traces to S37's validation loop discussion — "speed is the superpower, don't out-think the holes, out-build them." The user's framing: "build fast, fail fast because implementing costs less than thinking."
- User explicitly flagged that assessing cost in hypothetical time ("two weeks of development") is an anti-pattern across the entire system, not just for appetite sizing.
- Markup review flow worked well: wrote to scratch, user annotated 4 of 17 items, silence = agree on the rest. Efficient for large proposal sets.
- Selection principle for vocabulary: "governs a recurring decision pattern — without this concept loaded, leads to worse choices." Not "interesting concept."
- Card structure must support atomic entry access (individual terms pullable without the whole card) for future selective loading.

## Next Steps

- **Active continuing:** Shared vocabulary card [small] — plan approved, `/begin build` to execute Phase 1 (write card file, update references)
- **Shaped for next session:** Chores available alongside build: template sync [chore], vault housekeeping [chore]
- **Inbox captured:** 2 items (/vocab command, loading strategy)
