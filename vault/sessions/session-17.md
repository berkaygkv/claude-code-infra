---
session: 17
date: 2026-01-24
project: kh
topics: [modal-begin, dynamic-protocol-loading, claude-code-preprocessing]
outcome: successful
continues_from: session-16
transcript: "[[Sessions/transcripts/session-17]]"
tags:
  - session
---

## Handoff

### Context
This session implemented the modal `/begin` system — allowing users to choose their cognitive mode at session start via `/begin brainstorm`, `/begin build`, or just `/begin` for quick fixes. We researched Claude Code's preprocessing capabilities, discovered security restrictions on `${}` syntax, and implemented a workaround using external scripts with permission allowlists.

### Decisions
- LOCKED: Modal /begin System — `/begin [mode]` loads mode-specific protocols; user controls cognitive load
- LOCKED: Protocol Files Location — Mode protocols in `kh/protocols/` (base.md, brainstorm.md, build.md)
- LOCKED: Skill Preprocessing Workaround — External scripts for conditional logic; `${}` blocked, use `!/path/script.sh $ARGUMENTS` pattern

### Memory
- `!`command`` in skills runs preprocessing BEFORE Claude sees content
- `$ARGUMENTS` substituted by Claude Code directly (not bash) — this works
- `${}` bash parameter substitution blocked by Claude Code security
- Workaround: External scripts in `kh/scripts/` with `permissions.allow` in settings.json
- Pattern for dynamic loading: `!/home/.../scripts/load-protocol.sh $ARGUMENTS`
- Deep research agent found: Superpowers framework uses similar pattern (separate skills per mode)

### Next Steps
- Create starter kit: Obsidian vault + hooks + configs that pass e2e test
- Draft improved system prompt and test on 3 different task types
- Test /begin modes in real project work to validate the cognitive separation
