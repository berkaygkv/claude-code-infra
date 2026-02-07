---
type: decision
title: Ignore Transcripts in Git
status: locked
date: 2026-02-07
session: "[[sessions/session-26]]"
supersedes: null
superseded_by: null
related:
  - "[[decisions/template-distribution]]"
tags:
  - decision
---

## Decision
Add `vault/sessions/transcripts/` to `.gitignore`. Transcripts are auto-exported by the SessionEnd hook and should not be version-controlled.

## Rationale
Transcripts are large, auto-generated, and disposable. They bloat the repo without adding value to version history. Aligns with the template branch convention. Existing tracked transcripts remain in git history but new ones won't be committed.

## Alternatives Considered
- Keep tracking transcripts (current behavior) — rejected due to repo bloat and no meaningful review value
