---
type: state
project: kh
phase: build
current_session: 32
updated: 2026-02-11
last_session: "[[sessions/session-32]]"
active_plan: null
focus: "Sync shared infrastructure to template branch, then verify hooks and upgrade skill on another machine"
plan_summary: ""
---

# State

## Tasks
- [x] Execute system overhaul plan (build mode) #done
- [ ] Sync shared infrastructure to template branch (post-overhaul) #pending
- [ ] Test /upgrade skill on another machine (existing cookiecutter project) #pending
- [ ] Verify capture-research hook works after rewrite #pending
- [ ] Verify export-transcript hook works with relative paths #pending
- [ ] Test excalidraw skill on a different diagram type (flowchart or timeline) #pending
- [ ] Add bootstrap instructions to template README #pending
- [x] Draft overhaul implementation plan #done
- [x] Design brain vault integration architecture #done
- [x] Configure and test brain MCP server in ~/.claude.json #done
- [x] Full template sync to main #done
- [x] Build /upgrade skill for template-driven project migration #done
- [x] Sync upgrade skill to template branch #done
- [x] Rename "skb-layout-engine" to "kh-layout-engine" in layout.py #done

## Constraints
- [[decisions/template-distribution]] — dev in main, template in worktree
- [[decisions/vault-location]] — vault inside project root, git-tracked
- [[decisions/excalidraw-skill-design]] — 5 types, vault/canvas/, auto-detect
- [[decisions/io-strategy-v2]] — hard constraint: native for known paths, MCP for discovery
- [[decisions/ignore-transcripts]] — transcripts gitignored, auto-exported only
- [[decisions/system-overhaul-v1]] — 10 decisions: simplify research, brain vault, frontmatter, modes, scratch, voice
