---
type: state
project: kh
phase: build
current_session: 21
updated: 2026-02-04
last_session: "[[sessions/session-21]]"
active_plan: null
---

# State

## Focus
Merge vault-redesign branch to main.

## Plan
None

## Tasks
| Task | Status | Blocked By |
|------|--------|------------|
| Implement vault restructure | [status:: done] | - |
| Move vault inside kh/ | [status:: done] | - |
| Update path references | [status:: done] | - |
| E2E test /begin and /wrap | [status:: done] | - |
| Update /begin for two-file cold start | [status:: done] | - |
| Merge to main | [status:: pending] | - |

## Constraints
- [[decisions/template-distribution]] — dev in main, template in worktree
- [[decisions/vault-location]] — vault inside kh/, git-tracked
