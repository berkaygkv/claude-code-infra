<%*
const sessionName = tp.file.title;
const now = tp.date.now("YYYY-MM-DD");
const timeStart = tp.date.now("HH:mm");
// Extract session number from filename
const sessionMatch = sessionName.match(/session-(\d+[a-z]?)/);
const sessionNum = sessionMatch ? sessionMatch[1] : sessionName;
-%>
---
session: <% sessionNum %>
date: <% now %>
time_start: <% timeStart %>
time_end:
project: kh
session_note: "[[sessions/<% sessionName %>]]"
tags:
  - session
  - transcript
---

<!-- Raw transcript exported from Claude Code session -->
<!-- This file is auto-populated by the transcript export hook -->
