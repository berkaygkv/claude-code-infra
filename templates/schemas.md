---
type: reference
project: kh
updated: '2026-01-22'
---
# Schemas

> Reference documentation for project structures. See [[locked]] for decisions.

## Session Note Schema

Session notes live in `notes/Sessions/session-{N}.md` and capture the state at session end for handoff.

**Frontmatter:**

```yaml
session: {N}              # Sequential session number
date: 'YYYY-MM-DD'        # Session date
project: kh               # Project identifier
topics:                   # Array of topic tags
  - topic-one
  - topic-two
outcome: successful       # Enum: successful | blocked | partial
continues_from: session-{N-1}  # Optional: previous session reference
transcript: '[[Sessions/transcripts/session-{N}]]'  # Link to full transcript
tags:
  - session
```

**Outcome values:**
- `successful` — Goals achieved, clear next steps defined
- `blocked` — Hit an impediment that prevents progress
- `partial` — Some progress made but session ended early

**Content structure:**

```markdown
## Handoff

### Context
<!-- 2-4 sentences: What this session focused on, what was accomplished -->

### Decisions
<!-- Bulleted list of decisions made this session -->
<!-- Format: "- LOCKED: {decision} — {rationale}" or "- OPEN: {issue} — {current thinking}" -->

### Memory
<!-- Technical facts, paths, quirks, workarounds discovered -->
<!-- These persist across sessions and inform future work -->

### Next Steps
<!-- Prioritized list of what to do next -->
<!-- These become suggestions in the next /begin -->
```

### Handoff Section Guidelines

**Context:** Brief narrative summary. Should be enough to understand what happened without reading the transcript. Focus on outcomes, not process.

**Decisions:** Distinguish between:
- `LOCKED` — Committed decisions that shouldn't change without good reason
- `OPEN` — Identified issues or questions still being explored

**Memory:** Facts that future sessions need to know:
- File paths and configurations
- Tool quirks and workarounds
- Environment-specific details
- API behaviors discovered

**Next Steps:** Ordered by priority. First item becomes the default suggestion for `/begin`. Each item must be specific enough that future-you knows WHAT to do — test: can you start working without asking "what does this mean?"

## Session Scratch Schema

The scratch file lives at `scratch.md` (in the project root) and serves as the staging area for vault writes during a session.

**Purpose:** Accumulate content (decisions, memory, tasks) without touching the vault. At `/wrap`, content is processed and written to appropriate vault locations, then scratch.md is reset to template form.

**Template structure:**

```markdown
# Session Scratch

## Meta
- session: {N}

## Decisions
<!-- LOCKED: decision — rationale -->
<!-- OPEN: question still unresolved -->

## Memory
<!-- Facts, preferences, constraints to persist -->

## Tasks
<!-- New tasks, completed tasks, blockers -->

## Notes
<!-- Anything else to capture -->
```

**Section mapping at /wrap:**

| Section | Maps to |
|---------|---------|
| Meta | Session note frontmatter |
| Decisions | locked.md + session handoff |
| Memory | Session handoff Memory section |
| Tasks | runbook.md |
| Notes | Session handoff Context |

**Git behavior:** Template is committed; content is never committed (reset before commit).

## Research Target Schema

Research targets live in `notes/research/targets/TARGET-{timestamp}-{slug}.md` and capture scoped research questions.

**Frontmatter:**

```yaml
type: research-target
id: TARGET-{timestamp}         # Unique identifier (timestamp: YYYYMMDD-HHMMSS)
status: open                   # Enum: open | complete
created: 'YYYY-MM-DD'          # Creation date
output: null                   # Wikilink to OUTPUT when complete
tags:
  - research
```

**Status values:**
- `open` — Research pending, not yet executed
- `complete` — Research done, OUTPUT exists

**Content structure:**

