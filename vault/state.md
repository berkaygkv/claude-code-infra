---
type: state
project: kh
phase: build
current_session: 22
updated: 2026-02-04
last_session: "[[sessions/session-22]]"
active_plan: "[[plans/excalidraw-skill]]"
---

# State

## Focus
Implement excalidraw skill (Phase 1: Core Infrastructure).

## Plan
Excalidraw skill — 5 diagram types, auto-detect + manual invocation, modification support.

## Tasks
| Task | Status | Blocked By |
|------|--------|------------|
| Implement vault restructure | [status:: done] | - |
| Move vault inside kh/ | [status:: done] | - |
| Update path references | [status:: done] | - |
| E2E test /begin and /wrap | [status:: done] | - |
| Update /begin for two-file cold start | [status:: done] | - |
| Merge to main | [status:: parked] | excalidraw skill |
| Build excalidraw skill | [status:: pending] | - |

## Constraints
- [[decisions/template-distribution]] — dev in main, template in worktree
- [[decisions/vault-location]] — vault inside kh/, git-tracked
- [[decisions/excalidraw-skill-design]] — 5 types, vault/canvas/, auto-detect
