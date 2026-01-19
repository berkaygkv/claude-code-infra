<%*
const sessionName = tp.file.title;
const now = tp.date.now("YYYY-MM-DD");
// Extract session number from filename (e.g., "session-15" -> 15)
const sessionMatch = sessionName.match(/session-(\d+[a-z]?)/);
const sessionNum = sessionMatch ? sessionMatch[1] : sessionName;
// Calculate previous session for continues_from
const prevNum = sessionMatch ? parseInt(sessionMatch[1]) - 1 : null;
const continuesFrom = prevNum && prevNum > 0 ? `session-${prevNum}` : "";
-%>
---
session: <% sessionNum %>
date: <% now %>
project: kh
topics: []
outcome: successful  # successful | blocked | partial
continues_from: <% continuesFrom %>
transcript: "[[Sessions/transcripts/<% sessionName %>]]"
tags:
  - session
---

## Handoff

### Context
<!-- 2-4 sentences: What this session focused on and what was accomplished -->

### Decisions
<!-- Format: "- LOCKED: {decision} — {rationale}" or "- OPEN: {issue} — {current thinking}" -->

### Memory
<!-- Technical facts, paths, quirks, workarounds to remember across sessions -->

### Next Steps
<!-- Prioritized list; first item becomes default suggestion for /begin -->
