---
type: plan
title: "System Overhaul — Minimal Friction, Full Promise"
status: draft
date: 2026-02-11
session: "[[sessions/session-31]]"
phases_total: 5
phases_done: 0
---

# System Overhaul — Minimal Friction, Full Promise

Tighten the entire kh system: preserve every concept (earned over 30 sessions), fix implementations that add friction without value. Guiding principle: start at simplest viable form, let real friction drive complexity.

**Decisions driving this plan:** L1–L10 from session 31 scratch.md.

---

## Phase 1: CLAUDE.md — The Constitution

Rewrite CLAUDE.md as a tight constitution. Principles and architecture only. No duplicated procedures.

### Changes

**Section 1 (Core Identity):** Add Voice subsection after Functional Roles.

```markdown
### Voice
- Brevity over ceremony. One sentence if one sentence works.
- Opinions over hedging. Commit to a take.
- Direct over diplomatic. No "Great question!" — just answer.
- Wit welcome. Corporate praise banned.
- Challenge over compliance. If it's dumb, say so. Charm, not cruelty.
- Swearing allowed when it lands. Don't force it. Don't overdo it.

Be the collaborator worth talking to at 2am — not a corporate drone, not a sycophant.
```

**Section 2 (Operating Modes):** Two modes only.
- Remove Quick Fix row from table
- Remove `protocols/base.md` reference
- No argument = direct execution (implicit, not named)
- Keep mode transitions (brainstorm ↔ build)

**Section 3 (Memory Architecture):**
- Remove `templates/` from vault table
- Rewrite scratch.md as Session Changelog:

```markdown
### Session Changelog
**Path:** `scratch.md`

Running record of the current session:
- Initialized by /begin with session objective
- Updated by Claude on notable events (decisions, blockers, discoveries)
- Read by /wrap to build session handoff
- Survives context compression — the persistent session record
```

**Section 5 (Brain Vault):** Simplify to minimal rules.
- Keep: path, MCP server, on-demand access, `mcp__brain__*` tools
- Keep: search-before-create
- Keep: `created_by` in frontmatter
- Remove: `last_modified_by`, `source_session` (add when actually needed)
- Remove: folder contracts reference (parked)
- Remove: link to brain-vault-integration decision (will be superseded)

**Section 6 (Research Pipeline):** Simplify.
- Keep two-tier distinction (quick lookup vs deep research)
- Remove TARGET flow entirely
- Remove bidirectional linking
- Replace with: "Deep research → spawn deep-research agent. Quality standards in agent spec. Hook captures output to `vault/research/{slug}/`."

**Section 7 (Anti-Pattern Guards):** Delete entirely. These live in protocol files.

**Section 8 (Codebase vs Template):**
- Keep the structure explanation (main vs template branches)
- Remove the "HARD RULE" about syncing every session
- Replace with: "Sync when needed, not as a mandatory step."
- Remove `vault/schemas.md` and `vault/templates/` from sync list

**Section 10 (Session Lifecycle):**
- Add scratch.md initialization to /begin steps
- Update /wrap to "Read scratch.md changelog"
- Remove schema references

**Section 11 (Key Paths):** Remove templates/, add canvas/ if missing.

### Deliverable
Rewritten CLAUDE.md. Target: ~180 lines (down from 247).

---

## Phase 2: Protocols & Commands

### Protocols

**Delete:** `protocols/base.md`

**brainstorm.md:** No changes. Already has anti-pattern guards — it's the single source of truth for brainstorm behavior now that CLAUDE.md section 7 is gone.

**build.md:** One change:
- Update "Writes Allowed" table: scratch.md description from "Stage wrap content" → "Session changelog"

### Commands

**begin.md:**
- Remove Quick Fix mode references
- Remove schema reference at top
- No argument = "Direct execution — no protocol loaded"
- Add Step after Read State: "Initialize scratch.md"
- Scratch.md initialization format:
  ```markdown
  # Session Changelog

  ## Meta
  - session: {N}
  - mode: {brainstorm|build|direct}
  - objective: {focus from state.md or user's stated goal}

  ## Events
  - Session started — {objective}
  ```
