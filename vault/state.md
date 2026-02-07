---
type: state
project: kh
phase: idle
current_session: 28
updated: 2026-02-07
last_session: "[[sessions/session-28]]"
active_plan: null
focus: "Excalidraw skill improved — test on different diagram types, verify hooks"
plan_summary: ""
---

# State

## Tasks
- [x] Full template sync to main #done
- [x] Rename "skb-layout-engine" to "kh-layout-engine" in layout.py #done
- [ ] Verify capture-research hook works with new source extraction #pending
- [ ] Verify export-transcript hook works with relative paths #pending
- [ ] Test excalidraw skill on a different diagram type (flowchart or timeline) #pending

## Constraints
- [[decisions/template-distribution]] — dev in main, template in worktree
- [[decisions/vault-location]] — vault inside project root, git-tracked
- [[decisions/excalidraw-skill-design]] — 5 types, vault/canvas/, auto-detect
- [[decisions/research-pipeline-v2]] — TARGET required for deep research
- [[decisions/io-strategy-v2]] — hard constraint: native for known paths, MCP for discovery
- [[decisions/ignore-transcripts]] — transcripts gitignored, auto-exported only
