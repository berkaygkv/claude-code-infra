---
type: state
project: kh
phase: build
current_session: 24
updated: 2026-02-04
last_session: "[[sessions/session-24]]"
active_plan: null
---

# State

## Focus
Fix pre-merge issues: MCP vault path, hook scripts, TARGET system implementation.

## Plan
None — implementation tasks defined in session-24 handoff.

## Tasks
| Task | Status | Blocked By |
|------|--------|------------|
| Implement vault restructure | [status:: done] | - |
| Move vault inside kh/ | [status:: done] | - |
| Update path references | [status:: done] | - |
| E2E test /begin and /wrap | [status:: done] | - |
| Update /begin for two-file cold start | [status:: done] | - |
| Build excalidraw skill | [status:: done] | - |
| Fix MCP config (vault path) | [status:: pending] | - |
| Fix export-transcript.py | [status:: pending] | - |
| Fix create-target.py | [status:: pending] | - |
| Update capture-research.py (TARGET linking) | [status:: pending] | - |
| Update CLAUDE.md (TARGET enforcement) | [status:: pending] | - |
| Fix meta.md (wikilink casing) | [status:: pending] | - |
| Create vault/research/targets/ | [status:: pending] | - |
| Merge to main | [status:: pending] | all above |

## Constraints
- [[decisions/template-distribution]] — dev in main, template in worktree
- [[decisions/vault-location]] — vault inside kh/, git-tracked
- [[decisions/excalidraw-skill-design]] — 5 types, vault/canvas/, auto-detect
- [[decisions/research-pipeline-v2]] — TARGET required for deep research
- [[decisions/io-strategy-v2]] — hard constraint: native for known paths, MCP for discovery
