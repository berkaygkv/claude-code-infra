---
type: session
session: 24
date: 2026-02-04
project: kh
topics:
  - e2e-analysis
  - research-pipeline
  - target-system
  - io-strategy
  - pre-merge-validation
outcome: successful
continues_from: "[[sessions/session-23]]"
transcript: "[[sessions/transcripts/session-24]]"
decisions:
  - "[[decisions/research-pipeline-v2]]"
  - "[[decisions/io-strategy-v2]]"
research_spawned: []
tags:
  - session
---

## Handoff

### Context
Session 24 conducted thorough E2E analysis of the workflow before merging vault-redesign to main. Discovered 3 critical issues: export-transcript.py and create-target.py have hardcoded external vault paths, and MCP Obsidian plugin points to old external vault instead of kh/vault. Also identified that Session 6's LOCKED TARGET system was never implemented — the vault redesign simplified it away without formal unlocking. Restored TARGET with two-tier enforcement (quick lookup vs deep research). Fixed I/O strategy to be a hard constraint after behavioral failure (used Glob/Grep on vault instead of MCP).

### Decisions
- LOCKED: Research Pipeline v2 — Two tiers (quick lookup = no TARGET, deep research = TARGET required), automatic flow, bidirectional linking
- LOCKED: I/O Strategy v2 — Hard constraint: native Read/Write for known paths, MCP Obsidian for discovery/search
- LOCKED: MCP Vault Path — ALWAYS kh/vault, never external (reinforces vault-location decision)

### Memory
- MCP Obsidian config is in `~/.claude.json` under `mcpServers.obsidian`
- Current MCP path: `/home/berkaygkv/Dev/Docs/.obs-vault` (WRONG)
- Required MCP path: `/home/berkaygkv/Dev/headquarter/kh/vault`
- Session 6 TARGET decision was never implemented — now restored with v2
- export-transcript.py writes to external vault (broken)
- create-target.py writes to external vault (broken)
- capture-research.py correctly uses kh/vault (working)

### Next Steps
1. Fix MCP config (`~/.claude.json`) - change vault path to kh/vault
2. Fix `export-transcript.py` - use `vault/sessions/transcripts/`
3. Fix `create-target.py` - use `vault/research/targets/`
4. Update `capture-research.py` - add TARGET linking logic
5. Update `CLAUDE.md` - add Research Pipeline section with TARGET enforcement
6. Fix `meta.md` - wikilink casing `Sessions/` → `sessions/`
7. Create `vault/research/targets/` directory
8. Merge to main after fixes verified
