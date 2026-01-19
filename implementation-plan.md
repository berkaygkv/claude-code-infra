# Symbiotic Collaboration Framework — Implementation Plan

## Overview

This document serves as the practical blueprint for building the Symbiotic Collaboration Framework. It transforms the conceptual framework into concrete artifacts, tasks, and decisions.

---

## 1. Requirements

### 1.1 Files to Create

| File | Location | Purpose | Status |
|------|----------|---------|--------|
| `CLAUDE.md` | Codebase root | Main system prompt defining collaboration behavior | ✅ Created (research workflow) |
| `export-transcript.py` | `.claude/hooks/` | Hook script to export transcripts to vault | ⚠️ Needs update (session-N naming) |
| `capture-research.py` | `.claude/hooks/` | Hook script to capture subagent research outputs | ✅ Created |
| `wrap.md` | `.claude/commands/` | `/wrap` slash command for session wrap-up | ⚠️ Needs update (Handoff structure) |
| `begin.md` | `.claude/commands/` | `/begin` command to load previous session context | ⏳ Pending |
| `create-target.py` | `.claude/hooks/` | Script to create research TARGETs | ✅ Created |
| `deep-research.md` | `.claude/agents/` | Deep research agent definition | ✅ Created |
| `settings.json` | `.claude/` | Hook configuration for SessionEnd + SubagentStop | ✅ Created |
| `session.md` | Obsidian `/notes/templates/` | Template for session notes (Handoff document) | ✅ Created |
| `session-transcript.md` | Obsidian `/notes/templates/` | Template for raw transcript frontmatter | ✅ Updated |

### 1.2 Obsidian Vault Structure

```
/notes
├── Sessions/
│   ├── session-1.md           # Session note (Handoff document) - PRIMARY
│   ├── session-2.md
│   └── transcripts/           # Raw transcripts - ARCHIVE
│       ├── session-1.md
│       └── session-2.md
├── research/
│   ├── targets/               # Research questions (TARGET-xxx.md)
│   └── outputs/               # Research findings (folder per output)
│       └── OUTPUT-xxx-topic/
│           ├── findings.md
│           └── sources.md
└── templates/
    ├── session.md
    └── session-transcript.md
```

#### Sessions Architecture (Three-Level Hierarchy)

**Level 1: Frontmatter (Queryable)**
- Rich metadata for Dataview queries
- Session number, date, project, topics, outcome
- Links to transcript and previous session

**Level 2: Handoff Section (Reference)**
- Context: what we were working on
- Decisions: LOCKED/OPEN items
- Memory: important things to remember
- Next Steps: where to pick up

**Level 3: Raw Transcript (Deep Dive)**
- Full conversation history
- Only accessed when Levels 1-2 are insufficient
- Stored in `Sessions/transcripts/`

**Session Naming:** `session-N.md` (sequential), `session-Nb.md` (parallel sessions)

**Session Lifecycle:**
1. `/begin` loads previous session's Handoff → continuity
2. Work happens during session
3. `/wrap` creates session note with Handoff → persistence
4. SessionEnd hook exports transcript → archive

**Session Cleanup:**
- **Delete latest session:** Just delete both files (`Sessions/session-N.md` + `Sessions/transcripts/session-N.md`). Next session reuses the number.
- **Delete older session:** Delete files. Leaves gap in sequence (harmless). Optionally fix next session's `continues_from` link to skip the deleted one.
- System is resilient — numbering finds MAX, doesn't care about gaps.

#### Research Architecture

**TARGETs (`research/targets/`)**
- Research questions with context
- Frontmatter: status (active/resolved), assignee, created date
- Links to session that spawned it (optional)

**OUTPUTs (`research/outputs/`)**
- Folder per research output
- `findings.md`: main content + top sources
- `sources.md`: full source list
- Links back to TARGET via `target-id`

### 1.3 Template Schemas

#### Session Note Schema (Handoff Document)
```yaml
---
session: 15                              # Sequential number
date: YYYY-MM-DD
project: kh
topics: [topic1, topic2]                 # Free-form tags
outcome: successful | partial | blocked
continues_from: session-14               # Previous session link
transcript: "[[Sessions/transcripts/session-15]]"
tags: [session]
---

## Handoff

### Context
[What we were working on this session]

### Decisions
- LOCKED: [decision] — [rationale]
- OPEN: [question still unresolved]

### Memory
[Important things to remember across sessions]

### Next Steps
[Where to pick up, what's pending]
```

#### Session Transcript Schema
```yaml
---
session: 15
date: YYYY-MM-DD
time_start: HH:MM
time_end: HH:MM
project: kh
session_note: "[[Sessions/session-15]]"
tags: [session, transcript]
---

[RAW TRANSCRIPT CONTENT]
```

