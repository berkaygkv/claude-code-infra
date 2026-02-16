---
type: session
session: 41
date: 2026-02-16
mode: brainstorm
topics: [housekeeping, research-format-v2, template-overhaul, vault-auto-discovery]
outcome: successful
continues_from: "[[sessions/session-40]]"
decisions: ["[[decisions/template-vault-config]]"]
---

# Session 41: Housekeeping sweep + template vault overhaul

## Context
Cleared the pending kh task backlog: superseded old decisions, implemented research format v2 (flat files with frontmatter and inline sources), added vault auto-discovery to both hooks, and did a full template overhaul — renaming the vault directory to use the project slug, adding a preset Obsidian MCP server, rewriting the README with bootstrap instructions, and updating every vault path reference across CLAUDE.md, commands, protocols, and skills.

## Decisions

### Locked
- Obsidian MCP preset in template — project vault only, brain vault excluded (personal/machine-specific)
- Vault directory uses `{{ cookiecutter.project_slug }}` — CLI-friendly, gives meaningful Obsidian vault name
- Both hooks use `.obsidian/` auto-discovery — works regardless of vault directory name

### Open
- (none)

## Memory
- Template CLAUDE.md section 7 is now "Upgrading" (one-liner) — the old "Codebase vs Template" section was kh-dev-specific
- CLAUDE.md removed from `_copy_without_render` in cookiecutter.json — no more literal `{{ }}` in template CLAUDE.md
- Template diverges from main on vault path references (slug vs `vault/`) — this is expected and manageable during sync
- Upgrade SKILL.md now discovers vault at runtime (Step 0) — no more hardcoded `vault/` paths
- Schemas.md research section updated to flat format (no more directory-per-research)
- Template dashboard removed stale "Open Research" section (queried defunct `research/targets`)

## Next Steps
1. Test /upgrade skill on another machine (existing cookiecutter project)
2. Test excalidraw skill on a different diagram type
3. Knowledge-base project Phase 1 — entity resolution spike (separate repo)
