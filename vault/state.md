---
type: state
project: kh
phase: brainstorm
current_session: 26
updated: 2026-02-07
last_session: "[[sessions/session-26]]"
active_plan: "[[plans/sync-template-to-main]]"
---

# State

## Focus
Execute sync plan: bring template improvements (protocols, hooks, config) back into main.

## Plan
[[plans/sync-template-to-main]] — 3 phases: protocols, hooks, config. Locked and approved.

## Tasks
| Task | Status | Blocked By |
|------|--------|------------|
| Sync protocols from template | [status:: todo] | - |
| Sync hook scripts from template | [status:: todo] | - |
| Sync settings & config from template | [status:: todo] | - |

## Constraints
- [[decisions/template-distribution]] — dev in main, template in worktree
- [[decisions/vault-location]] — vault inside kh/, git-tracked
- [[decisions/excalidraw-skill-design]] — 5 types, vault/canvas/, auto-detect
- [[decisions/research-pipeline-v2]] — TARGET required for deep research
- [[decisions/io-strategy-v2]] — hard constraint: native for known paths, MCP for discovery
- [[decisions/ignore-transcripts]] — transcripts gitignored, auto-exported only