```markdown
# Research Target: {topic}

## Question
<!-- The specific question(s) we need answered -->

## Why
<!-- Why this matters, what decision it informs -->

## What We Need
<!-- List of specific things we need from the research -->

## Related
<!-- Links to relevant sessions, decisions, or other notes -->

## Status Notes
<!-- Timestamped progress updates, auto-appended on completion -->
```

## Research Output Schema

Research outputs live in `notes/research/outputs/OUTPUT-{timestamp}-{slug}/` as a folder containing findings and sources.

**Folder structure:**
```
OUTPUT-{timestamp}-{slug}/
├── findings.md    # Main findings + key sources
└── sources.md     # Full source list by relevance tier
```

**findings.md frontmatter:**

```yaml
type: research-output
id: OUTPUT-{timestamp}-{slug}  # Matches folder name
target: '[[path/to/TARGET]]'   # Wikilink to TARGET (null if ad-hoc)
created: 'YYYY-MM-DD'          # Capture date
researcher: claude-deep-research
tags:
  - research
```

**Content structure (findings.md):**

```markdown
# Research Output: {topic}

**Target:** [[link to TARGET]]
**Question:** {original question}

---

## Findings
<!-- Agent's synthesized findings -->

## Key Sources
<!-- Top 3-5 high-relevance sources -->

**Full sources:** [[link to sources.md]]
```

## Meta-Journal Schema

The meta-journal lives at `notes/meta-journal.md` and captures learnings about collaboration.

**Purpose:** Record what works, what doesn't, and what might—flaws, patterns, and hypotheses.

**Frontmatter:**

```yaml
type: meta-journal
project: kh
created: 'YYYY-MM-DD'
updated: 'YYYY-MM-DD'
tags:
  - meta
  - insights
```

**Entry format:**

```markdown
### {date} — [[Sessions/session-{N}|session-{N}: {topic}]]

{background - brief context of what led to this insight}

**Insight:** {the learning - what works, doesn't work, or might work}

---
```

**Guidelines:**
- Entries prepended (newest first)
- Background provides context; insight is the takeaway
- Link to session enables tracing back to full discussion
- Multiple entries per session allowed
- Not just flaws—also working patterns and hypotheses

## Plan Schema

Plans live in `notes/plans/plan-{slug}.md` and capture implementation blueprints for non-trivial work.

**Frontmatter:**

```yaml
type: plan
id: plan-{slug}              # URL-friendly identifier
status: draft                # Enum: draft | approved | in_progress | complete | abandoned
created: 'YYYY-MM-DD'        # Creation date
updated: 'YYYY-MM-DD'        # Last update
session: session-{N}         # Session where plan was created
tags:
  - plan
```

**Status lifecycle:**
- `draft` — Still being refined, not yet approved
- `approved` — User has approved, ready for execution
- `in_progress` — Actively being implemented
- `complete` — All phases done, success criteria met
- `abandoned` — Explicitly dropped (capture why in notes)

**Content structure:**

```markdown
# Plan: {title}

## Goal
<!-- What we're trying to achieve — the outcome, not the process -->

## Scope
<!-- What's IN and what's OUT -->
- **In scope:** {what we will do}
- **Out of scope:** {what we won't do}

## Approach
<!-- How we'll achieve the goal — high-level strategy -->

## Phases
<!-- Ordered phases with checkboxes -->
- [ ] **Phase 1: {name}** — {description}
- [ ] **Phase 2: {name}** — {description}

## Success Criteria
<!-- How we know we're done -->
- [ ] {criterion 1}
- [ ] {criterion 2}

## Related
<!-- Links to sessions, research, locked decisions -->
```

**Guidelines:**
- Plans bypass vault write discipline — create/update directly in vault (working artifacts, not archival)
- Each phase should be concrete enough to execute without further planning
- Success criteria must be verifiable
- Link to relevant research TARGETs/OUTPUTs if research informed the plan

## Mode Transitions

The collaboration operates in two modes with explicit transitions.

**Modes:**

| Mode | Purpose | Allowed Actions |
|------|---------|-----------------|
| **Plan** | Alignment & design | Read, search, research, discuss. NO codebase writes. |
| **Build** | Execution | All writes allowed. Implement the approved plan. |

