---
session: 13
date: 2026-01-22
project: kh
topics:
  - vault-audit
  - dataview-fix
  - claude-md-sync
  - runbook-cleanup
outcome: successful
continues_from: session-12
transcript: "[[Sessions/transcripts/session-13]]"
tags:
  - session
---

## Handoff

### Context
This session conducted a comprehensive vault health audit. Discovered and fixed Dataview query path bugs (wrong vault root assumption). Updated CLAUDE.md to match locked decisions (vault path, scratch structure, research pipeline with enforced TARGET requirement). Cleaned up runbook.md by removing redundant session summaries, reorganizing tasks into Active/Completed/Dropped sections, and fixing the Dataview query filter.

### Decisions
- LOCKED: TARGET enforcement — Research agents cannot spawn without first creating a TARGET file. Updated in CLAUDE.md research pipeline section.
- LOCKED: Vault I/O consistency in skills — /begin skill should use native Read for content (identified drift, not yet fixed in skill definition).

### Memory
- Obsidian vault root is `.obs-vault/notes/` (where .obsidian lives), not `.obs-vault/`
- Dataview queries need vault-relative paths: `FROM "runbook"` not `FROM "notes/runbook"`
- runbook.md session summaries were redundant with session notes — removed, now links to Sessions folder
- Research pipeline has 14 outputs but only 2 TARGETs — legacy ad-hoc outputs predate schema enforcement

### Next Steps
- Update /begin skill to use native Read instead of MCP read_note (consistency with locked I/O decision)
- Add Plan Schema and Mode Transitions to schemas.md [priority 1]
- Add living CLAUDE.md pattern to /wrap skill
