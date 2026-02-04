---
type: research-output
id: OUTPUT-20260120-195412-claude-code-community-workflows-for
target: '[[research/targets/TARGET-20260120-102231-the-best-practices-for-using-claude]]'
created: 2026-01-20
researcher: claude-deep-research
tags:
  - research
---

# Research Output: Claude Code community workflows for session management and memory persistence.

**Target:** [[research/targets/TARGET-20260120-102231-the-best-practices-for-using-claude]]

**Question:** Research Claude Code community workflows for session management and memory persistence.

## Context
I'm building a "Symbiotic Collaboration Framework" for Claude Code that includes:
- Session lifecycl...

---

## Findings

Excellent. I now have comprehensive information across multiple dimensions. Let me compile the final research output.

Based on my comprehensive investigation of Claude Code community workflows for session management and memory persistence, I've examined over 40 sources including GitHub repositories, documentation, blog posts, and community discussions. This research reveals a mature ecosystem of patterns, tools, and best practices that have emerged in 2024-2025.

## Research Summary

### Question/Topic
Investigation of Claude Code community workflows focusing on: 1) Session management approaches and context continuity patterns, 2) Memory/context persistence mechanisms, 3) Workflow automation using hooks and custom commands, and 4) Adoptable patterns and anti-patterns relevant to the Symbiotic Collaboration Framework.

### Key Findings

1. **No native session handoff exists** - Claude Code provides checkpointing and session resume, but lacks native session-to-session handoff mechanisms. The community has developed file-based workarounds using memory banks, decision logs, and persistent directories.

2. **MCP-based memory servers have emerged** - Multiple Model Context Protocol servers (MCP Memory Keeper, MCP Memory Service, WhenMoon Memory MCP) provide persistent memory across sessions using SQLite and semantic search.

3. **Research → Plan → Implement is the dominant workflow pattern** - Most sophisticated frameworks separate research, planning, and execution phases with context clearing between phases and persistent storage of artifacts.

4. **CLAUDE.md as living documentation** - Best practice treats CLAUDE.md as a persistent, evolving context layer that accumulates team knowledge through incremental commits during development.

5. **Obsidian integration is well-established** - Multiple MCP servers and plugins enable Claude Code to interact with Obsidian vaults for knowledge management and session memory.

6. **Hooks enable powerful automation** - SessionStart/SessionEnd hooks (available but underutilized) support environment setup, dependency sync, transcript archival, and cleanup workflows.

### Detailed Analysis

#### Memory Persistence Patterns

**MCP Memory Servers**

The community has developed several MCP-based memory solutions that address Claude Code's lack of native cross-session memory:

**MCP Memory Keeper** (mkreyman/mcp-memory-keeper):
- SQLite-based storage in `~/mcp-data/memory-keeper/`
- Session tracking with project directory and git branch auto-detection
- Channel system for topic organization
- Checkpoint/restore pattern for context handoffs
- Token budget management (default 25k with 80% safety buffer)
- Multi-session collaboration through shared channels

**MCP Memory Service** (doobidoo/mcp-memory-service):
- Three storage options: SQLite (local), Cloudflare Workers (cloud), or hybrid
- Semantic search using AI embeddings for context retrieval
- Knowledge graphs with D3.js visualization
- Quality scoring via ONNX models
- Graph traversal tools (5-25ms lookups, 30x faster than alternatives)
- Automatic hooks capture context during sessions
- Web dashboard at localhost:8000 for memory management

**Architecture Pattern**: Both solutions operate as middleware that captures context during sessions and injects relevant memories at session start through semantic matching, effectively simulating cross-session continuity without native support.

**File-Based Memory Banks**

Several frameworks implement persistent file storage for session continuity:

**RIPER Workflow** (tony/claude-code-riper-5):
- Branch-aware memory bank at `.claude/memory-bank/`
- Separate namespaces per git branch (e.g., `main/`, `feature-auth-v2/`)
- Three artifact types: plans/, reviews/, sessions/
- Automatic branch detection via `git branch --show-current`
- Substep execution granularity (e.g., `/riper:execute 2.3` resumes mid-task)
- Decoupled phases with documented outputs as canonical references

