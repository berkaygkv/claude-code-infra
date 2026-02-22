---
type: session
session: 43
date: 2026-02-22
mode: brainstorm
topics: [obsidian-cli, mcp-replacement, vault-knowledge-layer, bases, kepano-obsidian-skills]
outcome: successful
continues_from: "[[sessions/session-42]]"
decisions: []
---

# Session 43: Research Obsidian CLI + integration plan

## Context
Researched Obsidian's new CLI tool (shipped v1.12.0, Catalyst-only early access) to evaluate replacing our MCP Obsidian server. Ran two parallel deep research agents (CLI capabilities + codebase MCP audit) and discovered the CLI is far more than a file access layer — it's a runtime interface to Obsidian's metadata cache, link graph, Bases query engine, and plugin system. Also discovered our MCP Obsidian usage is essentially zero in practice (project vault MCP not even wired to this project; only brain vault `/meta` command actively uses MCP). Drafted a 3-phase integration plan with 4 spike assumptions. Blocked at end of session: CLI requires Catalyst license ($25 one-time) which user doesn't have yet.

## Decisions

### Locked
- (none — brainstorm/research session, plan still in draft)

### Open
- Whether to purchase Catalyst license ($25) to proceed with CLI integration
- Whether CLI integration plan should proceed or be parked until stable release

## Memory
- Obsidian CLI requires GUI running — no headless mode. Hard constraint for hooks (capture-research, export-transcript) which must stay on native file I/O
- CLI is Catalyst-only ($25 one-time, Insider tier). Catalyst does NOT include Sync — they're separate products
- macOS re-registration bug: CLI breaks after every Obsidian restart, requires manual toggle off/on
- `kepano/obsidian-skills` (10.3k stars, by Obsidian CEO) provides drop-in Claude Code skill files for CLI, Bases, markdown, canvas
- Our MCP Obsidian server at `~/.claude.json` points to `knowledge-graph-system/vault`, not this project's vault. No brain MCP server configured globally either
- The I/O strategy decision (io-strategy-v2) is policy on paper but disconnected from infrastructure — we use native Read/Write for everything in practice
- Key CLI value vectors: structured property search (`[type:decision] [status:locked]`), Bases database queries, link graph (orphans/unresolved/backlinks), template rendering, `eval` escape hatch
- Research files auto-captured to vault/research/ by hook (3 files this session)
- Plan at vault/plans/obsidian-cli-integration.md — 3 phases, 4 assumptions (A1: CLI reliability, A2: property search, A3: Bases dashboard, A4: templates)

## Next Steps
1. Decide: buy Catalyst ($25) to proceed, or park plan until CLI hits stable
2. If proceeding: create spike branch `spike/obsidian-cli`, execute Phase 1 (setup + smoke test)
3. If parked: sync trimmed files to template branch (carried over from session 42), test /upgrade skill
4. Excalidraw skill test still pending from session 42
