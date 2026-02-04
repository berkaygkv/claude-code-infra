---
session: 8
date: 2026-01-20
project: kh
topics:
  - vault-write-discipline
  - rollback-deprecation
  - procedural-vs-tooling
outcome: successful
continues_from: session-7
transcript: "[[Sessions/transcripts/session-8]]"
tags:
  - session
---

## Handoff

### Context
This session focused on recognizing and correcting an over-engineering mistake. We had built a `/rollback` command in session 7 to handle MCP write reversals, but realized the real solution was simpler: don't make speculative vault writes in the first place. Established "Vault Write Discipline" as a core principle and removed the /rollback command entirely.

### Decisions
- LOCKED: Vault Write Discipline — vault writes are commits, not drafts; only persist content at "commit" moments (/wrap, decision LOCKED, research complete, task done)
- LOCKED: Remove /rollback command — procedural solution preferred over tooling; if we don't make speculative writes, we don't need to undo them

### Memory
- The insight: "Procedural change before tooling change" — question whether the workflow is flawed before building tools to recover from it
- Vault "commit" moments: /wrap (session end), decision LOCKED, deep-research completes, task done
- If working memory needed mid-session, use conversation or local ephemeral file (kh/scratch.md)
- Meta-journal entry exists documenting this learning

### Next Steps
- Establish linking conventions for notes
- Use framework for real project work
- Consider future work: Claude Code customizations research, zero-to-working template, system prompt refinement, Mode 1/Mode 2 formalization
