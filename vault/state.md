---
type: state
project: kh
phase: idle
current_session: 41
updated: 2026-02-16
last_session: "[[sessions/session-41]]"
active_plan: null
focus: "Test /upgrade skill on another machine, test excalidraw on different diagram type"
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
- [x] Mark superseded decisions with `status: superseded` (vault-io-strategy.md, research-pipeline-v2.md) #done
- [ ] Test /upgrade skill on another machine (existing cookiecutter project) #pending
- [x] Verify capture-research hook works after rewrite #done
- [x] Verify export-transcript hook works with relative paths #done
- [ ] Test excalidraw skill on a different diagram type (flowchart or timeline) #pending
- [x] Add bootstrap instructions to template README #done
- [x] Implement research format v2 — modify capture-research hook + update CLAUDE.md #done
- [x] Template overhaul — vault renamed to slug, .mcp.json, CLAUDE.md updated, all paths synced #done

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
- [[decisions/template-vault-config]] — MCP preset in template, vault named after project slug