#### Research TARGET Schema
```yaml
---
type: research-target
id: TARGET-YYYYMMDD-HHMMSS
status: active | resolved
created: YYYY-MM-DD
assignee: claude | human
---

# Research Target: [topic]

## Question
[What we're trying to learn]

## Why
[Context for why this research is needed]

## What We Need
- [Specific aspect 1]
- [Specific aspect 2]
```

#### Research OUTPUT Schema
```yaml
---
type: research-output
id: OUTPUT-YYYYMMDD-HHMMSS-slug
target-id: TARGET-YYYYMMDD-HHMMSS
status: draft | reviewed
created: YYYY-MM-DD
researcher: claude-deep-research
confidence: low | medium | high
---

# Research Output: [topic]

**Target:** [[research/targets/TARGET-xxx]]

## Findings
[Research content]

## Key Sources
[Top 5 high-relevance sources]

**Full sources:** [[research/outputs/OUTPUT-xxx/sources]]
```

### 1.4 Claude Code Features Required

| Feature | Purpose | Status |
|---------|---------|--------|
| Obsidian MCP | Read/write vault notes, persist decisions | Available |
| Context7 MCP | Fetch up-to-date library docs | Available |
| Task tool (Explore agent) | Codebase exploration | Available |
| Task tool (Plan agent) | Implementation planning | Available |
| Task tool (Bash agent) | Isolated shell operations | Available |
| TodoWrite tool | Track execution progress | Available |
| Git integration | Commit artifacts with context | Available |

### 1.5 CLAUDE.md Structure

```
CLAUDE.md
├── Identity & Role
├── The Two Modes
│   ├── Mode 1: Brainstorm Protocol
│   └── Mode 2: Execution Protocol
├── Session Lifecycle
│   ├── Session Start
│   ├── During Session
│   └── Session End
├── Memory Protocol (Obsidian Integration)
├── Delegation Framework
├── Anti-Pattern Guards
├── Convergence Signals
└── Mode Switching Rules
```

---

## 2. Checklists

### Phase 1: Vault Foundation ✅ COMPLETE
- [x] Create Obsidian vault directories (`Sessions/transcripts/`, `Sessions/summaries/`, `Research/tasks/`, `Research/raw/`)
- [x] Create session transcript template
- [x] Create session summary template
- [x] Create research task template
- [x] Create research raw template
- [x] Validate templates work with Obsidian MCP (create, read, query frontmatter)

### Phase 2: Transcript Hook ✅ COMPLETE
- [x] Research Claude Code hook system (events, capabilities, limitations)
- [x] Design hook trigger (on session end? on demand? on specific command?) → **SessionEnd hook**
- [x] Implement transcript export mechanism (symlink vs copy) → **Copy with JSONL→Markdown conversion**
- [x] Implement frontmatter injection (session_id, date, timestamps)
- [x] Implement summary_link placeholder (for later linking)
- [x] Test hook with real session data
- [x] Document hook installation and configuration → **Documented in CLAUDE.md**

**Implementation Details:**
- Hook script: `.claude/hooks/export-transcript.py`
- Hook config: `.claude/settings.json`
- Transcripts stored at: `/notes/Sessions/transcripts/{session_id}.md`
- Source: `~/.claude/projects/<project-hash>/<session-uuid>.jsonl`

### Phase 3: Session Summary Flow ✅ COMPLETE
- [x] Define what triggers summary creation → **`/wrap` slash command**
- [x] Define summary generation approach → **AI-generated via /wrap**
- [x] Implement bidirectional linking (transcript ↔ summary)
- [x] Test full flow: session → transcript hook → summary creation → linking

**Implementation Details:**
- Slash command: `.claude/commands/wrap.md`
- Triggers: AI reads transcript, generates summary, writes to Obsidian
- Summary has `transcript_link`, transcript has `summary_link`
- `tldr` moved to frontmatter for searchability

### Phase 4: Research Task System ✅ COMPLETE

#### 4a: Raw Capture Infrastructure ✅ COMPLETE
- [x] Define raw findings capture flow → **SubagentStop hook auto-captures**
- [x] Test capture with real subagent

#### 4b: Research Task Lifecycle ✅ COMPLETE
- [x] Define task states: `active` → `resolved` (simplified from Jira-style)
- [x] Define task creation flow → **TARGET files created programmatically**
- [x] Implement task ↔ raw linkage (OUTPUT `target-id` ↔ TARGET)
- [x] Create task management queries → **Dataview compatible frontmatter**

