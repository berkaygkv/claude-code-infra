---
type: runbook
project: kh
updated: '2026-01-20'
phase: validation
blockers: none
---
# Runbook

## Progress

Initial infrastructure setup complete. Vault structure established with Sessions, Research, and Templates folders.

**Symlink setup verified:** Notes now live in `kh/` repo and are git-tracked.

**Session 4:** Comprehensive validation testing completed. All core features verified working: /begin, /wrap, Obsidian MCP, deep-research agent, WebSearch, Context7. Identified MCP search limitation through symlinks.

## Current

- [x] Create vault folder structure [phase:: infrastructure] ✅2026-01-19
- [x] Create project-level documents [phase:: infrastructure] ✅2026-01-19
- [x] Set up symlink for git versioning [phase:: infrastructure] ✅2026-01-19
- [x] Define session handoff schemas [phase:: infrastructure] ✅2026-01-20
- [x] Create session templates [phase:: infrastructure] ✅2026-01-20
- [x] Test full session lifecycle [phase:: validation] ✅2026-01-20

## Upcoming

- [ ] **→ Decide on frontmatter query solution** [phase:: validation] [priority:: 1]
- [ ] Define research workflow [phase:: research] [priority:: 1]
- [ ] Create research templates [phase:: research] [priority:: 2]
- [ ] Establish linking conventions [phase:: conventions] [priority:: 2]

## Knowledge Gaps

| Gap | Severity | Notes |
|-----|----------|-------|
| MCP search through symlinks | Medium | Obsidian MCP search doesn't index symlinked content; use Grep as workaround |
| Frontmatter queries for Claude | Medium | Need metadata index or query helper for structured queries |

## Blockers

None

---

## Task Queries

### Incomplete Tasks (Current Phase)

```dataview
TASK
FROM "notes/runbook"
WHERE !completed AND phase = "infrastructure"
SORT priority ASC
```

### All Incomplete Tasks

```dataview
TASK
FROM "notes/runbook"
WHERE !completed
GROUP BY phase
SORT priority ASC
```
