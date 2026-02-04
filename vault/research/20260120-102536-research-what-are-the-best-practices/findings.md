---
type: research-output
id: OUTPUT-20260120-102536-research-what-are-the-best-practices
target: '[[research/targets/TARGET-20260120-102231-the-best-practices-for-using-claude]]'
created: 2026-01-20
researcher: claude-deep-research
tags:
  - research
---

# Research Output: : What are the best practices for using Claude Code effectively?

This is for TA

**Target:** [[research/targets/TARGET-20260120-102231-the-best-practices-for-using-claude]]

**Question:** Research: What are the best practices for using Claude Code effectively?

This is for TARGET-20260120-102231.

Focus on:
1. Prompt engineering tips for Claude Code
2. Workflow patterns that work well
...

---

## Findings

Now I have comprehensive information from official Anthropic sources and well-regarded community resources. Let me synthesize this into a concise, actionable research output.

Claude Code best practices center on three core principles: structured context through CLAUDE.md files, workflow discipline (research-plan-execute), and strategic context management. Official Anthropic guidance emphasizes that Claude Code is intentionally unopinionated, providing raw model access that requires thoughtful configuration rather than prescribed workflows.

## Research Summary

### Question/Topic
What are the best practices for using Claude Code effectively, with focus on prompt engineering tips, workflow patterns, and common pitfalls to avoid.

### Key Findings

1. **CLAUDE.md files are the most powerful configuration mechanism** - They provide persistent project context that Claude automatically loads, and should be iteratively refined based on performance rather than exhaustively documented upfront.

2. **Research-Plan-Execute workflow prevents premature implementation** - Without explicit research and planning steps, Claude jumps straight to coding. Asking for exploration and plans first dramatically improves outcomes for complex tasks.

3. **Context management at 70% threshold is critical** - The `/compact` command should be invoked at 70% context usage (not 90%+), though experienced users prefer `/clear` + documentation patterns for complex tasks.

4. **Specificity in prompts yields exponentially better results** - Vague requests like "add tests for foo.py" produce generic outputs, while specific instructions like "write test case for foo.py covering the logged-out user edge case; avoid mocks" succeed on first attempt.

5. **Visual context dramatically improves UI development** - Screenshots, design mocks, and iterative visual comparison workflows produce significantly better results than text-only descriptions.

### Detailed Analysis

#### CLAUDE.md Optimization

CLAUDE.md files should contain project-specific guidance that persists across sessions:

**Recommended content:**
- Common bash commands with descriptions (`npm run test`, `npm run build`)
- Core utility functions and file locations
- Code style guidelines ("Use ES modules, not CommonJS")
- Testing procedures and requirements
- Repository standards (branching, merge strategies)
- Project-specific quirks or warnings

**Placement strategy:**
- Repository root for project-wide rules
- Parent directories for monorepo shared conventions
- Child directories for module-specific guidelines
- Home folder (`~/.claude/CLAUDE.md`) for personal preferences

**Anti-pattern:** Creating exhaustive documentation upfront without iteration. CLAUDE.md files become part of Claude's prompts and should be refined like any frequently-used prompt—add rules based on observed failure patterns, not hypothetical scenarios.

**Data-driven optimization:** Research from Arize demonstrated +10.87% accuracy improvements on Django issues by tailoring system prompts to specific codebases versus +5.19% for generic cross-repository optimization. The key is collecting LLM-generated feedback on task performance and using meta-prompting to synthesize refined instructions.

#### Proven Workflow Patterns

**1. Explore-Plan-Code-Commit (Primary Pattern)**

Without research and planning steps, Claude tends to jump straight to coding. The recommended sequence:

```bash
# Phase 1: Explore (explicitly prevent coding)
> Read the authentication module files—don't code yet

# Phase 2: Plan (use thinking modes for complex tasks)
> Think through how to add OAuth support and create a plan
# Toggle thinking: Option+T (macOS) or Alt+T (Windows/Linux)

# Phase 3: Code (implement incrementally)
> Implement the OAuth provider registration

# Phase 4: Commit (capture decisions)
> Commit these changes with a descriptive message
```

**Thinking mode budget:** Up to 31,999 tokens for reasoning before responding. Best for architectural decisions, challenging bugs, and evaluating tradeoffs.

**2. Test-Driven Development**

TDD becomes more powerful with agentic coding:

```bash
# 1. Generate tests from requirements
> Write tests for the notification service based on these input/output pairs

# 2. Confirm tests fail
> Run the tests—they should fail since we haven't implemented yet

# 3. Commit tests first
> Commit the test suite

# 4. Implement iteratively
> Implement notification service until all tests pass

# 5. Use subagents to verify
> Have a separate Claude instance review for overfitting
```