#### 4c: Deep Research Pipeline ✅ COMPLETE
- [x] Create dedicated research agent prompt → **`deep-research` built-in agent**
- [x] Implement active task state mechanism → **`/tmp/claude-active-research-target.txt`**
- [x] Fix YAML sanitization in capture hook
- [x] Test deep-research agent with real research query
- [x] Implement efficient TARGET creation → **`create-target.py` script**
- [x] Implement folder-per-output structure
- [x] Implement source separation (findings.md + sources.md)
- [x] Parse agent's own source ranking (High/Medium/Low)
- [x] Test end-to-end workflow
- [x] Document research workflow → **In CLAUDE.md (replaced `/research` command)**

**Implementation Details:**
- Hook: `.claude/hooks/capture-research.py` (SubagentStop, web-research only)
- TARGET creation: `.claude/hooks/create-target.py` (single command, sets active)
- Active target file: `/tmp/claude-active-research-target.txt`
- Workflow documented in: `CLAUDE.md`

**Design Decision:** Instead of a separate `/research` slash command, the research workflow is documented directly in `CLAUDE.md`. This is simpler and ensures Claude follows the workflow whenever the user requests research, without needing to invoke a specific command.

**Vault Structure (v2):**
```
research/
├── targets/                    # Research questions (TARGET-xxx.md)
└── outputs/                    # Research findings (folder per output)
    └── OUTPUT-xxx-topic/
        ├── findings.md         # Main content + top 5 sources
        └── sources.md          # Full source list (token-efficient)
```

**Workflow (2 tool calls):**
1. `Bash` - Create TARGET via `create-target.py` (heredoc JSON input)
2. `Task` - Spawn deep-research with source ranking instructions
3. Hook auto-creates OUTPUT folder linked to TARGET

### Phase 5: Sessions Refinement ⏳ IN PROGRESS

#### 5a: Vault Cleanup ✅ COMPLETE
- [x] Identify garbage files (old structures, orphaned outputs)
- [x] Remove deprecated folders (Sessions/plans, Sessions/Raw, Sessions/Processed, blueprints)
- [x] Remove old templates (research-raw.md, research-task.md, session-summary.md)
- [x] Remove orphaned TARGETs and flat OUTPUT files

#### 5b: Sessions Architecture Redesign ✅ COMPLETE
- [x] Design three-level hierarchy (Frontmatter → Handoff → Transcript)
- [x] Choose session naming: `session-N.md` (sequential)
- [x] Create session note template with Handoff structure
- [x] Update session transcript template

#### 5c: Sessions Implementation ⏳ IN PROGRESS
- [x] Update `export-transcript.py` hook for session-N naming
- [x] Update `/wrap` command for new Handoff structure
- [ ] Create `/begin` command to load previous session context
- [ ] Test full session lifecycle

**Session Lifecycle:**
1. `/begin` → loads previous session's Handoff section
2. Work during session
3. `/wrap` → creates session-N.md with Handoff + links
4. SessionEnd hook → exports transcript to session-N.md in transcripts/

---

### Phase 5-OLD: Research Pipeline Enhancements 🔒 DEFERRED

**Decision:** Skip for now. Solve problems with behavior, not infrastructure. Revisit if friction emerges from real-world usage.

#### Quick Search Mode
- Current behavior is sufficient: inline searches don't get captured, only deep-research does.

#### Vault Management Agent
- YAGNI. Vault is small, manual management is trivial. Revisit at 100+ files.

### Phase 6: CLAUDE.md Core

#### 6a: Lock-in Protocol ⏳ DESIGN NEEDED
- [ ] Design lock-in mechanism for transitioning from brainstorm → execution
- [ ] Define lock-in representation (file in vault? frontmatter status? dedicated note?)
- [ ] Define unlock protocol (explicit unlock required before modifying locked plan)
- [ ] Integrate with session workflow

**Concept:**
- Brainstorming often leads to distraction or premature implementation
- Need a cognitive checkpoint: "Are we locked in?" before starting execution
- Once locked in, the plan is frozen — changes require explicit unlock first
- Prevents scope creep and mid-implementation pivots
- Creates clear commitment point between exploration and execution

**Open questions:**
- What gets locked? (The plan? Specific decisions? Scope?)
- Where is lock state stored? (Vault note? Session frontmatter? Dedicated file?)
- What does unlock require? (Explicit command? Justification?)

#### 6b: Mode Separation ⏳ DESIGN NEEDED
- [ ] Decide mode separation mechanism
- [ ] Implement chosen approach
- [ ] Document mode switching protocol

