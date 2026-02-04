---
type: decision
title: Template Distribution
status: locked
date: 2026-01-25
session: "[[sessions/session-19]]"
supersedes: null
superseded_by: null
related: []
tags:
  - decision
  - distribution
---

## Decision
Git worktrees: `main` = dev workspace, `template` = cookiecutter; worktree at `../kh-template`

## Rationale
Need separate spaces for dev (with working /begin /wrap) and template (with cookiecutter placeholders). Two directories, two purposes.

## Alternatives Considered
- Template-first development with regeneration (too much friction)
- Abandon cookiecutter for setup script (throwing away working code)
