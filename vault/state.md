---
type: state
project: kh
phase: idle
current_session: 25
updated: 2026-02-05
last_session: "[[sessions/session-25]]"
active_plan: null
---

# State

## Focus
System operational. Restart Claude Code to activate MCP, then verify with /begin.

## Plan
None — vault-redesign merged, system ready for use.

## Tasks
| Task | Status | Blocked By |
|------|--------|------------|
| Implement vault restructure | [status:: done] | - |
| Move vault inside kh/ | [status:: done] | - |
| Update path references | [status:: done] | - |
| E2E test /begin and /wrap | [status:: done] | - |
| Update /begin for two-file cold start | [status:: done] | - |
| Build excalidraw skill | [status:: done] | - |
| Fix MCP config (vault path) | [status:: done] | - |
| Fix export-transcript.py | [status:: done] | - |
| Fix create-target.py | [status:: done] | - |
| Update capture-research.py (TARGET linking) | [status:: done] | - |
| Update CLAUDE.md (TARGET enforcement) | [status:: done] | - |
| Fix meta.md (wikilink casing) | [status:: done] | - |
| Create vault/research/targets/ | [status:: done] | - |
| Merge to main | [status:: done] | - |

## Constraints
- [[decisions/template-distribution]] — dev in main, template in worktree
- [[decisions/vault-location]] — vault inside kh/, git-tracked
- [[decisions/excalidraw-skill-design]] — 5 types, vault/canvas/, auto-detect
- [[decisions/research-pipeline-v2]] — TARGET required for deep research
- [[decisions/io-strategy-v2]] — hard constraint: native for known paths, MCP for discovery
