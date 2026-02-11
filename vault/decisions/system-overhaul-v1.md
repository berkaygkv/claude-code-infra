---
type: decision
title: "System Overhaul v1 — Minimal Friction, Full Promise"
status: locked
date: 2026-02-11
session: "[[sessions/session-32]]"
supersedes: "[[decisions/research-pipeline-v2]]"
tags: [decision]
---

# System Overhaul v1 — Minimal Friction, Full Promise

Bundle of 10 decisions tightening the kh system. Guiding principle: preserve every concept earned over 30 sessions, fix implementations that add friction without value. Start at simplest viable form, let real friction drive complexity.

## Decisions

**L1 — Two modes only:** Remove Quick Fix as a named mode. No-arg `/begin` = direct execution, no protocol loaded.

**L2 — Scratch.md as session changelog:** Replace the staging-area scratch format (Meta/Decisions/Memory/Tasks/Notes) with a running changelog (Meta + Events). Claude updates on notable events; /wrap reads the log to build handoff.

**L3 — Simplified research pipeline:** Remove TARGET system entirely. Two tiers remain: quick lookup (use tools directly) and deep research (spawn agent, hook captures output). No pre-registration, no bidirectional linking.

**L4 — Simplified decision format:** Drop `superseded_by`, `related`, forced body sections. Keep `title` in frontmatter (dashboard needs it). Body is free-form.

**L5 — Brain vault starts minimal:** Keep `created_by` only. Drop `last_modified_by`, `source_session`. Drop folder contracts reference. Add complexity when real friction demands it.

**L6 — Delete vault/templates/:** Obsidian Templater templates never used. Remove entirely.

**L7 — Move schemas.md:** Move from `vault/schemas.md` to `.claude/skills/upgrade/references/schemas.md`. Schemas are infrastructure, not vault content.

**L8 — /meta targets brain vault:** Rewrite /meta to write individual files to `_meta/journal/{slug}.md` via `mcp__brain__write_note`. Drop `/tmp/kh-session.json` dependency and interactive two-prompt flow.

**L9 — Dashboard cleanup:** Remove "Open Research" section (queried `research/targets` which no longer exists).

**L10 — Voice section:** Add personality block to CLAUDE.md Section 1. Brevity, opinions, directness, wit, challenge, controlled swearing.

## Also supersedes

- [[decisions/brain-vault-integration]] — L5 simplifies the brain vault integration to minimal rules
