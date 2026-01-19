---
type: runbook
project: kh
updated: '2026-01-19'
phase: infrastructure
blockers: none
---
# Runbook

## Progress

Initial infrastructure setup complete. Vault structure established with Sessions, Research, and Templates folders.

## Current

- [x] Create vault folder structure [phase:: infrastructure] ✅2026-01-19
- [x] Create project-level documents [phase:: infrastructure] ✅2026-01-19
- [ ] **→ Define session handoff schemas** [phase:: infrastructure] [priority:: 1]
- [ ] Create session templates [phase:: infrastructure] [priority:: 2]

## Upcoming

- [ ] Define research workflow [phase:: research] [priority:: 1]
- [ ] Create research templates [phase:: research] [priority:: 2]
- [ ] Establish linking conventions [phase:: conventions] [priority:: 2]
- [ ] First real session test [phase:: validation] [priority:: 1]

## Knowledge Gaps

| Gap | Severity | Notes |
|-----|----------|-------|
| *None identified* | | |

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
