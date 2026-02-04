---
session: 7
date: 2026-01-20
project: kh
topics:
  - rewind-research
  - rollback-command
  - git-notes-removal
  - architecture-simplification
outcome: successful
continues_from: session-6
transcript: "[[Sessions/transcripts/session-7]]"
tags:
  - session
---

## Handoff

### Context
This session investigated Claude Code's /rewind behavior and discovered it's completely broken (bug #15403 since Dec 25, 2025). We implemented a `/rollback` command that uses conversation-as-changelog to restore files mid-session. After analyzing the value proposition of git-notes, we decided to remove it entirely — the overhead wasn't justified given /rollback handles mid-session restore and notes are recoverable documentation.

### Decisions
- LOCKED: Remove git-notes infrastructure — /rollback handles mid-session restore; git-notes only provided disaster recovery for documentation files, not worth the overhead of maintaining a separate bare repo
- LOCKED: /rollback as primary restore mechanism — uses conversation history to identify and reverse file changes; works for both Edit tool and MCP writes
- LOCKED: Notes are NOT git-tracked — simplifies architecture; MCP search works natively; session handoffs capture what changed

### Memory
- Claude Code /rewind bug #15403: broken since Dec 25, 2025; only restores conversation, not code
- Even when fixed, MCP tools will NEVER be tracked by /rewind (only Edit/Write/NotebookEdit)
- /rollback requires reading files BEFORE editing to capture original state
- /rollback must be run BEFORE /rewind (needs conversation history intact)

### Next Steps
1. Use the simplified framework for real project work
2. Establish linking conventions for notes
3. Monitor bug #15403 — if fixed, /rollback becomes complementary rather than essential