Claude examines existing test files to match style, frameworks, and assertion patterns already in use.

**3. Visual Iteration for UI**

For design implementation, visual feedback loops are essential:

```bash
# 1. Provide reference (drag-drop, paste, or path)
> Here's the design mockup: [image]

# 2. Initial implementation
> Generate the component matching this design

# 3. Screenshot comparison (use Puppeteer MCP)
> Take a screenshot of the result and compare to the mockup

# 4. Iterate 2-3 rounds
> Adjust the spacing and colors to match more closely
```

Pasting screenshots uses `Ctrl+V` (not `Cmd+V` on macOS).

**4. Codebase Onboarding**

Ask exploratory questions as you would a colleague:

```bash
# Start broad
> Give me an overview of this codebase

# Understand patterns
> Explain the main architecture patterns used here
> What are the key data models?

# Drill down
> How is authentication handled?
> Trace the login process from front-end to database
```

Start with broad questions, then narrow down. Request project-specific glossaries of terms.

#### Prompt Engineering Best Practices

**1. Be Specific About Task Scope**

Poor: "fix the bug"
Better: "fix the memory leak in the user authentication service by properly closing database connections in the logout handler"

Structure using WHAT-WHERE-HOW-VERIFY:
- **What:** The specific change needed
- **Where:** Exact file and function/component
- **How:** Approach or constraints
- **Verify:** Expected outcome or test

**2. Provide Context and Motivation**

Claude generalizes better from motivated instructions. Instead of "Don't use console.log," explain "We use Winston for structured logging because console.log doesn't integrate with our production monitoring."

**3. Use Few-Shot Examples Strategically**

Start with one example (one-shot). Only add more if output doesn't match needs. Match your prompt formatting style to desired output style—Claude mirrors the structure you provide.

**4. Leverage @ Syntax for File References**

```bash
# Single file
> Explain the logic in @src/utils/auth.js

# Directory listing
> What's the structure of @src/components?

# Multiple references
> Compare @file1.js and @file2.js
```

This adds relevant CLAUDE.md files from referenced directories and their parents automatically.

**5. Include Visual Context When Relevant**

Screenshots, diagrams, and design mocks dramatically improve results for UI work. Methods:
- Drag and drop into terminal
- Copy and paste with `Ctrl+V`
- Provide file paths: "Analyze this image: /path/to/image.png"

**6. Course Correct Early**

- Press `Escape` to interrupt any phase while preserving context
- Double-tap `Escape` to jump back in history and explore alternatives
- Request undo operations: "Undo the last change and try this approach instead"
- Ask for plans before coding to validate direction

#### Permission Management

Control tool access strategically:

- **Interactive allowlisting:** "Always allow" during prompts
- **Command-based:** `/permissions` to adjust allowlist
- **Settings file:** Edit `.claude/settings.json` (recommended for team sharing)
- **CLI flags:** `--allowedTools` for session-specific permissions

**Safe YOLO mode:** Use `--dangerously-skip-permissions` in isolated containers for uninterrupted workflows like linting fixes or boilerplate generation.

#### Custom Slash Commands

Store prompt templates in `.claude/commands/` for shareable workflows:

```bash
# Project-specific (shared)
mkdir -p .claude/commands
echo "Analyze performance and suggest three optimizations:" > .claude/commands/optimize.md

# With arguments
echo 'Find and fix issue #$ARGUMENTS...' > .claude/commands/fix-issue.md

# Usage
> /optimize
> /fix-issue 123

# Personal (user-only)
mkdir -p ~/.claude/commands
echo "Review for security vulnerabilities..." > ~/.claude/commands/security-review.md
```

#### Session Management

```bash
# Continue most recent session
claude --continue

# Resume specific session
claude --resume auth-refactor

# Interactive picker (navigate with ↑/↓, P preview, R rename, / search)
claude --resume

# Name during work
> /rename auth-refactor

# Fork to parallel work (sessions group together)
```

**Git worktrees for parallel development:**

```bash
git worktree add ../project-feature-a -b feature-a
git worktree add ../project-bugfix bugfix-123

cd ../project-feature-a && claude
cd ../project-bugfix && claude

# Cleanup
git worktree remove ../project-feature-a
```

Each instance has isolated file state while sharing Git history and remotes.

### Limitations & Gotchas

**1. Context Degradation is the Primary Failure Mode**

The `/compact` command should be invoked at 70% context usage, not 90%+. It reduces usage by ~50%, freeing ~70K tokens for 130K total available.

**Recommended thresholds:**
- **0-50%:** Work freely
- **50-70%:** Monitor and prepare
- **70-85%:** `/compact` immediately
- **85-95%:** Emergency `/compact`
- **95%+:** `/clear` required

