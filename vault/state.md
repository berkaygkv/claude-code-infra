---
type: state
project: kh
phase: idle
current_session: 29
updated: 2026-02-07
last_session: "[[sessions/session-29]]"
active_plan: null
focus: "Test /upgrade skill on downstream project, verify vault migration"
plan_summary: ""
---

# State

## Tasks
- [ ] Test /upgrade skill on another machine (existing cookiecutter project) #pending
- [ ] Verify capture-research hook works with new source extraction #pending
- [ ] Verify export-transcript hook works with relative paths #pending
- [ ] Test excalidraw skill on a different diagram type (flowchart or timeline) #pending
- [ ] Add bootstrap instructions to template README #pending
- [x] Full template sync to main #done
- [x] Rename "skb-layout-engine" to "kh-layout-engine" in layout.py #done
- [x] Build /upgrade skill for template-driven project migration #done
- [x] Sync upgrade skill to template branch #done

## Constraints
- [[decisions/template-distribution]] — dev in main, template in worktree
- [[decisions/vault-location]] — vault inside project root, git-tracked
- [[decisions/excalidraw-skill-design]] — 5 types, vault/canvas/, auto-detect
- [[decisions/research-pipeline-v2]] — TARGET required for deep research
- [[decisions/io-strategy-v2]] — hard constraint: native for known paths, MCP for discovery
- [[decisions/ignore-transcripts]] — transcripts gitignored, auto-exported only
