---
session: 19
date: '2026-01-25'
project: kh
topics:
  - cookiecutter-template
  - git-worktrees
  - meta-reflection
outcome: successful
continues_from: session-18
transcript: "[[Sessions/transcripts/session-19]]"
tags:
  - session
---

## Handoff

### Context

Converted the kh framework to a cookiecutter template and merged to main. Discovered this broke the dev environment—no `/begin` or `/wrap` available in the template structure. After multiple overcomplicated proposals, arrived at the simple solution: git worktrees. Reset main to pre-cookiecutter state, created `template` branch with worktree at `../kh-template`. Documented the failure pattern in meta-journal and added Project Template Schema to schemas.md.

### Decisions

- LOCKED: Template Distribution — Git worktrees: `main` = dev workspace, `template` = cookiecutter; worktree at `../kh-template`
- LOCKED: Template usage: `uvx cookiecutter gh:berkaygkv/claude-code-infra --checkout template`

### Memory

- Vault path: `/home/berkaygkv/Dev/Docs/.obs-vault/notes/`
- Template worktree: `../kh-template` (relative to kh repo)
- Template branch: `template` (pushed to origin)
- Main branch reset to commit `cb00ef1` (Session 18: bootstrap system)
- Files requiring cookiecutter placeholders: CLAUDE.md, vault/locked.md, vault/overview.md, vault/runbook.md, .claude/commands/begin.md

### Next Steps

1. Continue framework development in main branch (use normally)
2. When ready to update template, port changes to `kh-template/` directory
3. Replace concrete values with `{{ cookiecutter.xxx }}` placeholders when porting
