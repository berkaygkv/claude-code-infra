<%*
const title = await tp.system.prompt("Plan title:");
const now = tp.date.now("YYYY-MM-DD");
-%>
---
type: plan
title: <% title %>
status: draft
created: <% now %>
updated: <% now %>
session_created: "[[sessions/session-]]"
session_completed: null
phases_total: 0
phases_done: 0
related_decisions: []
tags:
  - plan
---

## Goal
<!-- One sentence -->

## Scope
**In:** <!-- What's included -->
**Out:** <!-- What's excluded -->

## Phases

### Phase 1: Name
- [ ] Task 1
- [ ] Task 2

## Success Criteria
- Criterion 1
- Criterion 2
