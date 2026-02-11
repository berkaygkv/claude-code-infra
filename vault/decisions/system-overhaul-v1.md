---
type: decision
title: "System Overhaul v1 — Minimal Friction, Full Promise"
status: locked
date: 2026-02-11
session: "[[sessions/session-31]]"
supersedes: "[[decisions/research-pipeline-v2]], [[decisions/brain-vault-integration]]"
tags: [decision]
---

# System Overhaul v1

Bundle of 10 decisions tightening the kh system. Every concept earned over 30 sessions stays — implementations that add friction without value get simplified.

## Decisions

**L1: Single source of truth per rule.** Each rule lives in ONE place. CLAUDE.md = constitution. Protocols = mode behavior. Commands = execution. No duplication.

**L2: schemas.md moves to `.claude/skills/upgrade/references/`.** Infrastructure reference for migration, not project content.

**L3: Delete vault/templates/.** Obsidian Templater templates unused — vault files created by Claude via commands/hooks.

**L4: Two modes only (brainstorm/build).** No argument to /begin = direct execution. Delete protocols/base.md. Session mode value: `direct`.

**L5: Brain vault starts minimal.** `mcp__brain__*` tools, search before creating, `created_by` in frontmatter. No _sync/, no folder contracts, no Clawbot prompt.

**L6: /meta targets brain vault.** Individual files at `_meta/journal/{slug}.md` via `mcp__brain__write_note`. Plain-text session references (no cross-vault wikilinks).

**L7: Simplified decision/plan frontmatter.** Decisions: `type`, `title`, `status`, `date`, `session`, `supersedes` (when applicable). Free-form body. Plans: keep `phases_total`, `phases_done`, `status`. Drop other ceremony.

**L8: scratch.md redesigned as session changelog.** Running record with Meta (session, mode, objective) + Events log. Not a staging area. /begin initializes, Claude appends, /wrap reads.

**L9: Research pipeline simplified.** Quality standards in agent spec (checklist). capture-research.py gutted to ~150-200 lines. No TARGETs, no source ranking tiers. create-target.py deleted.

**L10: Voice section in CLAUDE.md.** Personality block after Functional Roles: brevity, opinions, directness, wit, swearing-when-it-lands. Architecture stays dry.

## Parked

- P1: _sync/ folder and Clawbot coordination — revisit when brain vault has actual content
- P2: TARGET bidirectional linking — revisit if research output management hurts
- P3: Template sync as hard rule — sync when needed, not mandatory

## Context

The pattern across all friction: protocol designed for general case before specific case was encountered. 30 sessions of earned concepts wrapped in too much ceremony. This overhaul cuts the wrapper, keeps the core. Implementation plan: `vault/plans/system-overhaul.md` (5 phases).
