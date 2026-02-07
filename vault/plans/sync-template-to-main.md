---
type: plan
title: Sync Template Improvements to Main
status: locked
created: 2026-02-07
session: "[[sessions/session-26]]"
tags:
  - plan
---

# Sync Template Improvements to Main

## Goal
Bring polished template improvements back into the dev workspace (main branch) so both stay aligned.

## Scope
6 files updated, 1 file merged. No new files. No structural changes.

## Phases

### Phase 1: Protocols
Update brainstorm.md and build.md with template's tightened versions.

- [ ] `protocols/brainstorm.md` — Replace with template version (no cookiecutter vars in this file, direct copy)
- [ ] `protocols/build.md` — Replace with template version (direct copy)

### Phase 2: Hook Scripts (relative paths + TARGET linking)
All three hooks switch from hardcoded paths to `get_project_root()` pattern.

- [ ] `.claude/hooks/capture-research.py` — Replace with template version (major: adds full TARGET bidirectional linking)
- [ ] `.claude/hooks/create-target.py` — Replace with template version (relative paths)
- [ ] `.claude/hooks/export-transcript.py` — Replace with template version (relative paths)

### Phase 3: Settings & Config
- [ ] `.claude/settings.json` — Switch absolute paths to relative paths
- [ ] `.gitignore` — Merge template rules (add `vault/.obsidian/`, `vault/sessions/transcripts/`; keep `.kh-config.json` ignore from main)
- [ ] `CLAUDE.md` — Update 3 occurrences of "kh directory"/"kh root" → "project root" (keep kh-specific header, no cookiecutter vars)

## Decisions
- LOCKED: Ignore transcripts in .gitignore — they're auto-exported, large, and disposable. Existing tracked ones stay but new ones won't be committed.

## Not Doing
- No cookiecutter vars in main (it's the dev workspace)
- No removal of existing vault content (sessions, decisions, research)
- No deletion of `.kh-config.json` ignore rule
- No changes to Obsidian plugin configs
