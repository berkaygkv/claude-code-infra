---
type: research-output
id: OUTPUT-20260121-210630-how-claude-code-customized-environments
target: null
created: 2026-01-21
researcher: claude-deep-research
tags:
  - research
---

# Research Output: how Claude Code customized environments structure their "plan" or "blueprint" p

**Question:** Research how Claude Code customized environments structure their "plan" or "blueprint" phase before execution.

**Primary target:** maxritter/claude-code-pro on GitHub - analyze their planning approac...

---

## Findings

Excellent. I now have comprehensive information. Let me compile the research synthesis.

This research investigated how Claude Code customization environments structure their planning/blueprint phase before execution, with deep focus on maxritter/claude-code-pro and other prominent frameworks. The findings reveal diverse but convergent patterns: most systems use persistent markdown files with phase-based structures, explicit approval gates between planning and execution, and varying granularity levels matched to task complexity. Key patterns include three-file systems (task_plan.md, findings.md, progress.md), spec-driven workflows with separate requirement/design/implementation documents, and context engineering strategies that treat the filesystem as persistent memory.

## Research Summary

### Question/Topic
How do Claude Code customized environments structure their "plan" or "blueprint" phase before execution? Primary target: maxritter/claude-code-pro. Secondary targets: Other popular Claude Code customization repos with focus on concrete plan templates, schemas, sections, approval mechanisms, storage patterns, and granularity levels.

### Key Findings

1. **Three-File Manus Pattern (Most Influential)**: The planning-with-files skill implements Manus AI's context engineering approach using task_plan.md (phases/progress), findings.md (research), and progress.md (logs). This pattern inspired by Meta's $2B Manus acquisition treats filesystem as persistent memory.

2. **Spec-Driven Workflows Dominate**: Multiple frameworks (claude-code-pro, agentic-startup, claude-code-spec-workflow) separate planning into sequential documents: product-requirements.md → solution-design.md → implementation-plan.md.

3. **Phase-Based Structures Universal**: All examined systems use phase/milestone breakdowns with checkbox tracking. Phases typically contain: description, file paths, specific changes, success criteria (automated/manual), and status indicators.

4. **Approval Gates Are Explicit but Varied**: Most use dedicated approval tools (ExitPlanMode), validation commands (/validate), or manual review checkpoints between plan and implement phases. The native Claude Code ExitPlanMode reads plan from disk and triggers user approval dialog.

5. **Granularity Matches Complexity**: High-quality frameworks adjust detail level—simple tasks get high-level plans, complex multi-file refactors get file:line specificity with code examples.

6. **File Storage Strongly Preferred Over Inline**: Community consensus (2025) favors persistent markdown files in project repos over conversation-only plans. Enables version control, team collaboration, session recovery, and multi-agent coordination.

### Detailed Analysis

#### Claude-Code-Pro (maxritter): Spec-Driven Four-Phase Workflow

The claude-code-pro framework implements:

**Structure:**
- Plans stored in `docs/plans/` as markdown
- Uses modular rules system in `.claude/rules/`
- Workflow: Plan → Approve → Implement → Verify

**Commands:**
- `/plan` - Explores codebase, asks questions, writes spec to docs/plans/
- Human reviews/edits plan
- `/implement` - Executes approved plan with TDD enforcement
- `/verify` - Validates completion against plan

**Approval Mechanism:**
Explicit human-in-the-loop: "You review, edit if needed, and approve the plan before implementation." No automatic proceed. Manual approval required to transition from plan to implement phase.

**Key Insight:**
Quick Mode available for simple tasks (no plan file, no approval gate) but retains quality hooks. This demonstrates adaptive granularity—framework recognizes when planning overhead exceeds value.

#### Planning-With-Files: Three-File Manus Pattern

**Complete Template Structures:**