**Options to evaluate:**
| Option | Pros | Cons |
|--------|------|------|
| Git branch per mode | Clear separation, can diff/merge | Overhead, merge conflicts |
| Git worktree | Parallel work, isolated | Complex setup |
| `/begin` argument | Simple, session-scoped | No persistent separation |
| Vault-based flag | Queryable, persistent | Manual tracking |

**Open questions:**
- Do modes need file-level separation or just behavioral?
- Should mode be per-session or per-task?
- How does mode interact with lock-in? (e.g., must be locked-in to enter execution mode?)

#### 6c: Core Protocol
- [ ] Write Identity & Role section
- [ ] Write Mode 1 (Brainstorm) protocol
- [ ] Write Mode 2 (Execution) protocol
- [ ] Write Anti-Pattern Guards section
- [ ] Write Convergence Signals section
- [ ] Write session start protocol (context loading)
- [ ] Write during-session protocol (research, decision tracking)
- [ ] Write session end protocol (trigger hook, create Handoff)
- [ ] Integrate session protocol with Obsidian vault structure

### Phase 7: CLAUDE.md Research Protocol
- [ ] Write research task management protocol
- [ ] Write raw findings capture protocol
- [ ] Write research evaluation protocol
- [ ] Define when to spawn research agents vs. direct search

### Phase 8: Integration Testing
- [ ] Test full session lifecycle (start → work → end → transcript → summary)
- [ ] Test research lifecycle (create task → research → raw capture → evaluate → close)
- [ ] Test cross-session context restoration (load previous summaries)
- [ ] Test Obsidian query on frontmatter (filter by status, priority, project)

### Phase 9: Refinement
- [ ] Dry-run full workflow on a real task
- [ ] Identify friction points
- [ ] Revise CLAUDE.md based on findings
- [ ] Revise templates based on findings
- [ ] Document final system for shipping

---

## 3. Open Questions

### Transcript Hook ✅ RESOLVED

| Question | Severity | Resolution |
|----------|----------|------------|
| What Claude Code hook event should trigger transcript export? | `high` | **SessionEnd** hook with reasons: `clear`, `logout`, `prompt_input_exit`, `other` |
| Symlink vs. copy for transcript storage? | `moderate` | **Copy** — converts JSONL to readable Markdown with frontmatter |
| Where does Claude Code store raw session data? | `high` | **`~/.claude/projects/<project-hash>/<session-uuid>.jsonl`** |
| How to detect session boundaries (start/end)? | `moderate` | **SessionStart/SessionEnd hooks** — both available with payload including `session_id`, `transcript_path` |

### Session Summary ✅ RESOLVED

| Question | Severity | Resolution |
|----------|----------|------------|
| Should summary generation be automatic (AI) or manual (human)? | `high` | **AI-generated** via `/wrap` command |
| What triggers summary creation? | `moderate` | **`/wrap` slash command** — bundles summary + git commit + docs update |
| How much of the transcript should the AI read for summarization? | `moderate` | Full transcript — Claude reads most recent `.jsonl` file |

### Research System ✅ RESOLVED

| Question | Severity | Resolution |
|----------|----------|------------|
| Who creates research tasks — human, AI, or both? | `moderate` | **Claude creates via `create-target.py`** when user requests research |
| How to automatically capture raw findings from agents? | `high` | **SubagentStop hook** captures to `research/outputs/`. Active TARGET auto-linked via state file. |
| Should raw findings be one file per search, or appended to single file? | `low` | **Folder per agent invocation** — findings.md + sources.md |
| How to handle research that spans multiple sessions? | `moderate` | TARGET persists in Obsidian, OUTPUT folders accumulate with `target-id` links. |
| How to trigger research workflow? | `moderate` | **CLAUDE.md instructions** — Claude follows workflow when user requests research (no separate command) |

### Context Loading ✅ RESOLVED

| Question | Severity | Resolution |
|----------|----------|------------|
| What should auto-load at session start? | `high` | **Previous session's Handoff section** via `/begin` command. Contains context, decisions, memory, next steps. |
| How to prevent context overload? | `moderate` | **Handoff is focused** — only essential info for continuity, not full transcript. Level 3 (transcript) only accessed when needed. |

### CLAUDE.md Scope

| Question | Severity | Notes |
|----------|----------|-------|
| How much protocol belongs in CLAUDE.md vs. external referenced docs? | `moderate` | Long CLAUDE.md = token cost. Short = lost nuance. Need balance. |
| Should CLAUDE.md be project-agnostic or project-specific? | `moderate` | Agnostic = reusable. Specific = immediately useful. |

---

## 4. Knowledge Gaps

