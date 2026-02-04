<%*
const topic = await tp.system.prompt("Research topic:");
const now = tp.date.now("YYYY-MM-DD");
-%>
---
type: research
topic: <% topic %>
status: open
created: <% now %>
completed: null
session: "[[sessions/session-]]"
confidence: low
led_to_decision: null
tags:
  - research
---

## Question
<!-- What we need to figure out -->

## Findings
<!-- Populated by deep-research agent -->

## Outcome
<!-- Decision made, if any -->
