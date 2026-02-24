---
type: state
project: kh
phase: idle
current_session: 51
updated: 2026-02-25
last_session: "[[sessions/session-51]]"
active_plan: null
focus: "Batch template sync or fix hardcoded vault paths"
plan_summary: ""
---

# State

## Objective
Build and maintain a knowledge infrastructure system that enables productive cold-starting across Claude Code sessions, with disciplined context persistence and minimal ceremony.

## Active

<!-- No active items -->

## Shaped

- Batch template sync S42–S51 [chore] — copy shared infrastructure changes to template worktree
- Fix hardcoded `vault/` paths in infrastructure files [small] — replace with dynamic path for cookiecutter compatibility

## Parked

<!-- No parked items -->

## Constraints
- [[decisions/template-distribution]] — dev in main, template in worktree
- [[decisions/vault-location]] — vault inside project root, git-tracked
- [[decisions/excalidraw-skill-design]] — 5 types, vault/canvas/, auto-detect
- [[decisions/io-strategy-v2]] — hard constraint: native for known paths, MCP for discovery
- [[decisions/ignore-transcripts]] — transcripts gitignored, auto-exported only
- [[decisions/system-overhaul-v1]] — 10 decisions: simplify research, brain vault, frontmatter, modes, scratch, voice
- [[decisions/research-format-v2]] — flat files, clean slugs, frontmatter, inline sources
- [[decisions/plan-protocol]] — standard format, lifecycle, creation/consumption in protocols
- [[decisions/validation-loop]] — spike assumptions, build from evidence, findings drive context
- [[decisions/stance-rewrite]] — behavioral stance rules, reason-first pattern
- [[decisions/template-vault-config]] — MCP preset in template, vault named after project slug
- [[decisions/scratch-collab-surface]] — shared working surface, Obsidian callouts, vault/scratch.md
- [[decisions/output-style-system]] — kh-brainstorm for brainstorm, default for build, manual toggle
- [[decisions/pm-lifecycle]] — Inbox → Shaped → Active → Done/Parked, appetite-gated, WIP-limited