**Research-Plan-Implement Framework** (brilliantconsultingdev/claude-research-plan-implement):
- Persistent storage in `thoughts/shared/` directory
- Structured subdirectories: research/, plans/, sessions/, cloud/
- Eight numbered commands for workflow phases
- Save/resume pattern for session continuity
- Parallel agent execution with shared knowledge store

**Pattern**: Both use git-tracked directory structures to persist decisions, plans, and context. The key innovation is treating filesystem artifacts as the memory layer rather than relying on Claude's context window.

#### Session Management Approaches

**Native Claude Code Capabilities**

- `claude --continue` or `claude -c`: Resume most recent session
- `claude --resume <id>` or `claude -r <id>`: Resume specific session by ID
- Background process persistence with output buffer tracking
- File context memory (remembers files accessed via Read/Edit/Write)
- Working directory and permission persistence
- Checkpointing: Automatic state capture before edits, accessible via `/rewind`

**Limitations**:
- Sessions don't survive system reboots
- Machine-local only (not cloud-synced)
- Background processes may timeout during extended idle
- Checkpointing doesn't track bash command file modifications
- No native session handoff or warm start from previous sessions

**Community Workarounds**

**Session Handoff Pattern** (feature requested but not native):
- Community proposals suggest `.claude/handoff.md` for session summaries
- Warm start capability where new sessions auto-load recent checkpoint
- Cross-session memory for project-level decisions
- Current implementations use custom hooks or commands to create handoff files

**Context Preservation Strategies**:

1. **Document & Clear**: Have Claude dump plan/progress to .md file, `/clear` context, start new session by reading the file
2. **Memory Bank + Resume**: Store decisions in persistent files, reference on session start
3. **MCP Memory Injection**: Automatic context retrieval via semantic search at session initialization

**SessionStart/SessionEnd Hooks**:
- SessionStart: Load context, install dependencies, restore environment
- SessionEnd: Archive transcripts, cleanup temp files, create session reports
- GitButler example: Create commit after every session with changes in separate branches
- Transcript archival: Copy `transcript_path` to shared drive or knowledge base

#### Workflow Automation Patterns

**Hook Events and Use Cases**

Claude Code provides six hook types with different automation capabilities:

1. **SessionStart** - Environment setup, dependency installation, context loading
2. **SessionEnd** - Transcript archival, cleanup, session reports (non-blocking)
3. **PreToolUse** - Permission enforcement, dangerous operation blocking (can block with exit 2)
4. **PostToolUse** - Auto-formatting, linting, test execution
5. **PermissionRequest** - Custom permission logic
6. **Stop** - Determine whether Claude continues execution

**Real-World Automation Examples**:

**GitButler Team** (blog.gitbutler.com):
- SessionEnd hook creates commit after every chat session
- Multiple simultaneous sessions store changes in different branches
- Automatic branch management for parallel work streams

**Dependency Sync** (SessionStart pattern):
- Auto-run `npm install`, `bundle install`, `pip install -r requirements.txt`
- Especially useful with git worktrees (different dependency states per worktree)

**Logging and Compliance** (Notification hook):
- Track and count all executed commands
- Provide automated feedback when code violates conventions
- Send notifications for task completion

**Security Gates** (PreToolUse):
- Block modifications to production files
- Prevent sensitive directory access
- Enforce branch-specific permissions

**Quality Automation** (PostToolUse):
- Code formatting after file edits
- TypeScript type-checking
- Test suite execution
- ESLint custom rules

**Skills and Custom Commands**

Skills are domain-knowledge documents in `.claude/skills/` with YAML frontmatter. Key patterns:

**Skill Evaluation Hooks**: Analyze prompts and auto-suggest which skills to activate based on keywords, file paths, and intent patterns

**Command-Based Automation**: Store prompt templates in `.claude/commands/` as Markdown files, accessible via `/` menu. Common pattern: Identify weekly/daily workflows, codify as commands, reduce to single slash prompts.

**Example Commands**:
- Linear integration: Read issue → create implementation plan
- `/todo-all`: Loop autonomous task processing (agents run 1-2+ hours unattended)
- `/context_gather`: Pull from multiple sources (memory, LSP analysis, codebase) and synthesize briefing

#### CLAUDE.md Best Practices

The community has converged on specific CLAUDE.md patterns:

**Content Organization** (2024-2025 consensus):

