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
outcome:
continues_from: <% continuesFrom %>
transcript: "[[Sessions/transcripts/<% sessionName %>]]"
tags:
  - session
---

## Handoff

### Context
[What we were working on this session]

### Decisions
- LOCKED: [decision] — [rationale]
- OPEN: [question still unresolved]

### Memory
[Important things to remember across sessions]

### Next Steps
[Where to pick up, what's pending]
