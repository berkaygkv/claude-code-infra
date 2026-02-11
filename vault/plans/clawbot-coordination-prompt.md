---
type: plan
title: "Clawbot Coordination Prompt"
status: active
date: 2026-02-08
session: "[[sessions/session-31]]"
---

# Clawbot Coordination Prompt

Copy the message below and paste it into Telegram for Clawbot.

---

## Message to Paste

```
Hey KL, I've set up a coordination protocol so you and Claude Code can share the brain vault cleanly. Two changes:

1. New folder: `_sync/`
   - `_sync/for-clawbot/` — CC leaves handoffs for you here (status: pending → you process)
   - `_sync/for-claude-code/` — you leave handoffs for CC here
   - Only for explicit "do this" requests, not for every edit

2. New frontmatter fields on all brain vault files going forward:
   - `created_by`: clawbot | claude-code | berkay
   - `last_modified_by`: same values (update when you edit)
   - `source_session`: your context ref or CC's session number

Key rules:
- Search before creating any file — update existing content, don't duplicate
- Knowledge = living docs (update in place). Artifacts = immutable snapshots (create new, never edit old)
- Project briefs (`projects/{slug}/brief.md`) = the star doc per project, either of you can update

Full spec is at `_meta/coordination/claude-code-protocol.md` — read it when you get a chance and let me know if anything needs adjusting.
```