1. **WHAT**: Tech stack, project structure, codebase map (especially for monorepos)
2. **WHY**: Project purpose, function of different parts
3. **HOW**: Workflow specifics (bun vs node, testing commands, deployment)

**Progressive Disclosure Pattern**:
- Don't include all instructions in CLAUDE.md
- Keep task-specific instructions in separate markdown files with descriptive names
- List these files in CLAUDE.md with brief descriptions
- Instruct Claude to decide which are relevant and read before starting

**Living Documentation Approach**:
- Use `#` frequently during coding to document commands, files, style guidelines
- Accumulate repeated instructions into CLAUDE.md
- Include CLAUDE.md changes in commits so team benefits
- Treat as data-driven flywheel: Bugs → Improved CLAUDE.md → Better Agent

**Key Constraints**:
- Keep concise - frontier LLMs can follow ~150-200 instructions with consistency
- Claude ignores CLAUDE.md if not relevant to current task
- More irrelevant information = higher likelihood Claude ignores instructions
- Location precedence: `.claude/CLAUDE.md` → `./CLAUDE.md` → `~/.claude/CLAUDE.md`

**Analysis of 253 Real CLAUDE.md Files** (academic study):
- Shallow hierarchies with one main heading and several subsections
- Content dominated by: operational commands, technical implementation notes, architecture
- Most effective when concise and universally applicable

#### Obsidian Integration Workflows

**MCP Server Implementation** (iansinnott/obsidian-claude-code-mcp):

**Architecture**:
- Dual transport: WebSocket (Claude Code) + HTTP/SSE (Claude Desktop)
- Shared tools: File operations (read, write, str_replace, create, insert), workspace context, Obsidian API
- IDE-specific tools (WebSocket only): Diagnostics, diffs, tab management
- Legacy protocol support (HTTP with SSE, 2024-11-05)

**Operations Supported**:
- Read/write vault notes
- Retrieve active file context
- Access workspace file structure
- Direct Obsidian API calls

**Workflow Patterns** (kyleygao.com, forum.obsidian.md):

1. **Context Layer Architecture**: Treat Obsidian as persistent context layer storing decisions, constraints, workflows; use skills/commands for reusable tasks

2. **Automated Linking**: Claude reads journal entries, adds backlinks to people/places/books, searches vault for existing entities, creates new notes if needed

3. **Daily/Weekly/Monthly Aggregation**: Daily notes → weekly summaries → monthly reviews; conversational daily note creation with smart linking

4. **Research Workflows**: Web search → synthesize findings → create linked notes with sources and related links

5. **Command-Based Automation**: Codify repeated workflows as commands, reduce to single slash prompts

**Friction Reduction**: Users report using Obsidian more because Claude removes organization overhead—capturing a thought doesn't mean committing to 10 minutes of manual work.

**Technical Setup**: Plugin creates MCP server in Obsidian, Claude Code connects via WebSocket, auto-discovery and file operations work across both clients.

#### Research Workflow Patterns

**Dominant Pattern: Research → Plan → Implement**

Multiple frameworks independently converged on this three-phase approach:

**Phase Separation Benefits**:
- Without research/plan phases, Claude jumps straight to coding
- Research first significantly improves performance for complex problems
- Context clearing between phases prevents contamination
- Persistent storage enables resumption at any phase

**RIPER Workflow** (Research → Innovate → Plan → Execute → Review):
- Five phases with three consolidated agents
- research-innovate agent: Read-only access for investigation
- plan-execute agent: Full file access for specs and implementation
- review agent: Test execution for validation
- Mode-specific restrictions prevent premature implementation
- Memory bank stores plans as canonical references during execution

**Research-Plan-Implement Framework** (brilliantconsultingdev):
- Eight numbered commands for workflow phases
- Parallel AI agents for research questions
- Phased implementation specifications
- Validation against success criteria
- Save/resume for session continuity

**Four-Phase Alternative**:
- Research → Plan → Implement → Validate
- Clear context between each phase
- Save everything to `thoughts/` directory
- Natural checkpoints for session handoffs

**Knowledge Gathering Patterns**:

**Multi-Source Context** (context_gather pattern):
- Search memory for past decisions/patterns
- LSP-powered analysis of current codebase
- Synthesize into briefing
- Combination of exhaustive analysis and rapid refinement

**Parallel Agent Research**:
- Spawn multiple agents with specific research questions
- Read-only access prevents premature changes
- Agents document findings in shared directory
- Main session consumes research artifacts

