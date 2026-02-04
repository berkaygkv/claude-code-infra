---
session: 11
date: 2026-01-20
project: kh
topics:
  - community-workflows-research
  - locked-semantics
  - phase-transitions
outcome: successful
continues_from: session-10
transcript: "[[Sessions/transcripts/session-11]]"
tags:
  - session
---

## Handoff

### Context
This session researched Claude Code community workflows to identify patterns worth borrowing. Ran deep-research agent across 60+ sources covering MCP memory servers, RIPER workflow, Research-Plan-Implement framework, hooks automation, and CLAUDE.md best practices. Selected two patterns to adopt: explicit phase transitions and living CLAUDE.md. Also clarified the semantics of LOCKED decisions.

### Decisions
- LOCKED: LOCKED Semantics — LOCKED means thoroughly thought through from all aspects, decided, moving on. To change requires unlocking with proof or strong reason. Not just "we decided" but "we decided with conviction" — high bar to reverse.
- OPEN: Explicit Phase Transitions — Research → Plan → Execute with clear signals between phases. Creates natural checkpoints and prevents "jump to coding" anti-pattern. (Need to define: strict protocol vs available phases)
- OPEN: Living CLAUDE.md — At /wrap, review session for repeated instructions/corrections and offer to add to CLAUDE.md.

### Memory
- Community patterns discovered: MCP memory servers (mcp-memory-keeper, mcp-memory-service), RIPER workflow (5-phase with branch-aware memory), Research-Plan-Implement framework (8 commands, thoughts/ directory)
- What we have that others don't: vault write discipline, scratch.md staging, research pipeline with TARGET/OUTPUT, Obsidian-native memory
- Anti-patterns to avoid: auto-compaction (prefer manual /compact at 70%), context poisoning between task types, TodoWrite doesn't persist (our runbook.md solves this)
- Research agent ID: a3562fb (can resume if needed)

### Next Steps
- Use framework for real project work (pick a real task and run a full session cycle)
- Implement explicit phase transitions (Research → Plan → Execute) with clear signals
- Add living CLAUDE.md pattern: at /wrap, review session for repeated instructions and offer to add
