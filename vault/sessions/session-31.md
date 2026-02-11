---
type: session
session: 31
date: 2026-02-11
mode: brainstorm
topics: [system-overhaul, plan-review, friction-reduction, voice-personality, protocol-simplification]
outcome: successful
continues_from: "[[sessions/session-30]]"
decisions:
  - "[[decisions/system-overhaul-v1]]"
---

# Session 31: System Overhaul — Plan Review & Refinement

## Context
Reviewed the system overhaul plan against every file it touches (CLAUDE.md, 3 protocols, 3 commands, research pipeline, schemas, dashboard, vault files). Found 6 gaps that would have caused breakage or confusion during build: dashboard dead query, phases_done ambiguity, session mode for no-arg begins, underspecified /meta rewrite, stale schemas.md content, and undefined scratch.md changelog format. Also caught that decision frontmatter needed `title` for dashboard queries. Resolved all gaps with concrete proposals. Added L10 (Voice section) — a personality block for CLAUDE.md inspired by a soul.md prompt. Updated the plan file with all refinements. Plan is now fully specified and ready for build.

## Decisions

### Locked
- System overhaul v1 (L1-L10 bundle) — 10 decisions tightening the entire kh system. See [[decisions/system-overhaul-v1]]
- Key refinements from review: dashboard "Open Research" section removed, `phases_done` kept, `mode: direct` for no-arg sessions, `/meta` writes individual files to `_meta/journal/` in brain vault, schemas.md updated before moving, scratch.md uses Meta + Events format

### Open
- None — plan fully specified

## Memory
- User values concepts but hates ceremony — "problem is implementation weight, not feature set"
- User wants swearing-when-it-lands in the voice section — genuine tone matters
- Bionic reading experiment: user asked for bold-first-letters formatting — interesting but probably not worth the effort for regular output
- Overhaul plan verified against all 15+ affected files — no remaining gaps
- Brain vault tasks from session 30 (create _sync/, draft Clawbot prompt) are PARKED — superseded by L5 (brain vault starts minimal)
- research-pipeline-v2 and brain-vault-integration constraints removed from state.md — superseded by system-overhaul-v1

## Next Steps
1. `/begin build` — execute system overhaul plan, Phase 1 (CLAUDE.md) first
2. Phases 2-4 can be parallelized after Phase 1
3. Phase 5 (validation) last — smoke test all commands
