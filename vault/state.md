---
type: state
project: kh
phase: build
current_session: 49
updated: 2026-02-24
last_session: "[[sessions/session-49]]"
active_plan:
focus: "Brainstorm shared language / operational glossary, or batch template sync"
plan_summary:
---

# State

## Objective
Build and maintain a knowledge infrastructure system that enables productive cold-starting across Claude Code sessions, with disciplined context persistence and minimal ceremony.

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
- [x] Update brainstorm.md and build.md protocols with validation loop #done
- [x] Close failure/recovery gaps in validation system (plan rejection, plan failure, thrashing detection) #done
- [x] Mark superseded decisions with `status: superseded` (vault-io-strategy.md, research-pipeline-v2.md) #done
- [x] Verify capture-research hook works after rewrite #done
- [x] Verify export-transcript hook works with relative paths #done
- [x] Add bootstrap instructions to template README #done
- [x] Implement research format v2 — modify capture-research hook + update CLAUDE.md #done
- [x] Template overhaul — vault renamed to slug, .mcp.json, CLAUDE.md updated, all paths synced #done
- [x] Trim /begin command + protocols + CLAUDE.md — 119 lines cut, zero info loss #done
- [x] Redesign scratch.md — from changelog to reasoning surface with objective lifecycle #done
- [x] Design output style for chat formatting — kh-brainstorm style + mode integration #done
- [x] Draft gemwrap video research plan #done
- [x] Build /research-video skill (SKILL.md, playbook, gemwrap-reference, CLAUDE.md update) #done
- [x] Test /research-video skill with a real YouTube video #done
- [x] Design collaborative scratch surface — shared working surface with Obsidian callouts #done
- [x] Implement collaborative scratch surface (plan completed, session 49) #done
- [ ] Sync trimmed files to template branch (CLAUDE.md, begin.md, brainstorm.md, build.md) #pending
- [ ] Sync session 44 changes to template branch (CLAUDE.md, begin.md, wrap.md, brainstorm.md, build.md) #pending
- [ ] Sync research-video skill + CLAUDE.md to template branch #pending
- [ ] Sync output style + protocol updates to template branch #pending
- [ ] Sync scratch-collab-surface changes to template branch #pending
- [ ] Design project management lifecycle (idea funnel, prioritization, strategic layer) #pending
- [ ] Design shared language / operational glossary #pending
- [ ] Fix hardcoded `vault/` paths in infrastructure files (begin.md, wrap.md) — breaks when vault name differs from `vault/` (e.g. cookiecutter dynamic naming) #pending

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
- [[decisions/scratch-collab-surface]] — shared working surface, Obsidian callouts, vault/scratch.md
- [[decisions/output-style-system]] — kh-brainstorm for brainstorm, default for build, manual toggle
