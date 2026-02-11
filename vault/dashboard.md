---
type: dashboard
---

# Dashboard

## Current State
**Phase:** `= [[state]].phase`
**Focus:** `= [[state]].focus`
**Plan:** `= [[state]].plan_summary`

---

## Tasks

```dataview
TASK
FROM "state"
WHERE !completed
GROUP BY file.link
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

## Plan Progress

```dataview
TABLE WITHOUT ID
  title AS "Plan",
  status AS "Status",
  phases_done + "/" + phases_total AS "Progress"
FROM "plans"
WHERE status = "in_progress" OR status = "approved"
```