**Power user preference:** Many experienced users avoid `/compact` because automatic compaction is opaque and error-prone. Preferred alternatives:

1. **`/clear` + `/catchup`:** Clear state, then run custom command to read all changed files in the git branch
2. **"Document & Clear":** Have Claude dump its plan/progress to a `.md` file, `/clear`, then start new session by reading the documentation

**2. Auto-Accept Without Review**

Coding agents don't critique their own work—they ship the first thing that compiles. Security vulnerabilities, edge cases, and code quality issues slip through. Use Plan Mode (`--permission-mode plan` or `Shift+Tab` toggle) for multi-step implementations requiring review.

**3. Vibe Coding vs. Production Code**

"Vibe coding" works for throwaway MVPs, but production code requires structured thinking, validation, and documentation. Skip planning at your peril.

**4. Context Window Mismanagement**

Using `/clear` between unrelated tasks maintains performance during long sessions. However, clearing mid-task loses critical context—use `/compact` strategically instead.

**5. CLAUDE.md Bloat**

Adding extensive content without iterating on effectiveness creates noise. The `/init` command generates starter files—refine them based on observed failure patterns rather than comprehensive documentation.

**6. Skipping Exploration Phase**

Jumping to implementation without understanding existing patterns leads to inconsistent code that doesn't match project conventions. Always start with codebase exploration for unfamiliar areas.

**7. Generic Documentation Requests**

"Add documentation" produces generic output. Better: Let Claude examine existing docs first to match tone, structure, and conventions already established.

### Recommendations

1. **Start every new codebase with structured onboarding** - Ask broad overview questions, drill down to patterns, then specific implementations. Build mental model before coding.

2. **Create project-specific slash commands for repeated workflows** - Testing procedures, linting patterns, deployment checks—anything you do more than twice becomes a command.

3. **Use Plan Mode for multi-file changes** - Toggle with `Shift+Tab` or start with `claude --permission-mode plan`. Have Claude ask clarifying questions and create implementation plans before touching code.

4. **Invoke `/compact` at 70% context usage** - Don't wait until 90%+. For complex tasks, prefer "Document & Clear" pattern over relying on automatic compaction.

5. **Iterate on CLAUDE.md based on failure patterns** - When Claude makes a mistake, add the pattern to CLAUDE.md and commit to git. Next session reads the updated rules.

6. **Include screenshots for any UI work** - Visual context produces exponentially better results. Use iterative screenshot comparison for polishing.

7. **Create custom subagents for specialized review** - One Claude writes code, another reviews independently. Separation yields better outcomes than single-instance handling.

8. **Use Git worktrees for parallel feature development** - Multiple Claude instances on same repo create conflicts. Worktrees provide isolated file state with shared history.

### Open Questions

- **Optimal thinking token budgets for different task complexities** - Default is up to 31,999 tokens, but there's limited guidance on when to constrain budgets for faster responses versus maximizing reasoning depth.

- **CLAUDE.md optimization metrics** - While Arize demonstrated +10.87% accuracy gains through data-driven optimization, there's no standardized framework for measuring effectiveness of CLAUDE.md changes across different project types.

- **Multi-agent orchestration patterns** - Official guidance covers parallel review and git worktrees, but best practices for complex multi-agent workflows (e.g., one agent for architecture, another for implementation, third for testing) remain underdocumented.

### Sources

1. [Claude Code: Best practices for agentic coding - Anthropic](https://www.anthropic.com/engineering/claude-code-best-practices) - Official Anthropic guide covering CLAUDE.md optimization, proven workflows, tool integration, and common pitfalls
2. [Common workflows - Claude Code Docs](https://code.claude.com/docs/en/common-workflows) - Official documentation of research-plan-execute patterns, session management, specialized subagents, and anti-patterns
3. [CLAUDE.md: Best Practices Learned from Optimizing Claude Code - Arize](https://arize.com/blog/claude-md-best-practices-learned-from-optimizing-claude-code-with-prompt-learning/) - Data-driven optimization study showing +10.87% accuracy gains through repository-specific prompt refinement
4. [Managing Claude Code's Context: a practical handbook - CometAPI](https://www.cometapi.com/managing-claude-codes-context/) - Context management strategies, /compact command usage thresholds (70% recommendation), and power user alternatives
5. [Prompting best practices - Claude Docs](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) - General prompt engineering principles adapted to Claude Code context (specificity, motivation, few-shot examples)

---

## Key Sources

- [Claude Code: Best practices for agentic coding - Anthropic](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Common workflows - Claude Code Docs](https://code.claude.com/docs/en/common-workflows)

**Full sources:** [[research/outputs/OUTPUT-20260120-102536-research-what-are-the-best-practices/sources]]
