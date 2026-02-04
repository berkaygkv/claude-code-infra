---
type: state
project: kh
phase: build
current_session: 23
updated: 2026-02-04
last_session: "[[sessions/session-23]]"
active_plan: null
---

# State

## Focus
Merge vault-redesign branch to main.

## Plan
None — excalidraw skill complete.

## Tasks
| Task | Status | Blocked By |
|------|--------|------------|
| Implement vault restructure | [status:: done] | - |
| Move vault inside kh/ | [status:: done] | - |
| Update path references | [status:: done] | - |
| E2E test /begin and /wrap | [status:: done] | - |
| Update /begin for two-file cold start | [status:: done] | - |
| Build excalidraw skill | [status:: done] | - |
| Merge to main | [status:: pending] | - |

## Constraints
- [[decisions/template-distribution]] — dev in main, template in worktree
- [[decisions/vault-location]] — vault inside kh/, git-tracked
- [[decisions/excalidraw-skill-design]] — 5 types, vault/canvas/, auto-detect
