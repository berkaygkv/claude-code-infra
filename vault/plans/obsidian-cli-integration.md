---
type: plan
title: "Integrate Obsidian CLI as vault knowledge layer"
status: draft
date: 2026-02-22
session: "[[sessions/session-43]]"
phases_total: 3
phases_done: 0
assumptions_total: 4
assumptions_validated: 0
---

# Integrate Obsidian CLI as Vault Knowledge Layer

## Goal

Replace our file-level vault access with Obsidian CLI to gain structured property search, Bases database queries, link graph intelligence, template rendering, and eval-based extensibility. Validate via a spike branch that tests every capability against our real vault before committing to migration.

## Scope

**Includes:** CLI setup & registration, capability testing across all value vectors (Bases, templates, search, link graph, eval, daily notes), kepano/obsidian-skills installation, I/O strategy rewrite, migration of `/meta` command from MCP brain to CLI, vault health check prototype.

**Excludes:** Headless/CI scenarios (hooks stay on native file I/O — that's a feature, not a limitation), MCP server removal (defer until CLI proves stable past early access), template branch sync (separate task after plan completes).

## Assumptions

### A1: CLI works reliably on this machine — HIGH

Obsidian 1.12+ is installed, Catalyst license is active, CLI registration succeeds on macOS, and commands return valid JSON for our vault. The macOS re-registration bug (CLI breaks after Obsidian restart) has a workable mitigation.

- **Spike:** Install/enable CLI, run 10+ commands against the live vault, restart Obsidian and test re-registration, script a health check.
- **Inspectable output:** Terminal output showing each command + response. Documented re-registration workaround.
- **Findings:** _pending_
- **Impact:** If fails → plan abandoned. CLI is unusable without reliable registration.

### A2: Property search replaces MCP/grep for discovery — CRITICAL

`obsidian search query="[type:decision] [status:locked]" format=json` returns structured results matching our frontmatter conventions. This is the core value proposition — treating frontmatter as a query language.

- **Spike:** Run property searches for every frontmatter pattern we use: `type` (session/decision/plan/research), `status` (locked/draft/active/completed), `date` ranges, combined filters. Compare results to what grep finds.
- **Inspectable output:** Side-by-side comparison table: grep results vs CLI results for 5+ queries. Accuracy, completeness, response format.
- **Findings:** _pending_
- **Impact:** If fails → direction-level. The core value proposition collapses and CLI becomes a nice-to-have, not a system component.

### A3: Bases can serve as a queryable project dashboard — HIGH

A `.base` file using our existing frontmatter properties (`type`, `status`, `date`, `session`) produces a structured view exportable via `base:query format=json`. This could replace manual state.md task tracking for project-level queries.

- **Spike:** Create `vault/dashboard.base` with filters for sessions, decisions, plans. Query via CLI. Assess: does the output contain what `/begin` needs for cold start?
- **Inspectable output:** The `.base` file itself + raw JSON output from `base:query`. Annotated assessment of what it captures vs what state.md provides.
- **Findings:** _pending_
- **Impact:** If fails → task-level. We keep state.md as-is; Bases becomes informational-only (nice for Obsidian UI, not critical for Claude).

### A4: Template rendering produces correct session/decision files — MEDIUM

`obsidian create name=X template=Y silent` generates files with correct frontmatter using our vault's template conventions. Core Templates variables (`{{title}}`, `{{date}}`) substitute correctly.

- **Spike:** Create Obsidian templates for session, decision, and plan files. Test CLI-based creation. Verify frontmatter, file placement, and variable substitution. Test Templater auto-trigger if Templater is installed.
- **Inspectable output:** Generated files vs manually-created reference files. Diff showing any gaps.
- **Findings:** _pending_
- **Impact:** If fails → task-level. We keep manual frontmatter generation; minor convenience loss.

## Phases

### Phase 1: Setup + smoke test all capabilities
**Targets:** A1 (CLI reliability)
**Type:** Spike
**Fits in one session:** Yes

Prerequisites: Obsidian 1.12+ running, Catalyst license active.

- [ ] Verify Obsidian version ≥ 1.12 and Catalyst status
- [ ] Enable CLI in Settings → General → Command line interface
- [ ] Complete registration, verify PATH (`which obsidian` or `obsidian version`)
- [ ] Create spike branch: `spike/obsidian-cli`
- [ ] Smoke test — run each command category against live vault:
  - [ ] `obsidian files format=json` — list vault files
  - [ ] `obsidian read file="state"` — read a known file
  - [ ] `obsidian search query="decision" format=json` — full-text search
  - [ ] `obsidian search query="[type:decision]" format=json` — property search
  - [ ] `obsidian properties file="state" format=json` — read frontmatter
  - [ ] `obsidian property:set file="state" key=test_key value=test_value` — set property (revert after)
  - [ ] `obsidian tags` — list all tags
  - [ ] `obsidian backlinks file="state"` — link graph
  - [ ] `obsidian orphans` — orphaned notes
  - [ ] `obsidian unresolved` — broken links
  - [ ] `obsidian eval code="app.vault.getFiles().length"` — eval
  - [ ] `obsidian daily:read` — daily note (if configured)
- [ ] Test re-registration: quit Obsidian, relaunch, test CLI, document workaround
- [ ] Install kepano/obsidian-skills via `/plugin marketplace add kepano/obsidian-skills` (or manual copy)
- [ ] Write smoke test results to `vault/research/20260222-obsidian-cli-spike.md`

**Deliverable:** Documented smoke test with pass/fail per command. CLI reliability assessment. kepano/obsidian-skills installed.

### Phase 2: Deep validation of value vectors
**Targets:** A2 (property search), A3 (Bases dashboard), A4 (template rendering)
**Type:** Spike
**Fits in one session:** Yes (assuming Phase 1 passed)

#### Property Search (A2)
- [ ] Run 5+ property search queries matching our frontmatter patterns:
  - `[type:decision] [status:locked]`
  - `[type:session]` with date filtering
  - `[type:plan] [status:active]`
  - `[type:research]`
  - Combined: `[type:decision] [status:locked] [date:>2026-02-01]`
- [ ] Run equivalent grep/glob queries for the same data
- [ ] Compare: accuracy, completeness, output format, speed
- [ ] Test `search:context` — does contextual search add value for Claude's cold start?
- [ ] Document which queries CLI wins, ties, or loses vs grep

#### Bases Dashboard (A3)
- [ ] Create `vault/dashboard.base` with:
  - Session index (type: session, sorted by date desc)
  - Decision registry (type: decision, grouped by status)
  - Plan tracker (type: plan, with phase progress)
- [ ] Run `obsidian base:query name="dashboard" format=json` — capture output
- [ ] Test `sed '1d'` workaround for debug message bug
- [ ] Assess: does the JSON output provide what `/begin` needs?
- [ ] Test from Obsidian UI: does the Base render correctly?

#### Template Rendering (A4)
- [ ] Create Obsidian templates in vault (or a templates folder):
  - `_templates/Session.md` — session handoff template with `{{title}}`, `{{date}}`
  - `_templates/Decision.md` — decision file template
  - `_templates/Plan.md` — plan file template
- [ ] Test CLI creation: `obsidian create name="Test Session" path="vault/sessions/" template="Session" silent`
- [ ] Verify: frontmatter correctness, variable substitution, file placement
- [ ] If Templater installed: test auto-trigger on CLI-created files
- [ ] Clean up test files

#### Link Graph
- [ ] Run `obsidian orphans format=json` — identify orphaned vault notes
- [ ] Run `obsidian unresolved format=json` — find broken wikilinks
- [ ] Run `obsidian backlinks file="io-strategy-v2" format=json` — trace decision dependencies
- [ ] Prototype vault health check script (5-10 lines bash):
  ```bash
  echo "Orphans:"; obsidian orphans format=json
  echo "Broken links:"; obsidian unresolved format=json
  echo "Unreferenced decisions:"; obsidian search query="[type:decision]" format=paths | while read p; do ...
  ```

#### Eval
- [ ] `obsidian eval code="app.vault.getFiles().length"` — basic
- [ ] `obsidian eval code="JSON.stringify(app.metadataCache.getFileCache(app.vault.getAbstractFileByPath('vault/state.md'))?.frontmatter)"` — frontmatter via cache
- [ ] Test: can eval return data the CLI commands can't? (e.g., plugin state, computed properties)

- [ ] Write all findings to `vault/research/20260222-obsidian-cli-spike.md` (append to Phase 1 results)

**Deliverable:** Findings for A2, A3, A4. Comparison data. Bases dashboard file. Template files. Health check prototype.

### Phase 3: Integration design + I/O strategy rewrite
**Targets:** None (pure build, informed by Phase 1-2 findings)
**Type:** Build
**Fits in one session:** Yes

_Tasks below are provisional — shaped by Phase 1-2 findings. If any critical assumption fails, this phase adjusts or gets abandoned._

- [ ] Write LOCKED decision: `vault/decisions/obsidian-cli-integration.md`
  - What CLI replaces (MCP project vault, grep for property search)
  - What stays (native Read/Write for known paths, hooks on file I/O)
  - What's new (Bases queries, link graph checks, template rendering)
  - GUI-required constraint and mitigation
- [ ] Rewrite I/O strategy (supersede `io-strategy-v2`):
  - Known path → Native Read/Write (unchanged)
  - Property-filtered discovery → `obsidian search query="[prop:val]" format=json`
  - Vault health → `obsidian orphans/unresolved`
  - Bases queries → `obsidian base:query format=json`
  - Brain vault → evaluate CLI with `vault="Notes"` vs keep MCP
  - Hooks → native file I/O (unchanged, GUI not guaranteed)
- [ ] Update CLAUDE.md §4 (I/O Strategy) to reflect new tool routing
- [ ] Update `/meta` command if brain vault CLI access works (or document why MCP stays)
- [ ] Add vault health check to `/wrap` protocol (or document as optional)
- [ ] Add `kepano/obsidian-skills` to shared infrastructure sync list
- [ ] Update state.md with new decisions and completed tasks

**Deliverable:** LOCKED decision file. Updated CLAUDE.md. Updated I/O strategy. Migration notes for template sync.

## Decisions

- [[decisions/io-strategy-v2]] — current I/O strategy (will be superseded if plan succeeds)
- [[decisions/plan-protocol]] — standard format and lifecycle
- [[decisions/validation-loop]] — spike assumptions, build from evidence
- [[decisions/template-vault-config]] — MCP preset in template (may need updating)
- [[decisions/brain-vault-integration]] — brain vault access pattern (may shift from MCP to CLI)
