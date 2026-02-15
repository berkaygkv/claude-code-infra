---
type: state
project: kh
phase: idle
current_session: 40
updated: 2026-02-15
last_session: "[[sessions/session-40]]"
active_plan: null
focus: "Pending tasks: supersede old decisions, test upgrade skill, verify hooks, template README"
plan_summary: null
---

# State

## Tasks
- [x] Execute system overhaul plan (build mode) #done
- [x] Sync shared infrastructure to template branch (post-overhaul) #done
- [x] Draft overhaul implementation plan #done
- [x] Design brain vault integration architecture #done
- [x] Configure and test brain MCP server in ~/.claude.json #done
- [x] Full template sync to main #done
- [x] Build /upgrade skill for template-driven project migration #done
- [x] Sync upgrade skill to template branch #done
- [x] Rename "skb-layout-engine" to "kh-layout-engine" in layout.py #done
- [x] Test validation loop on a real task — shipped qualitative validation system (session 39) #done
- [x] Set up knowledge base project repo at ~/Dev/knowledge-base #done
- [ ] Build Phase 1 — entity resolution spike (in knowledge-base project, not here) #moved
- [x] Update brainstorm.md and build.md protocols with validation loop #done
- [x] Close failure/recovery gaps in validation system (plan rejection, plan failure, thrashing detection) #done
- [ ] Mark superseded decisions with `status: superseded` (vault-io-strategy.md, research-pipeline-v2.md) #pending
- [ ] Test /upgrade skill on another machine (existing cookiecutter project) #pending
- [ ] Verify capture-research hook works after rewrite #pending
- [ ] Verify export-transcript hook works with relative paths #pending
- [ ] Test excalidraw skill on a different diagram type (flowchart or timeline) #pending
- [ ] Add bootstrap instructions to template README #pending
- [ ] Implement research format v2 — modify capture-research hook + update CLAUDE.md #pending

## Constraints
- [[decisions/template-distribution]] — dev in main, template in worktree
- [[decisions/vault-location]] — vault inside project root, git-tracked
- [[decisions/excalidraw-skill-design]] — 5 types, vault/canvas/, auto-detect
- [[decisions/io-strategy-v2]] — hard constraint: native for known paths, MCP for discovery
- [[decisions/ignore-transcripts]] — transcripts gitignored, auto-exported only
- [[decisions/system-overhaul-v1]] — 10 decisions: simplify research, brain vault, frontmatter, modes, scratch, voice
- [[decisions/research-format-v2]] — flat files, clean slugs, frontmatter, inline sources
- [[decisions/plan-protocol]] — standard format, lifecycle, creation/consumption in protocols
- [[decisions/validation-loop]] — spike assumptions, build from evidence, findings drive context
- [[decisions/stance-rewrite]] — behavioral stance rules, reason-first pattern