- Update mode display: two modes + direct
  - No argument → "Direct execution — no protocol"
  - `brainstorm` → "Brainstorm mode — alignment before action"
  - `build` → "Build mode — executing approved plan"
- Tighten notes section: remove schema references

**wrap.md:**
- Remove schema reference at top
- Step 1: Read scratch.md changelog (synthesize decisions, memory, tasks from Events log)
- Step 4 (Create Decision Files): Simplified frontmatter:
  ```yaml
  ---
  type: decision
  title: {title}
  status: locked
  date: {YYYY-MM-DD}
  session: "[[sessions/session-{N}]]"
  supersedes: {only if applicable}
  tags: [decision]
  ---

  # {Title}

  {Free-form: rationale, context, alternatives — whatever's relevant}
  ```
  Keep `title` in frontmatter (dashboard queries need it). Remove `superseded_by`, `related`, forced sections.
- Step 6 (Create Session Note): Valid `mode` values: `brainstorm | build | direct`
- Step 7 (Reset Scratch): Update reset template:
  ```markdown
  # Session Changelog

  ## Meta
  - session: {N+1}

  ## Events
  ```
- Step 8 (Living CLAUDE.md Review): Keep
- Remove all "read schemas.md" instructions throughout

**meta.md:** Rewrite to target brain vault.
- Remove: `/tmp/kh-session.json` dependency
- Remove: MCP obsidian references (uses `mcp__brain__*` now)
- Session context: read from scratch.md Meta or conversation
- Individual files: `_meta/journal/{slug}.md` via `mcp__brain__write_note`
- Frontmatter: `type: meta`, `created_by: claude-code`, `date: YYYY-MM-DD`, `project: {current project}`
- Body: Background paragraph + **Insight:** line (keep the format, it's clean)
- Session reference: plain text ("Session 31, kh project") — not wikilinks (brain vault doesn't have project sessions)
- Drop interactive two-prompt flow — capture directly from conversation context
- Target: ~60 lines (down from 199)

### Deliverables
- Updated begin.md, wrap.md, meta.md
- Updated build.md
- Deleted protocols/base.md

---

## Phase 3: Research Pipeline

### deep-research.md (Agent Spec)

**Update stale references:**
- Fix output path (currently `/notes/Research/raw/` → `vault/research/`)
- Remove "Research tasks" reference (`/notes/Research/tasks/RESEARCH-XXX.md`)
- Remove "Dashboard" reference (`/notes/Research/dashboard.md`)

**Add quality checklist** (to "Quality Standards" section):
```
## Research Checklist
Before finalizing your output, verify:
- [ ] 5+ distinct sources consulted
- [ ] Official documentation checked first
- [ ] Information is current (2024-2026)
- [ ] Conflicting claims documented with explanation
- [ ] Concrete examples / code snippets included
- [ ] Limitations and gotchas section is substantive
- [ ] Recommendations are specific and actionable
- [ ] All source URLs included with brief descriptions
```

**Tighten "Your Role in the Framework" section:**
- Just: "Your output is automatically captured to the project's Obsidian vault by a SubagentStop hook. Focus purely on research quality."

### capture-research.py

**Gut to ~150-200 lines.** Keep:
- Agent type detection (web-research only)
- Transcript parsing (initial prompt, final summary)
- Simple source extraction (markdown links + bare URLs, no ranking)
- Slug generation
- Output folder creation (`vault/research/{timestamp}-{slug}/`)
- findings.md generation (frontmatter + summary + sources list)
- sources.md generation (flat list, no tiers)
- Processed agent tracking (dedup)
- Logging

**Simplified research-output frontmatter:**
```yaml
---
type: research-output
created: {YYYY-MM-DD}
topic: {extracted topic}
researcher: claude-deep-research
tags: [research]
---
```
Drop `target_link` (TARGET system removed) and `confidence` (never populated meaningfully).

**Remove:**
- All TARGET support (get_active_target, find_active_target, mark_target_complete)
- Domain authority tiers (HIGH_AUTHORITY_DOMAINS, MEDIUM_AUTHORITY_DOMAINS)
- Source ranking logic (extract_ranked_sources_from_summary, rank_sources_by_domain, get_domain_tier)
- ACTIVE_TARGET_FILE and RESEARCH_TARGETS_DIR constants

**Delete:** `create-target.py`

### Deliverables
- Updated deep-research.md
- Rewritten capture-research.py (~150-200 lines)
- Deleted create-target.py

---

## Phase 4: Vault Cleanup

### Update schemas.md content (before moving)
- Remove `research-target` schema entirely
- Update `research-output`: remove `target_link` and `confidence`, keep `type`, `created`, `topic`
- Update `decision`: simplified frontmatter per L7 (keep `title`, drop `superseded_by`, `related`, forced body sections)
- Update `plan`: keep `phases_done` alongside `phases_total` (dashboard needs both), drop `created` (use `date`), drop `project`
- Remove "Dashboard Queries Reference" section (dashboard is self-documenting)

### Move
- `vault/schemas.md` → `.claude/skills/upgrade/references/schemas.md`

### Delete
- `vault/templates/` (entire directory — 5 Obsidian Templater templates)
- `vault/meta-journal.md` (replaced by brain vault /meta)
- `vault/research/targets/` (empty except .gitkeep, TARGET system removed)

### Update dashboard.md
- Remove "Open Research" section entirely (queried `research/targets` which no longer exists)
- Other sections unaffected: decisions query uses `title`/`status`/`date` (all kept), plan query uses `title`/`status`/`phases_done`/`phases_total` (all kept)

### Decision Files

**Create new decision:** `vault/decisions/system-overhaul-v1.md`
- Supersedes: `research-pipeline-v2`, `brain-vault-integration`
- Documents: simplified research (no TARGETs), simplified brain vault (minimal rules), simplified decision format, two-mode system, scratch.md as changelog, voice section
- Uses the new simplified frontmatter format (eating our own dogfood)

**Update superseded decisions:**
- `research-pipeline-v2.md`: add `superseded_by` pointing to new decision
- `brain-vault-integration.md`: add `superseded_by` pointing to new decision

### Migration policy
- Existing decisions: leave as-is (old format is valid, not worth migrating)
- Existing research outputs: leave as-is (all have `target: null`, no breakage)

### Deliverables
- Updated + moved schemas.md
- Updated dashboard.md
- Deleted templates/, meta-journal, targets/
- New + updated decision files

---

## Phase 5: Validation

### Smoke test
1. Run `/begin brainstorm` — verify cold start loads correctly, scratch.md initialized
2. Run `/begin build` — verify plan loading works
3. Run `/begin` (no arg) — verify direct execution, no protocol crash, scratch.md initialized with `mode: direct`
4. Trigger a deep-research agent — verify capture hook works without TARGET
5. Run `/meta` — verify it writes to brain vault at `_meta/journal/`
6. Run `/wrap` — verify session handoff, decision creation, scratch reset all work
7. Verify dashboard renders all sections without errors (Open Research gone, rest intact)

### Check
- No broken wikilinks in state.md constraints
- No orphaned references to deleted files (schemas.md, templates/, meta-journal, targets/)
- `git status` is clean (only intentional changes)

### Deliverable
All smoke tests pass. System operational.

---

## Execution Notes

- **Phase order matters:** Phase 1 first (everything references CLAUDE.md), then 2-4 can be parallelized, Phase 5 last
- **No new features:** This is purely tightening. If we discover something missing, note it for a future session.
- **Decision format:** Start using the new simplified format immediately (Phase 4 decision file)
- **Complexity note:** Phase 3 (capture-research.py rewrite) is the highest-risk item — essentially a new script. Phases 1, 2, 4 are file edits and deletions.
