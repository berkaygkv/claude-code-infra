<%*
const title = await tp.system.prompt("Decision title:");
const now = tp.date.now("YYYY-MM-DD");
-%>
---
type: decision
title: <% title %>
status: locked
date: <% now %>
session: "[[sessions/session-]]"
supersedes: null
superseded_by: null
related: []
tags:
  - decision
---

## Decision
<!-- The decision -->

## Rationale
<!-- Why we chose this -->

## Alternatives Considered
<!-- What we rejected -->