### Limitations & Gotchas

**Context Management Pitfalls**

1. **Automatic Compaction Issues**:
   - Opaque, error-prone, not well-optimized
   - Many experienced users avoid auto-compaction
   - Recommendation: Manual `/compact` at 70% (not 90%) capacity
   - Better: `/clear` + `/catchup` or "Document & Clear" pattern

2. **Context Poisoning**:
   - Context bleeding without explicit task boundaries
   - Claude carries forward expectations from previous tasks
   - Example: Update code → deploy sequence causes all future updates to trigger deployment
   - Fix: `/clear` between task types, use different sessions for different work

3. **Instruction Decay**:
   - Instructions at conversation start lose importance as conversation grows
   - AI models pay more attention to recent messages
   - Fix: Refresh critical instructions or use `/compact`

4. **Multi-Agent Context Loss**:
   - Declining agent draft spawns fresh copy instead of iterating
   - All agent-specific context disappears
   - Handoff artifacts required for agent coordination

**Session Management Gotchas**

1. **Checkpointing Limitations**:
   - Does NOT track bash command file modifications
   - Only tracks files edited within current session
   - Only direct file edits via Claude's tools are tracked
   - Workaround: Commit frequently, use git for bash-modified files

2. **Session Persistence Boundaries**:
   - Sessions don't survive system reboots
   - Machine-local only (not cloud-synced)
   - Background processes may timeout during extended idle
   - No native cross-session handoff

3. **Todo List Non-Persistence**:
   - Claude Code todo lists don't persist across sessions
   - When context fills and you start new conversation, todos are gone
   - Workaround: Use runbook.md or similar file-based task tracking

**Subagent Anti-Patterns**

1. **Over-Agent-ization**:
   - Large fleets of 10-15+ agents consume 200k token budget quickly
   - Can run for 1+ hour before surfacing useful results
   - Each subagent adds another context window
   - Recommendation: Use Task/Explore feature instead of custom agents

2. **Complex Command Libraries**:
   - Long list of complex slash commands defeats natural language purpose
   - Forcing engineers to learn documented magic commands
   - Better: Give main agent context in CLAUDE.md, let it manage delegation

3. **Handoff Problem**:
   - Subagents start with blank slate when delegated
   - Without detailed brief, suffer "context amnesia"
   - Fix: Use handoff contracts/artifacts preserving required information

**CLAUDE.md Anti-Patterns**

1. **Sprawling Documentation**:
   - Disorganized, overly long files
   - Claude keeps asking same basic questions
   - Claude ignores content if not relevant to current task
   - Fix: Keep concise, universally applicable; use progressive disclosure

2. **Missing CLAUDE.md**:
   - Every project must have CLAUDE.md
   - Without it, knowledge doesn't persist across sessions
   - Team doesn't benefit from accumulated learning

3. **Too Many Instructions**:
   - LLMs can follow ~150-200 instructions max
   - More irrelevant info = higher ignore rate
   - Fix: Include minimum necessary, move task-specific to separate files

### Recommendations

Based on this comprehensive research, here are the top recommendations for the Symbiotic Collaboration Framework:

#### 1. Adopt SessionStart/SessionEnd Hooks for Automation (HIGH PRIORITY)

**Why**: Native Claude Code feature, underutilized by community, perfect fit for framework needs.

**What to Adopt**:
- **SessionStart hook**: Load previous session handoff from Obsidian, set session number, prepare scratch.md
- **SessionEnd hook**: Export transcript to vault (already implemented), create session summary

**How it Maps**:
- `/begin` command logic → SessionStart hook (automatic vs manual trigger)
- `/wrap` command logic → SessionEnd hook + manual vault writes
- Consider hybrid: Keep `/wrap` for user control but add SessionEnd safety net

**Benefits**:
- Automates environment setup (dependency install, context loading)
- Ensures transcripts always archived (GitButler pattern)
- Aligns with community best practices
- Reduces manual session lifecycle management

**Caution**: SessionEnd hooks can't block termination, so critical operations should remain in `/wrap` or use git hooks.

#### 2. Implement Research → Plan → Implement Workflow with Phase Separation (HIGH PRIORITY)

**Why**: Most successful community pattern for complex work, prevents premature execution, enables natural session boundaries.

