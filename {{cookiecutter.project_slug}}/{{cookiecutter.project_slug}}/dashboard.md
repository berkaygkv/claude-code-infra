---
type: dashboard
---

# Dashboard

## Current State
**Phase:** `= [[state]].phase`
**Focus:** `= [[state]].focus`
**Plan:** `= [[state]].plan_summary`

---

## Lifecycle

![[state#Active]]

![[state#Shaped]]

![[state#Parked]]

---

## Inbox

![[inbox#Inbox]]

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
WHERE status = "active" OR status = "approved"
```
