---
session: 12
date: '2026-01-21'
project: kh
topics:
  - plan-mode
  - mode-transitions
  - vault-io-strategy
  - community-workflows-research
outcome: successful
continues_from: session-11
transcript: "[[Sessions/transcripts/session-12]]"
tags:
  - session
---

## Handoff

### Context
This session defined the Plan/Build mode system for the framework. Started by validating a hybrid Vault I/O approach (native Read/Write for content, MCP for metadata operations). Then researched community plan structures (claude-code-pro, Manus three-file pattern, agentic-startup) before designing our own Obsidian-native Plan Schema. Concluded by locking explicit mode transition signals between Plan and Build modes.

### Decisions
- LOCKED: Vault I/O Strategy — Native Read/Write for content operations, MCP for metadata operations (frontmatter, search, tags, delete). Validated via 8-point test.
- LOCKED: Plan Schema — Plans live in `notes/plans/plan-{slug}.md`. Sections: Goal, Scope (In/Parked), Approach, Phases (checkbox tasks), Success Criteria, Related. Status lifecycle: draft → approved → in_progress → complete | abandoned.
- LOCKED: Plan Files Bypass Vault Write Discipline — Plans are operational documents, not archival. Create/update directly in vault during work.
- LOCKED: Mode Transitions — Two modes: Plan (alignment, no codebase writes) and Build (execution, all writes). Signals: "let's plan X" → Plan mode; "LGTM"/"approved" → Build mode; "revisit the plan" → back to Plan. Trivial tasks skip planning via direct instruction.

### Memory
- Research agent ID: aba2c19 (plan structures research) — can resume if needed
- Community patterns examined: claude-code-pro (spec-driven), Manus three-file (task_plan.md, findings.md, progress.md), agentic-startup (requirements/design/implementation), project-plan (7-step spec process)
- Key insight from research: "Context Window = RAM, Filesystem = Disk" — anything important must be written to files
- Plan mode constraint: No codebase writes, only plan file writes allowed

### Next Steps
- Add Plan Schema and Mode Transitions to schemas.md (full templates)
- Define Build mode structure (execution phase details)
- Add living CLAUDE.md pattern: at /wrap, review session for repeated instructions