**task_plan.md:**
```markdown
# Goal
[Single sentence task description]

# Phases
- [ ] Phase 1: [Name]
  - [ ] Subtask 1
  - [ ] Subtask 2
  **Status:** pending/in_progress/complete

- [ ] Phase 2: [Name]
  **Status:** pending

[Continue for 3-7 phases total]

# Technical Decisions
| Decision | Rationale | Date |
|----------|-----------|------|
| [Choice] | [Why]     | [When]|

# Errors Encountered
| Error | Resolution | Date |
|-------|------------|------|
| [Issue]| [Fix]     | [When]|
```

**findings.md:**
```markdown
# Research Findings
## [Topic Area]
- Discovery 1
- Discovery 2

# Technical Decisions
## [Decision Title]
**Choice:** [What was decided]
**Rationale:** [Why this approach]
**Alternatives Considered:** [What was rejected and why]

# Resources
- [URL] - [Description]
- [URL] - [Description]

# Important Notes
- Critical insight 1
- Critical insight 2
```

**progress.md:**
```markdown
# 5-Question Context Check
(When resuming work)
1. What was I working on?
2. What phase am I in?
3. What was the last action?
4. Were there blockers?
5. What's next?

# Phase 1 Summary
**Actions Taken:**
- Implemented X
- Modified files: path/to/file.ts

**Files Changed:**
- path/to/file1.ts
- path/to/file2.ts

# Test Results
| Test | Status | Notes |
|------|--------|-------|
| Unit tests | ✓ Pass | All 47 passed |
| Integration | ✗ Fail | API timeout issue |

# Error Log
**[2025-01-21 14:30]** - Connection timeout to external API
**Resolution Attempted:** Increased timeout to 30s
**Outcome:** Still failing, need to investigate further
```

**Update Triggers:**
- task_plan.md: Read before every Write/Edit/Bash (PreToolUse hook), updated after phase completion (PostToolUse hook)
- findings.md: Updated after every 2 search/view/browser operations (2-Action Rule)
- progress.md: Updated after phase completion or error encounters

**Approval Pattern:**
No explicit approval gate—continuous planning. Stop hook verifies all phases complete before task termination. Emphasis on preventing premature closure rather than gating execution start.

**Philosophy:**
"Context Window = RAM (volatile), Filesystem = Disk (persistent)" → Anything important must be written to files, not kept in conversation memory.

#### The Agentic Startup (rsmdt/the-startup): Three-Document Specification System

**Structure:**
```
docs/specs/001-feature-name/
├── product-requirements.md  # What to build and why
├── solution-design.md       # How to build it technically
└── implementation-plan.md   # Executable tasks and phases
```

**Workflow Commands:**
- `/start:specify` - Creates all three documents through research and Q&A
- `/start:validate 001` - Checks 3 Cs: Completeness, Consistency, Correctness
- `/start:implement 001` - Parses plan and executes phases sequentially
- `/start:review` - Multi-agent code review (security, performance, quality)

