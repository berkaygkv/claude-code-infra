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
type: session
session: <% sessionNum %>
date: <% now %>
project: {{ cookiecutter.project_slug }}
topics: []
outcome: successful
continues_from: "[[sessions/<% continuesFrom %>]]"
transcript: "[[sessions/transcripts/<% sessionName %>]]"
decisions: []
research_spawned: []
tags:
  - session
---

## Handoff

### Context
<!-- What we worked on -->

### Decisions
<!-- What we decided -->

### Memory
<!-- Facts to persist -->

### Next Steps
<!-- What comes next -->
