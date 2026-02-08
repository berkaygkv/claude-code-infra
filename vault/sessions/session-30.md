---
type: session
session: 30
date: 2026-02-08
mode: brainstorm
topics: [brain-vault, multi-agent-coordination, obsidian-sync, cross-machine-continuity, clawbot-integration]
outcome: successful
continues_from: "[[sessions/session-29]]"
decisions:
  - "[[decisions/brain-vault-integration]]"
---

# Session 30: Brain Vault — Multi-Agent Shared Knowledge Layer

## Context
Brainstormed and designed a central "brain" vault integration for cross-project, cross-machine knowledge sharing. The user has 4 devices (desktop, company laptop, Mac, iPhone) and an existing Obsidian vault at `~/Documents/Notes/` managed by Clawbot (KL), a 24/7 AI agent accessible via Telegram. Designed the architecture for both Claude Code and Clawbot to share the brain vault with explicit conventions: folder contracts, provenance tracking, search-before-create protocol, and inter-agent handoffs via `_sync/` folder. Configured and tested a second MCP Obsidian server (`brain`) in `~/.claude.json` — confirmed both vaults are accessible simultaneously with auto-namespaced tools (`mcp__obsidian__*` vs `mcp__brain__*`).

## Decisions

### Locked
- Brain vault integration — central knowledge layer at `~/Documents/Notes/`, on-demand only, never auto-loaded at `/begin`
- MCP config — second server `brain` in global `~/.claude.json`, tools namespaced `mcp__brain__*`
- Provenance tracking — `created_by`, `last_modified_by`, `source_session` in frontmatter for all brain files
- Search-before-create — both agents must search before creating to prevent duplicates
- Folder contracts — explicit per-folder write rules shared by both agents (inbox=user, projects/knowledge=both, artifacts=both-immutable, _sync=directional)
- Knowledge vs artifacts — knowledge = living docs, artifacts = immutable snapshots
- Brain structure — keep existing Clawbot structure, add only `_sync/` folder

### Open
- Detailed Clawbot coordination prompt still needs drafting (build task)
- CLAUDE.md Brain Vault section still needs writing (build task)
- Template sync after CLAUDE.md update

## Memory
- Brain vault path: `~/Documents/Notes/` (Obsidian Sync across all devices)
- Brain MCP server configured and tested in `~/.claude.json` — both vaults work simultaneously
- Clawbot is referred to as "KL" / "Külaude-Light" in brain vault docs
- Brain vault already has well-organized structure: `_meta/` (style guide, tag taxonomy, quick reference, templates, dashboards), `knowledge/`, `artifacts/`, `projects/`, `inbox/`, `people/`, `daily/`, `Excalidraw/`
- Tag taxonomy already defined by Clawbot: `topic/`, `type/`, `status/`, `project/`, `source/`, `effort/`, `priority/`, `confidence/`
- Frontmatter schema already defined by Clawbot: title, type, created, updated, status, confidence, tags, summary
- Either agent can create content — both must follow same conventions and search before creating
- Existing brain projects: spechunt, gastromind, neova (+ _archive)
- Existing brain knowledge: `tech/neo4j-knowledge-graphs.md`, `investments/` (asset-classes, global-markets, market-research, turkish-real-estate, watchlist)
- The project brief (`projects/{slug}/brief.md`) is the star artifact — accumulates thinking, rich enough for either agent to plan/build from
- `_sync/` handoffs are for explicit "this is ready for you" signals, not for every edit — provenance frontmatter handles audit trail

## Next Steps
1. `/begin build` — create `_sync/` folder structure in brain vault (folders + README)
2. Add `## Brain Vault` section to CLAUDE.md with access rules, folder contracts, provenance protocol
3. Draft Clawbot coordination prompt (detailed message user pastes into Telegram)
4. Sync CLAUDE.md changes to template branch