### Claude Code Hook System ✅ RESOLVED
- **Gap:** Full understanding of Claude Code hooks — available events, payload structure, execution context
- **Resolution:** 10 hook events available: `PreToolUse`, `PostToolUse`, `PermissionRequest`, `UserPromptSubmit`, `Notification`, `Stop`, `SubagentStop`, `PreCompact`, `SessionStart`, `SessionEnd`. Each receives JSON via stdin with `session_id`, `transcript_path`, and event-specific fields.

### Claude Code Session Storage ✅ RESOLVED
- **Gap:** Where and how Claude Code stores session/conversation data locally
- **Resolution:** Sessions stored at `~/.claude/projects/<project-hash>/<session-uuid>.jsonl` in JSONL format (one JSON object per line).

### Obsidian MCP Write Behavior ✅ RESOLVED
- **Gap:** How Obsidian MCP handles file creation, updates, and frontmatter parsing
- **Resolution:** Tested successfully. `write_note` creates/overwrites, supports `frontmatter` parameter as object, modes: `overwrite`, `append`, `prepend`.

### Obsidian Dataview/Query Capabilities ✅ RESOLVED
- **Gap:** How to query notes by frontmatter fields (status, priority, project)
- **Resolution:** Dataview plugin supports WHERE clause filtering on any frontmatter field. Use `contains(tags, "value")` for arrays. Case-sensitive. Query examples captured in `/notes/Research/raw/agent-aa8cdd0.md`.

### Agent Output Capture ✅ RESOLVED
- **Gap:** How to programmatically capture output from spawned agents (Explore, Plan, etc.)
- **Resolution:** SubagentStop hook fires when agents finish. Subagent transcripts stored at `~/.claude/projects/{project}/{session}/subagents/agent-{id}.jsonl`. Hook can parse JSONL and export to Obsidian.

### Session Boundary Detection ✅ RESOLVED
- **Gap:** How to reliably detect when a session starts and ends
- **Resolution:** `SessionStart` hook (with `source`: `startup`, `resume`, `clear`, `compact`) and `SessionEnd` hook (with `reason`: `clear`, `logout`, `prompt_input_exit`, `other`) provide reliable lifecycle events.

---

## Next Steps

1. ~~Review this document~~ ✅
2. ~~Resolve `high` severity open questions (especially hook system and session storage)~~ ✅
3. ~~Begin Phase 1 (Vault Foundation)~~ ✅
4. ~~Begin Phase 2 research in parallel (Claude Code hooks)~~ ✅
5. ~~Phase 3: Session Summary Flow~~ ✅
6. ~~Phase 4a: Raw capture infrastructure~~ ✅
7. ~~Phase 4b: Research task lifecycle~~ ✅
8. ~~Phase 4c: Deep research pipeline~~ ✅
9. ~~Phase 5a: Vault Cleanup~~ ✅
10. ~~Phase 5b: Sessions Architecture Redesign~~ ✅

**Current:**
11. Phase 5c: Sessions Implementation (hooks + commands)
12. Phase 6: CLAUDE.md Core (Identity, Modes, Anti-Patterns, Convergence)

---

*This document is a living artifact. Update it as decisions are made and gaps are filled.*

---

## Changelog

| Date | Changes |
|------|---------|
| 2026-01-19 | Phase 1 complete: Vault structure + templates created |
| 2026-01-19 | Phase 2 complete: SessionEnd hook exports transcripts to Obsidian |
| 2026-01-19 | Resolved: Hook system, session storage, session boundary detection |
| 2026-01-19 | Phase 3 complete: `/wrap` command for session summaries |
| 2026-01-19 | Phase 4a complete: SubagentStop hook captures research outputs to Obsidian |
| 2026-01-19 | Phase 4b complete: Research task lifecycle, dashboard, bidirectional linkage |
| 2026-01-19 | Resolved: Agent output capture, Dataview query syntax |
| 2026-01-19 | Phase 4c partial: `deep-research` agent created, YAML sanitization fixed |
| 2026-01-19 | Added: Active task state mechanism for auto-linking raw findings to tasks |
| 2026-01-19 | Researched: Obsidian plugins for task management (captured in vault) |
| 2026-01-19 | **Phase 4 COMPLETE**: All research infrastructure done. Workflow in CLAUDE.md (replaced `/research` command) |
| 2026-01-19 | **Phase 5a-5b COMPLETE**: Vault cleanup + Sessions architecture redesign. Three-level hierarchy (Frontmatter→Handoff→Transcript). Sequential naming (session-N). `/begin` command planned. |
| 2026-01-19 | **DEFERRED**: Research Pipeline Enhancements (Phase 5-OLD). YAGNI - solve with behavior, not infrastructure. |