**What to Adopt**:
- Formalize three modes: Research (read-only exploration), Plan (specification creation), Execute (implementation)
- Clear context boundaries between phases
- Persistent artifact storage for each phase

**How it Maps to Framework**:
- Research mode → spawn `deep-research` agent or use Task/Explore
- Plan mode → brainstorming mode with specification output
- Execute mode → execution mode with TodoWrite tracking
- Each phase creates artifact in scratch.md or vault

**Benefits**:
- Prevents "jump to coding" anti-pattern
- Natural session handoff points (pause after research, resume at plan)
- Aligns with existing Mode 1/Mode 2 distinction
- Persistent plans serve as canonical references (like RIPER)

**Implementation**:
- Add phase markers to session handoff
- Create `thoughts/` or similar directory for phase artifacts
- Consider adding `/research`, `/plan`, `/execute` mode-switching commands

#### 3. Adopt Living CLAUDE.md + Progressive Disclosure Pattern (MEDIUM PRIORITY)

**Why**: Community consensus best practice, improves Claude performance, enables team knowledge accumulation.

**What to Adopt**:
- Treat CLAUDE.md as living documentation updated via commits
- Use progressive disclosure: Reference task-specific files rather than inline everything
- Implement "# frequently → accumulate to CLAUDE.md" workflow

**How it Maps**:
- Existing CLAUDE.md is already comprehensive and well-structured
- Add instruction to framework: "Use # during sessions to note repeated instructions"
- At `/wrap`, offer to update CLAUDE.md with accumulated patterns
- Stage CLAUDE.md changes in scratch.md for review before commit

**Benefits**:
- Aligns with community best practices
- Creates data-driven improvement flywheel
- Team benefits from accumulated knowledge
- Reduces token waste from repeated instructions

**Caution**: Keep CLAUDE.md concise (150-200 instructions max), universally applicable only.

### Open Questions

1. **Should we adopt MCP memory server integration?**
   - MCP Memory Keeper or Memory Service could supplement Obsidian
   - Adds semantic search and automatic context injection
   - Tradeoff: Additional dependency vs enhanced memory capabilities
   - Question: Does Obsidian MCP + manual handoff provide sufficient memory, or would semantic search add significant value?

2. **Should we implement branch-aware memory like RIPER?**
   - Current framework is branch-agnostic
   - RIPER's branch-aware memory bank prevents cross-branch contamination
   - Question: Is branch isolation valuable for our use case, or does it add unnecessary complexity?

3. **Should we formalize decision tracking beyond locked.md?**
   - Community has active feature requests for DECISIONS.md and ADR support
   - Pattern: Track not just decisions but rejected alternatives and rationale
   - Question: Should we create dedicated decision logging beyond current locked.md, perhaps with rejected-alternatives section?

4. **Should we implement autonomous task processing?**
   - Some users run `/todo-all` agents for 1-2+ hours autonomously
   - Enables "batch and walk away" workflows
   - Question: Does this align with framework philosophy, or do we prefer human-in-loop for all execution?

5. **Should scratch.md become git-tracked with staged/committed states?**
   - Current: Template committed, content reset before commit
   - Alternative: Track content evolution, commit after `/wrap` processing
   - Question: Is there value in git history of scratch.md content, or should it remain ephemeral staging only?

6. **How should we handle compaction strategy?**
   - Community consensus: Manual `/compact` at 70%, or "Document & Clear" pattern
   - Our framework: Stage in scratch.md, commit at `/wrap`, start fresh
   - Question: Should we add proactive context monitoring with `/compact` recommendations, or trust session-boundary approach?

### Sources

