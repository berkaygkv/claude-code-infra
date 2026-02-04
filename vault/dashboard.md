---
type: dashboard
---

# Dashboard

## Current State
**Phase:** `= [[state]].phase`
**Focus:** `= [[state]].Focus`
**Plan:** `= [[state]].Plan`

---

## Tasks

```dataview
TABLE WITHOUT ID
  T.text AS "Task",
  T.status AS "Status",
  T.blocked_by AS "Blocked By"
FROM "state"
FLATTEN file.tasks AS T
WHERE T.status != "done"
```

---

## Recent Decisions

```dataview
TABLE WITHOUT ID
  title AS "Decision",
  status AS "Status",
  date AS "Date"
FROM "decisions"
SORT date DESC
LIMIT 5
```

---

## Session History

```dataview
TABLE WITHOUT ID
  file.link AS "Session",
  date AS "Date",
  outcome AS "Outcome",
  join(topics, ", ") AS "Topics"
FROM "sessions"
WHERE type = "session"
SORT session DESC
LIMIT 5
```

---

## Open Research

```dataview
TABLE WITHOUT ID
  topic AS "Topic",
  confidence AS "Confidence"
FROM "research"
WHERE status = "open"
```

---

## Plan Progress

```dataview
TABLE WITHOUT ID
  title AS "Plan",
  status AS "Status",
  phases_done + "/" + phases_total AS "Progress"
FROM "plans"
WHERE status = "in_progress" OR status = "approved"
```
