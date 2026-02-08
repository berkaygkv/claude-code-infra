---
type: decision
title: "Brain Vault Integration — Multi-Agent Shared Knowledge Layer"
status: locked
date: 2026-02-08
session: "[[sessions/session-30]]"
supersedes: null
superseded_by: null
related:
  - "[[decisions/io-strategy-v2]]"
tags:
  - decision
  - brain-vault
---

## Decision

Integrate a central "brain" vault (`~/Documents/Notes/`) as a cross-project, cross-machine, multi-agent knowledge layer accessible to both Claude Code and Clawbot (KL). The brain vault is synced via Obsidian Sync across all devices (desktop, company laptop, Mac, iPhone).

### Architecture

- **MCP config:** Second MCP server `brain` in `~/.claude.json` pointing to `~/Documents/Notes/`. Tools namespaced as `mcp__brain__*`. Global config so it's available from any project.
- **Access pattern:** Strictly on-demand. Never auto-loaded at `/begin`. Claude Code queries the brain only when the user explicitly requests it.
- **Provenance:** All brain vault files include `created_by`, `last_modified_by`, `source_session` in frontmatter. Values: `clawbot` | `claude-code` | `berkay`.
- **Search-before-create:** Both agents MUST search the brain vault before creating any file. If content exists, update it. Never create parallel files.

### Folder Contracts

| Folder | Write Authority | Rule |
|--------|----------------|------|
| `inbox/` | User writes, Clawbot processes | Claude Code reads only |
| `projects/{slug}/brief.md` | Both agents | One brief per project, either creates/updates |
| `knowledge/{domain}/` | Both agents | Living reference docs, updated as understanding deepens |
| `artifacts/{type}/` | Both agents | Immutable time-bound outputs, never update old ones |
| `_sync/for-claude-code/` | Clawbot writes | Claude Code reads + acknowledges |
| `_sync/for-clawbot/` | Claude Code writes | Clawbot reads + acknowledges |
| `people/`, `daily/` | Clawbot/user primary | Claude Code reads only |

### Key Distinctions

- **Knowledge** = living docs that evolve over time (reference material, patterns, how things work)
- **Artifacts** = immutable snapshots tied to a specific moment/question (analyses, calculations, summaries)
- **Project briefs** (`projects/{slug}/brief.md`) = the definitive project document, accumulates thinking over time, either agent creates/updates

### Brain Structure

Keep Clawbot's existing structure unchanged. Only addition: `_sync/` folder with `for-claude-code/` and `for-clawbot/` subfolders for inter-agent handoffs.

## Rationale

The kh framework's session handoff architecture already supports cold starts across machines — but all context is project-scoped. Cross-project knowledge (ideas, career plans, investment research, technical patterns, project seeds) had no home. The brain vault fills this gap by providing a persistent, Obsidian-synced knowledge layer that both AI agents can read/write with shared conventions. Clawbot already maintained this vault; the integration makes it accessible to Claude Code sessions on demand.

## Alternatives Considered

- **Git-only sync (no Obsidian Sync):** Simpler but no iPhone access, requires manual git discipline. Rejected because Obsidian Sync is already paid for and provides seamless cross-device access.
- **Vault extraction from git (symlink approach):** Move project vault out of git, use Obsidian Sync for both. Rejected because it breaks the existing `vault-location` decision and adds setup complexity per machine.
- **Single vault (merge brain into project):** Would create scope pollution. Rejected — the brain is cross-project by nature.
- **Clawbot writes only, Claude Code reads only:** Too restrictive. User may ask Claude Code to create project briefs or knowledge notes directly. Both agents need write access with coordination protocol.
