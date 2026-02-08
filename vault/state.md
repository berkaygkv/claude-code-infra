---
type: state
project: kh
phase: brainstorm
current_session: 30
updated: 2026-02-08
last_session: "[[sessions/session-30]]"
active_plan: null
focus: "Build brain vault integration: _sync/ folder, CLAUDE.md section, Clawbot prompt, template sync"
plan_summary: ""
---

# State

## Tasks
- [ ] Create _sync/ folder structure in brain vault (folders + README) #pending
- [ ] Add Brain Vault section to CLAUDE.md #pending
- [ ] Draft Clawbot coordination prompt (for user to paste into Telegram) #pending
- [ ] Sync CLAUDE.md changes to template branch #pending
- [ ] Test /upgrade skill on another machine (existing cookiecutter project) #pending
- [ ] Verify capture-research hook works with new source extraction #pending
- [ ] Verify export-transcript hook works with relative paths #pending
- [ ] Test excalidraw skill on a different diagram type (flowchart or timeline) #pending
- [ ] Add bootstrap instructions to template README #pending
- [x] Full template sync to main #done
- [x] Rename "skb-layout-engine" to "kh-layout-engine" in layout.py #done
- [x] Build /upgrade skill for template-driven project migration #done
- [x] Sync upgrade skill to template branch #done
- [x] Design brain vault integration architecture #done
- [x] Configure and test brain MCP server in ~/.claude.json #done

## Constraints
- [[decisions/template-distribution]] — dev in main, template in worktree
- [[decisions/vault-location]] — vault inside project root, git-tracked
- [[decisions/excalidraw-skill-design]] — 5 types, vault/canvas/, auto-detect
- [[decisions/research-pipeline-v2]] — TARGET required for deep research
- [[decisions/io-strategy-v2]] — hard constraint: native for known paths, MCP for discovery
- [[decisions/ignore-transcripts]] — transcripts gitignored, auto-exported only
- [[decisions/brain-vault-integration]] — on-demand brain vault, dual MCP, search-before-create, provenance tracking