**Transition triggers:**

```
         "let's plan X"
              │
              ▼
         ┌────────┐
         │  PLAN  │ ← alignment, no codebase writes
         └────────┘
              │
         "LGTM" / approval
              │
              ▼
         ┌────────┐
         │ BUILD  │ ← execution, all writes
         └────────┘
              │
         "revisit" / scope change
              │
              └──────────► back to PLAN
```

**Entry signals → Plan mode:**
- "let's plan X"
- "I want to think through..."
- "before we build..."
- Any non-trivial task without clear requirements

**Entry signals → Build mode:**
- "LGTM" / "looks good" / "approved"
- "go ahead" / "ship it"
- Explicit approval of a plan

**Skip conditions (no planning needed):**
- Trivial tasks with direct instruction ("fix the typo in X")
- Single-file changes with clear scope
- User provides explicit implementation details

**Guard:** In Plan mode, Claude should refuse codebase writes and redirect to planning. In Build mode, Claude should sanity-check against the approved plan before writing.

### Build Mode Protocol

When in Build mode, follow this sequence:

**1. Pre-flight Check**
- Re-read the approved plan
- Confirm: "Executing Plan: {name}. Starting Phase {N}."
- If plan seems stale or scope unclear → propose returning to Plan mode

**2. Phase Execution**
- State which phase you're starting
- Break into working tasks (ephemeral—Claude's working memory)
- Delegate to sub-agents where appropriate (give Why + Constraints)
- On phase completion: check off phase in plan file, brief status

**3. Deviation Handling**

| Situation | Response |
|-----------|----------|
| Minor friction (typo, small refactor) | Fix and continue |
| Unexpected complexity in phase | Voice it, propose refinement, continue if approved |
| Scope change / new requirement | **Stop.** "This is new. Return to Plan mode?" |
| Blocker (dependency, unclear requirement) | **Stop.** Flag blocker, propose next step |

**4. Completion**
- All phases checked off
- Success criteria verified
- Update plan status to `complete`
- Report: "Plan complete. {summary}."

### Adaptive Sub-task Tracking

Sub-tasks are ephemeral by default. Add them to the plan file only when needed.

**Triggers to persist sub-tasks:**
- Session ends mid-phase → checkpoint progress before handoff
- Blocker discovered → add remediation task
- Unexpected complexity → break down remaining work

**Example (mid-phase checkpoint):**

```markdown
## Phases
- [x] **Phase 1: Schema & Storage** — Add user table, password hashing
- [ ] **Phase 2: Auth Endpoints** — Login, logout, register routes
  - [x] POST /register endpoint
  - [x] POST /login endpoint
  - [ ] POST /logout endpoint ← session ended here
  - [ ] Handle expired token edge case (added: blocker)
- [ ] **Phase 3: Session Middleware** — Protect routes, token refresh
```

**Guiding principle:** Phases are sized to complete in one session. Sub-tasks appearing in the plan file are an *exception handler*, not standard practice. If sub-tasks frequently get added, it signals planning is too coarse.

### Build Mode Document Updates

| Document | When | What |
|----------|------|------|
| Plan file | Phase completion | Check off phase, update status |
| Plan file | Mid-phase checkpoint | Add sub-task progress (if session ending) |
| Codebase | During execution | The actual implementation |
| scratch.md | As needed | Notes, decisions, memory for /wrap |

## Research Pipeline Workflow

```
Brainstorming / Execution
        │
        ▼
  Hit knowledge gap
        │
        ▼
  Scoping conversation
  "What do we need to know?"
        │
        ▼
  Create TARGET(s) ← captures agreed scope
        │
        ▼
  Spawn deep-research agent(s)
        │
        ▼
  Hook captures OUTPUT(s)
  - Links OUTPUT → TARGET
  - Updates TARGET: status=complete, output=link
        │
        ▼
  Resume work with new knowledge
```
