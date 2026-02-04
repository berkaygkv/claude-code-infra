---
type: decision
title: Vault Location
status: locked
date: 2026-02-04
session: "[[sessions/session-21]]"
supersedes: null
superseded_by: null
related:
  - "[[decisions/template-distribution]]"
tags:
  - decision
  - infrastructure
---

## Decision
The vault/ directory lives inside the kh/ codebase, not at an external Obsidian path.

## Rationale
- Git-tracked: all vault content versioned with the codebase
- Self-contained: no external dependencies or path fragility
- Portable: clone the repo, get everything

## Alternatives Considered
- External Obsidian vault at ~/Dev/Docs/.obs-vault/notes/ — rejected due to path fragility and not being git-tracked with the codebase