**Approval Mechanism:**
1. Advisory validation (recommendations don't block)
2. Phase-by-phase approval during implementation (user approval between stages)
3. Optional constitutional governance (project-wide rules auto-enforced)

**Granularity Example:**
Plans specify exact file paths with code changes:
```markdown
## Phase 2: Backend Implementation

### Files to Modify:
**prisma/schema.prisma**
- Add Payment model
- Add relation to User model

**src/api/payments.ts**
- Implement createPayment endpoint
- Add Stripe integration
- Error handling for failed charges

### Success Criteria:
#### Automated:
- [ ] Migration runs successfully
- [ ] Unit tests pass (>80% coverage)
- [ ] API returns 200 on valid request

#### Manual:
- [ ] Test with Stripe test card
- [ ] Verify webhook handling
```

**Session Continuity:**
If context limits hit during specify phase, pass spec ID to new conversation (`/start:specify 001`). Claude reads existing files and continues. Each document can be completed across separate sessions.

#### Research-Plan-Implement Framework: Phase-Driven Execution

**Four-Phase Structure:**
1. `/1_research_codebase` - Deep exploration with parallel agents
2. `/2_create_plan` - Interactive planning with user engagement
3. `/4_implement_plan` - Reads plan, creates todos, executes phase-by-phase
4. `/3_validate_plan` - Verification and reporting

**Plan Template:**
```markdown
# Feature Implementation Plan

## Phase 1: Database Setup
### Changes Required:
- Add payment tables
- Create migration scripts
- Update Prisma schema

### Success Criteria:
#### Automated:
- [ ] Migration runs successfully
- [ ] Schema validation passes
- [ ] Tests pass

#### Manual:
- [ ] Data integrity verified
- [ ] No performance degradation

## Phase 2: API Integration
[Similar structure...]

## Phase 3: Frontend Components
[Similar structure...]
```

**Approval/Transition:**
- No explicit approval gate documented
- Relies on success criteria validation
- Interactive planning resolves questions before finalizing
- Checkpoint system: `/5_save_progress` captures state, `/6_resume_work` restores

**Key Pattern:**
"Plans serve as technical specs" maintaining structure throughout implementation. Implementation reads plan and tracks with todos.

#### Project-Plan Command Template: Seven-Step Specification Process

**Structure from shamshirz/project-plan gist:**

```markdown
# PLAN.md

## Problem Description
**Context:** [Background on project and business]
**Problem Statement:** [What challenge needs solving]
**Target Outcome:** [Desired end result]

## Implementation Approach
### Option 1: [Approach Name]
**Description:** [How it works]
**Pros:**
- Benefit 1
- Benefit 2
**Cons:**
- Drawback 1
- Drawback 2

### Option 2: [Alternative Approach]
[Same structure...]

### Option 3: [Third Alternative]
[Same structure...]

**Recommendation:** [Selected approach with justification]

## Milestones
### Milestone 1: [Phase Name]
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3
**Automated Test:** [Assertion for completion]

### Milestone 2: [Phase Name]
[Similar structure...]

## Implementation Notes
- MVP scope clarifications
- Technology decisions
- Constraints and assumptions

## Future Enhancements
- Out-of-scope feature 1
- Out-of-scope feature 2

## Iteration Workflow
[Reference to quality verification processes]
```

**Seven-Step Process:**
1. Feature Analysis
2. Repository Context Research
3. Best Practices Research
4. Implementation Plan (broad strategy)
5. Requirements Gathering (functionality, security, performance)
6. Quality Control (validate completeness)
7. Document Generation (`plans/YYYYMMDD-feature-name.md`)

**Output Artifact:**
- Dated plan files: `plans/YYYYMMDD-feature-name[-suffix].md`
- Ready for human review
- Includes developer guide with style references
- Sub-agent delegation recommendations

**Critical Constraints:**
- No future work or "Next Steps" sections
- Provide examples/pseudocode only, not complete implementations
- Use numeric suffixes to avoid file naming conflicts

#### Spec-Workflow (Pimzino): Requirements → Design → Tasks → Implementation

**Template Structure (in `.claude/` directory):**

**Steering Documents (one-time setup):**
- `steering/product.md` - Vision, users, features, metrics
- `steering/tech.md` - Stack, tools, constraints, integrations
- `steering/structure.md` - File organization, naming, import patterns

**Specification Documents (per feature):**
- `specs/feature-name/requirements.md` - User stories + acceptance criteria
- `specs/feature-name/design.md` - Technical architecture + diagrams
- `specs/feature-name/tasks.md` - Atomic, agent-friendly breakdown
- `specs/feature-name/commands/` - Auto-generated task execution commands

**Bug Fix Documents:**
- `bugs/issue-name/documentation.md` - Structured issue format
- `bugs/issue-name/analysis.md` - Root cause
- `bugs/issue-name/solution.md` - Implementation details
- `bugs/issue-name/verification.md` - Confirmation

**Commands:**
```bash
/spec-steering-setup          # Create steering docs
/spec-create feature-name "Description"
/spec-execute                 # Run all tasks
/feature-name-task-1          # Run specific task
/spec-status                  # Track progress

/bug-create issue-name "Description"
/bug-analyze
/bug-fix
/bug-verify
/bug-status
```

**Approval Mechanism:**
- Confirmation prompts during setup (safety)
- Status commands for progress tracking
- Manual execution control (selective task implementation)
- Steering document validation (alignment with standards)

**Key Benefit:**
"60-80% token reduction" through context optimization. Tasks are atomic and context-optimized for agent execution.

#### Native Claude Code Plan Mode: Built-In Approval Workflow

**How It Works:**
1. User activates: Press `Shift+Tab` twice or `/plan` command
2. Claude restricted to read-only tools (Read, Grep, Glob, WebSearch, WebFetch)
3. Claude analyzes codebase and creates plan file
4. Claude calls `ExitPlanMode` tool when plan complete
5. Approval dialog appears showing plan contents
6. User chooses: "Auto-accept edits + clear context", "Auto-accept edits", or manual review
7. If approved, Claude proceeds with implementation using Sonnet 4.5

**Plan Structure:**
Unstructured markdown but typically contains:
- Task breakdown with dependencies
- Execution order
- File paths for changes
- Four-phase workflow: Understanding → Design → Review → Final Plan

**Storage:**
- Plans saved to `~/.claude/plans/` (user-level directory)
- Community requests (2025): Support for `.claude/plans/` in project root
- Feature requests: Support for `.claude/plan-template.md` templates

**ExitPlanMode Tool Mechanics:**
- Does NOT take plan content as parameter
- Reads plan from file already written
- Inherently requests user approval (don't ask "Is this plan okay?" separately)
- Use ONLY for implementation planning, not research/exploration tasks
- Returns approval status to agent

**Known Issues (2025):**
- Bug reports of approval dialog not rendering
- Default option "clear context + auto-accept" controversial (loses conversation context including instructions/templates)
- Some users report auto-approval without interaction

**Best Practice:**
"It's a good practice to have Claude save the refined plan into a Markdown file (e.g., PLAN.md) and commit it to your repository" for persistent reference across sessions.

#### Manus AI Context Engineering: Todo.md + Task Recitation

**Planning Approach:**
Centralized orchestrator (single agent) rather than multi-agent swarms. "Less structure, more intelligence" philosophy.

**Todo.md Pattern:**
- Create and continuously update `todo.md` throughout execution
- Updates push global plan into model's recent attention span
- Addresses "lost-in-the-middle" attention degradation in long contexts
- Tasks average ~50 tool calls, requiring sustained goal alignment

**Context Management:**
- File system = Structured persistent memory
- Offload heavy data to files, keep summaries in context
- Retrieve archived context via search tools when needed
- Write to and read from files on demand

**Error Integration:**
Deliberately preserve errors in context (not in separate log initially):
- Failed actions remain visible
- Model implicitly updates beliefs
- Avoids repeating similar mistakes
- Treats error traces as instructional data

**No Explicit Approval Gate:**
Planning is continuous and adaptive rather than "plan then execute." The todo.md file evolves as understanding deepens.

### Limitations & Gotchas

**Native Plan Mode Issues:**
- Approval dialog bugs reported (fails to render, auto-approves without interaction)
- Context clearing on approval loses conversation instructions/templates
- Plans stored in user home directory (`~/.claude/plans/`) not project-local
- No template support as of 2025-01
- Can't be used in TypeScript SDK in some cases

**Granularity Pitfalls:**
- Too detailed (file:line level) for simple tasks adds overhead
- Too vague (high-level only) prevents effective agent execution
- Rule of thumb: Multi-file tasks need detailed plans, single-file edits don't

**Over-Planning Risk:**
Multiple sources warn against using Plan Mode for:
- Trivial tasks (typo fixes, single-line changes)
- Research/exploration (no implementation intent)
- Tasks isolated to one file
- Low-latency requirements (planning adds overhead)

**Context Continuity Challenges:**
- Native Claude Code plans don't persist across sessions
- Conversation history not project-local
- Context window limits can interrupt specification phase
- Recovery patterns needed (pass spec ID to new session)

**Approval Gate Friction:**
- Some frameworks have advisory validation only (doesn't block)
- Manual approval between every phase can slow velocity
- Balance needed between safety gates and execution speed

**File Naming Conflicts:**
Multiple systems use dated filenames (`YYYYMMDD-feature-name.md`) or numeric suffixes to avoid collisions when multiple features planned simultaneously.

### Recommendations

**1. Adopt Three-File Pattern for Complex Tasks**

Use the Manus-inspired approach:
- `task_plan.md` - Goal, phases (3-7), decisions, errors
- `findings.md` - Research, technical decisions, resources
- `progress.md` - Session logs, test results, error timeline

**When:** Multi-phase features, research-heavy tasks, anything requiring >10 tool calls

**Why:** Proven by Manus acquisition, handles context limits, enables session recovery, explicit error tracking

**2. Use Separate Specification Documents for Large Features**

Follow agentic-startup three-document pattern:
- `product-requirements.md` - What and why
- `solution-design.md` - How (architecture)
- `implementation-plan.md` - Executable phases

**When:** Features requiring architectural decisions, team collaboration, or multi-week implementation

**Why:** Separates concerns, enables parallel work on different documents, supports stakeholder review at appropriate abstraction levels

**3. Implement Explicit Approval Gates**

Use dedicated tools/commands between phases:
- Plan creation → Validation command → Approval → Implementation
- Or: ExitPlanMode pattern with approval dialog
- Or: Phase-by-phase approval during execution

**When:** Production code, multi-file refactors, anything with risk

**Why:** Prevents misaligned implementations, enables course correction cheaply, maintains human oversight

**4. Match Granularity to Complexity**

| Task Complexity | Plan Detail Level | Example |
|----------------|-------------------|---------|
| Trivial | No plan, direct execute | Fix typo, add import |
| Simple | High-level tasks only | Add validation to form |
| Moderate | Tasks + file paths | Implement new API endpoint |
| Complex | Tasks + files + code examples | Multi-file refactor |
| Very Complex | Phases + tasks + files + code + diagrams | New feature with DB changes |

**5. Store Plans in Project Repository**

Prefer `.claude/plans/` or `docs/specs/` over `~/.claude/plans/`:
- Version control plans alongside code
- Enable team collaboration on approach
- Support multi-agent access to same plan
- Persist across Claude Code sessions
- Commit plans to create persistent roadmap

**6. Use Checkbox-Based Progress Tracking**

Standard markdown checkboxes enable:
- Visual progress indicators
- Easy status updates
- Clear completion criteria
- Integration with tools that parse markdown tasks

Format:
```markdown
## Phase 2: API Integration
- [ ] Create endpoint
- [ ] Add validation
- [x] Write tests (COMPLETED)
- [ ] Deploy to staging
```

**7. Separate Success Criteria: Automated vs Manual**

```markdown
### Success Criteria
#### Automated:
- [ ] Tests pass (>80% coverage)
- [ ] Build succeeds
- [ ] Migrations run cleanly

#### Manual:
- [ ] UI/UX review approval
- [ ] Performance testing in staging
- [ ] Security review completed
```

**Why:** Makes verification expectations explicit, enables partial automation, clarifies what requires human judgment

**8. Implement the 2-Action Rule for Research**

After every 2 view/search/browser operations, update findings.md. Prevents context drift during extended research phases.

**9. Use Dated or Versioned Filenames**

Pattern: `plans/YYYYMMDD-feature-name.md` or `specs/001-feature-name/`

Avoids conflicts when multiple features planned simultaneously, creates chronological record, enables comparisons across iterations.

**10. Don't Ask "Is This Plan Okay?" When Using ExitPlanMode**

The tool inherently requests approval. Asking separately is redundant and confusing.

**11. Provide Escape Hatches for Simple Tasks**

Like claude-code-pro's Quick Mode: Skip planning overhead for straightforward work while retaining quality hooks. Adaptive granularity improves velocity.

**12. Document Decisions and Errors in Plans**

Both technical decisions (with rationale) and errors encountered (with resolutions) should be captured. Creates learning artifacts, prevents repeated mistakes, informs future work.

### Open Questions

**1. Optimal Phase Count?**

Sources suggest 3-7 phases but don't provide rigorous justification. Is there research on cognitive load or agent performance by phase granularity?

**2. When Does Planning Overhead Exceed Value?**

The "trivial task" threshold is subjective. Need empirical data: at what complexity level (measured by file count, LOC changed, dependency count) does formal planning improve outcomes?

**3. Template Standardization Efforts?**

Are there emerging standards for plan schema (like OpenAPI for APIs)? Would machine-readable plan formats enable better tooling?

**4. Multi-Agent Plan Coordination?**

Most systems use single-agent planning. How do the few multi-agent systems (agentic-startup's parallel execution) coordinate plan updates when multiple agents work simultaneously?

**5. Plan Versioning Best Practices?**

When plans change during implementation (scope adjustments, discovered blockers), how should versions be managed? Git history? Explicit v1/v2 files? Changelog sections?

**6. Integration with Project Management Tools?**

Plans are markdown files, but teams use Jira/Linear/etc. Are there patterns for syncing plan state to external systems?

**7. Cost/Benefit Analysis?**

No sources provided data on planning phase costs (tokens, time) vs. implementation savings (fewer iterations, reduced debugging). What's the ROI curve?

### Sources

1. [GitHub - maxritter/claude-codepro](https://github.com/maxritter/claude-codepro) - Production-grade spec-driven workflow
2. [GitHub - hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) - Curated list of skills and tools
3. [GitHub - OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) - Manus-style three-file pattern
4. [Armin Ronacher - What Actually Is Claude Code's Plan Mode?](https://lucumr.pocoo.org/2025/12/17/what-is-plan-mode/) - Critical analysis of native plan mode
5. [ClaudeLog - Plan Mode Mechanics](https://claudelog.com/mechanics/plan-mode/) - Technical documentation
6. [Steve Kinney - Claude Code Plan Mode](https://stevekinney.com/courses/ai-development/claude-code-plan-mode) - Practical guide
7. [GitHub - Pimzino/claude-code-spec-workflow](https://github.com/Pimzino/claude-code-spec-workflow) - Spec-driven development workflow
8. [GitHub - rsmdt/the-startup](https://github.com/rsmdt/the-startup) - Agentic Startup orchestration
9. [GitHub - schoolofai/claude-code-command-template](https://github.com/schoolofai/claude-code-command-template) - PRD-based workflow
10. [ZenML - Manus Context Engineering Strategies](https://www.zenml.io/llmops-database/context-engineering-strategies-for-production-ai-agents) - Manus AI planning patterns
11. [Alex Kurkin - Research → Plan → Implement Framework](https://www.alexkurkin.com/guides/claude-code-framework) - Phase-driven execution
12. [Gist - shamshirz/project-plan template](https://gist.github.com/shamshirz/eb1dac86bc7238f228ed58d1fac5fba2) - Seven-step specification
13. [Gist - Sothatsit/plan.md template](https://gist.github.com/Sothatsit/c9fcbcb50445ebb6f367b0a6cab37f3a) - Alternative planning structure
14. [GitHub - brilliantconsultingdev/claude-research-plan-implement](https://github.com/brilliantconsultingdev/claude-research-plan-implement) - Research-plan-implement workflow
15. [Anthropic - Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) - Official guidance
16. [GitHub - Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts/blob/main/system-prompts/tool-description-exitplanmode.md) - ExitPlanMode tool description
17. [ruvnet/claude-flow Wiki - CLAUDE.md Templates](https://github.com/ruvnet/claude-flow/wiki/CLAUDE-MD-Templates) - Template collection
18. [Manus AI Context Engineering Blog](https://www.manusai.io/blog/context-engineering-for-ai-agents-lessons-from-building-manus) - Context engineering strategies

---

## Key Sources

- [Anthropic - Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)

**Full sources:** [[research/outputs/OUTPUT-20260121-210630-how-claude-code-customized-environments/sources]]
