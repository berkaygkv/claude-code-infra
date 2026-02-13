---
type: decision
title: "Research Format v2 — Flat Files with Metadata"
status: locked
date: 2026-02-13
session: "[[sessions/session-35]]"
tags: [decision]
---

# Research Format v2 — Flat Files with Metadata

Research folder redesign to fix discoverability and reduce structural bloat.

## Problems Addressed
- Directory-per-research is overkill (each dir has 1-2 files)
- Timestamp-slug names unreadable (`20260119-221115-the-key-features-of-uv-package-manager`)
- No frontmatter — invisible to Dataview, unsearchable
- No link back to the session that spawned it
- Write-only sink: 16 dirs, zero ever referenced

## Design

**Structure:** Flat files, not directories.
```
research/{YYYYMMDD}-{slug}.md
```

**Naming:** Date prefix + clean 2-4 word slug. `20260120-claude-code-hooks.md` not `20260120-004427-claude-code-hooks-system-focus-on-how/findings.md`.

**Frontmatter:**
```yaml
type: research
date: YYYY-MM-DD
session: "[[sessions/session-N]]"
topic: "Human-readable topic"
```

**Sources:** Inline `## Sources` section at bottom. No separate `sources.md`.

**Session linkback:** Session handoffs reference research generated during that session.

## Scope
- Modify `capture-research` hook to produce flat files with frontmatter + clean slugs
- Update CLAUDE.md research pipeline section
- No migration of existing 16 directories — new format going forward
- No bidirectional linking (per system-overhaul-v1 L3)
- No tags/categorization — search and session links are sufficient