#### Session Management & Memory
1. [Manage Claude's memory - Claude Code Docs](https://code.claude.com/docs/en/memory)
2. [Feature Request: Persistent Memory Between Claude Code Sessions · Issue #14227](https://github.com/anthropics/claude-code/issues/14227)
3. [Claude Code Session Management | Steve Kinney](https://stevekinney.com/courses/ai-development/claude-code-session-management)
4. [Master Claude Code Memory in 7 Steps | Medium](https://alirezarezvani.medium.com/master-claude-memory-in-7-steps-cut-context-loss-by-80-with-project-scoped-recall-b1ff67f0bc2e)
5. [session persistence · ruvnet/claude-flow Wiki](https://github.com/ruvnet/claude-flow/wiki/session-persistence)
6. [Context persistence across sessions · Issue #2954](https://github.com/anthropics/claude-code/issues/2954)

#### Awesome Claude Code Resources
7. [awesome-claude-code | GitHub](https://github.com/hesreallyhim/awesome-claude-code)
8. [Awesome Claude Code - Visual Directory](https://awesomeclaude.ai/awesome-claude-code)
9. [How I Use Every Claude Code Feature | Shrivu Shankar](https://blog.sshh.io/p/how-i-use-every-claude-code-feature)
10. [I mastered the Claude Code workflow | Ashley Ha](https://medium.com/@ashleyha/i-mastered-the-claude-code-workflow-145d25e502cf)

#### CLAUDE.md Patterns
11. [Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices)
12. [Context Engineering for Claude Code](https://thomaslandgraf.substack.com/p/context-engineering-for-claude-code)
13. [Writing a good CLAUDE.md | HumanLayer Blog](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
14. [Using CLAUDE.MD files | Claude Blog](https://claude.com/blog/using-claude-md-files)
15. [Creating the Perfect CLAUDE.md | Dometrain](https://dometrain.com/blog/creating-the-perfect-claudemd-for-claude-code/)
16. [claude-code-showcase | GitHub](https://github.com/ChrisWiles/claude-code-showcase)

#### MCP Memory Solutions
17. [mcp-memory-keeper | GitHub](https://github.com/mkreyman/mcp-memory-keeper)
18. [mcp-memory-service | GitHub](https://github.com/doobidoo/mcp-memory-service)
19. [Adding Memory to Claude Code with MCP | Medium](https://medium.com/@brentwpeterson/adding-memory-to-claude-code-with-mcp-d515072aea8e)
20. [claude-memory-mcp | GitHub](https://github.com/WhenMoon-afk/claude-memory-mcp)
21. [The Claude you'll never need to remind: MCP in action](https://www.qed42.com/insights/the-claude-youll-never-need-to-remind-mcp-in-action)

#### Hooks & Workflow Automation
22. [Get started with Claude Code hooks - Docs](https://code.claude.com/docs/en/hooks-guide)
23. [Complete guide to hooks in Claude Code | eesel.ai](https://www.eesel.ai/blog/hooks-in-claude-code)
24. [How I'm Using Claude Code Hooks | Medium](https://medium.com/@joe.njenga/use-claude-code-hooks-newest-feature-to-fully-automate-your-workflow-341b9400cfbe)
25. [Automate Your AI Workflows with Claude Code Hooks | GitButler](https://blog.gitbutler.com/automate-your-ai-workflows-with-claude-code-hooks)
26. [Hooks reference - Docs](https://code.claude.com/docs/en/hooks)
27. [Feature Request: SessionStart and SessionEnd Hooks · Issue #4318](https://github.com/anthropics/claude-code/issues/4318)

#### RIPER Workflow
28. [RIPER-5 mode · Issue #164](https://github.com/hesreallyhim/awesome-claude-code/issues/164)
29. [claude-code-riper-5 | GitHub](https://github.com/tony/claude-code-riper-5)

#### Obsidian Integration
30. [obsidian-claude-code-mcp | GitHub](https://github.com/iansinnott/obsidian-claude-code-mcp)
31. [Using Claude Code with Obsidian | Kyle Gao](https://kyleygao.com/blog/2025/using-claude-code-with-obsidian/)
32. [Agent Client Plugin | Obsidian Forum](https://forum.obsidian.md/t/new-plugin-agent-client-bring-claude-code-codex-gemini-cli-inside-obsidian/108448)
33. [Obsidian × Claude Code: The Ultimate Workflow Guide](https://www.axtonliu.ai/newsletters/ai-2/posts/obsidian-claude-code-workflows)

#### Checkpointing & Session Handoff
34. [Checkpointing - Claude Code Docs](https://code.claude.com/docs/en/checkpointing)
35. [Feature Request: Session Handoff / Continuity Support · Issue #11455](https://github.com/anthropics/claude-code/issues/11455)
36. [Ccundo: "Restore Checkpoint" for Claude Code](https://apidog.com/blog/ccundo/)
37. [Claude Code Checkpoints: A Developer's Guide](https://skywork.ai/skypage/en/claude-code-checkpoints-ai-coding/1976917740735229952)

#### Task Management
38. [What is Todo List in Claude Code | ClaudeLog](https://claudelog.com/faqs/what-is-todo-list-in-claude-code/)
39. [Minimalist Claude Code Task Management Workflow | Nick Tune](https://medium.com/nick-tune-tech-strategy-blog/minimalist-claude-code-task-management-workflow-7b7bdcbc4cc1)
40. [claude-todo-emulator | GitHub](https://github.com/joehaddad2000/claude-todo-emulator)
41. [Claude Code: Keeping It Running for Hours | motlin.com](https://motlin.com/blog/claude-code-running-for-hours)

#### Subagent Patterns
42. [Create custom subagents - Docs](https://code.claude.com/docs/en/sub-agents)
43. [Best practices for Claude Code subagents | PubNub](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/)
44. [How to Use Claude Code Subagents to Parallelize Development](https://zachwills.net/how-to-use-claude-code-subagents-to-parallelize-development/)
45. [claude-code-sub-agent-collective | GitHub](https://github.com/vanzan01/claude-code-sub-agent-collective)
46. [Common Sub-Agent Anti-Patterns | Steve Kinney](https://stevekinney.com/courses/ai-development/subagent-anti-patterns)

#### Anti-Patterns & Best Practices
47. [The 4-Step Protocol That Fixes Context Amnesia | Medium](https://medium.com/@ilyas.ibrahim/the-4-step-protocol-that-fixes-claude-codes-context-amnesia-c3937385561c)
48. [An easy way to stop Claude code from forgetting the rules | DEV](https://dev.to/siddhantkcode/an-easy-way-to-stop-claude-code-from-forgetting-the-rules-h36)
49. [Poison Context Awareness | ClaudeLog](https://claudelog.com/mechanics/poison-context-awareness/)
50. [From Chaos to Control | Brandon Casci](https://www.brandoncasci.com/2025/07/30/from-chaos-to-control-teaching-claude-code-consistency.html)

#### Decision Tracking
51. [FEATURE: Decision History Tracking with DECISIONS.md · Issue #15222](https://github.com/anthropics/claude-code/issues/15222)
52. [FEATURE: Architecture Decision Records (ADRs) · Issue #13853](https://github.com/anthropics/claude-code/issues/13853)

#### Research Workflows
53. [claude-research-plan-implement | GitHub](https://github.com/brilliantconsultingdev/claude-research-plan-implement)
54. [Research → Plan → Implement: The Claude Code Framework | Alex Kurkin](https://www.alexkurkin.com/guides/claude-code-framework)
55. [How Claude Code Became My Knowledge Management System | Matt Stockton](https://mattstockton.com/2025/09/19/how-claude-code-became-my-knowledge-management-system.html)

#### Context Management
56. [Managing Claude Code's Context | CometAPI](https://www.cometapi.com/managing-claude-codes-context/)
57. [Managing Claude Code context to reduce limits | mcpcat.io](https://mcpcat.io/guides/managing-claude-code-context/)
58. [How Claude Code Got Better by Protecting More Context](https://hyperdev.matsuoka.com/p/how-claude-code-got-better-by-protecting)
59. [Claude Code Context Management | Medium](https://medium.com/@kushalbanda/claude-code-context-management-if-youre-not-managing-context-you-re-losing-output-quality-71c2d0c0bc57)

#### Workspace & Settings
60. [Claude Code settings - Docs](https://code.claude.com/docs/en/settings)
61. [Never Lose Your Work: Session Management | DEV](https://dev.to/rajeshroyal/never-lose-your-work-session-management-that-saves-your-sanity-4dp8)
62. [Claude Code Security Best Practices | Backslash](https://www.backslash.security/blog/claude-code-security-best-practices)

---

## Key Sources

- [Manage Claude's memory - Claude Code Docs](https://code.claude.com/docs/en/memory)
- [Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Get started with Claude Code hooks - Docs](https://code.claude.com/docs/en/hooks-guide)
- [Hooks reference - Docs](https://code.claude.com/docs/en/hooks)
- [Checkpointing - Claude Code Docs](https://code.claude.com/docs/en/checkpointing)

**Full sources:** [[research/outputs/OUTPUT-20260120-195412-claude-code-community-workflows-for/sources]]
