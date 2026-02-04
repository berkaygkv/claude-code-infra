---
type: research-output
id: OUTPUT-20260124-202744-claude-codes-capabilities-for-dynamic
target: null
created: 2026-01-24
researcher: claude-deep-research
tags:
  - research
---

# Research Output: Claude Code's capabilities for dynamic context loading and conditional instruct

**Question:** Research Claude Code's capabilities for dynamic context loading and conditional instructions. Specifically investigate:

1. **CLAUDE.md features** — Can CLAUDE.md content be conditional based on runti...

---

## Findings

Perfect! I now have comprehensive information to provide a thorough research report. Let me compile my findings.

Claude Code's dynamic context loading capabilities are more sophisticated than simple conditional CLAUDE.md files, but they don't support direct runtime evaluation of different CLAUDE.md versions based on arguments. However, there are several powerful mechanisms that can achieve mode-based instruction loading. Here's what I found after investigating official documentation, GitHub repositories, and community patterns.

## Research Summary

### Question/Topic
Investigate Claude Code's capabilities for dynamic context loading and conditional instructions, specifically to enable loading different cognitive protocols (brainstorm vs build mode) based on runtime arguments like `/begin brainstorm` or `/begin build`, without cluttering context with both instruction sets.

### Key Findings

1. **CLAUDE.md has NO built-in conditional evaluation** - CLAUDE.md files are static and loaded wholesale; there's no native syntax for conditional blocks or runtime evaluation based on arguments.

2. **Skills with `$ARGUMENTS` and `!`command`` preprocessing exist** - These enable dynamic content injection but work differently than you might expect.

3. **SessionStart hooks with `additionalContext`** provide the most viable path for mode-based instruction loading at session initialization.

4. **Subagents with `context: fork`** can run skills with completely different system prompts in isolated contexts.

5. **The community "Superpowers" pattern** demonstrates a working brainstorm/build/execute workflow using separate skills.

### Detailed Analysis

#### 1. CLAUDE.md Conditional Loading

**Official capability**: CLAUDE.md files are **static markdown** that get loaded into context wholesale. No conditional syntax exists.

**Hierarchical loading**: Claude Code loads CLAUDE.md from multiple locations (home directory, parent directories, project root, child directories), but this is directory-based, not argument-based.

**Key limitation**: You cannot write `if (mode === 'brainstorm') { ... }` or use any conditional directives in CLAUDE.md itself.

**Source**: [Using CLAUDE.md files](https://claude.com/blog/using-claude-md-files), [Claude Code settings](https://code.claude.com/docs/en/settings)

#### 2. Skills System Dynamic Features

**`$ARGUMENTS` placeholder**: Skills support a `$ARGUMENTS` variable that gets replaced with whatever arguments follow the skill name.

```yaml
---
name: fix-issue
description: Fix a GitHub issue
---
Fix GitHub issue $ARGUMENTS following our coding standards.
```

When you run `/fix-issue 123`, Claude receives "Fix GitHub issue 123 following our coding standards..."

**Positional arguments (`$1`, `$2`, `$3`)**: Documented but **NOT IMPLEMENTED**. The official docs mention them, but empirical testing shows they remain as literal text due to security concerns around bash injection. Only `$ARGUMENTS` reliably works.

**`!`command`` preprocessing syntax**: This is the most powerful dynamic feature. Commands wrapped in backticks with `!` prefix execute **before** the skill content is sent to Claude.

```markdown
---
name: pr-summary
description: Summarize changes in a pull request
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

**Critical distinction**: This is **preprocessing**, not runtime evaluation. The commands run once when the skill loads, their output replaces the placeholders, and Claude sees the final rendered content. This isn't conditional logic—it's command substitution.

**Sources**: [Extend Claude with skills](https://code.claude.com/docs/en/skills), [Inside Claude Code Skills](https://mikhail.io/2025/10/claude-code-skills/), [M.academy lesson on arguments](https://m.academy/lessons/pass-arguments-custom-slash-commands-claude-code/)

#### 3. SessionStart Hooks with additionalContext

**This is your best option for mode-based loading.**

SessionStart hooks can inject context dynamically at session start. The hook receives JSON with a `source` field indicating how the session started (`"startup"`, `"resume"`, `"clear"`, `"compact"`).

**Implementation pattern**:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/load-mode-context.sh"
          }
        ]
      }
    ]
  }
}
```

Your hook script receives stdin with session metadata and can return JSON:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Your mode-specific instructions here"
  }
}
```

**The challenge**: SessionStart hooks don't directly receive skill arguments. You'd need to:

1. Store the desired mode in an environment variable or file
2. Have your `/begin` skill write the mode preference to a file
3. Have the SessionStart hook read that file and inject appropriate context

**Alternative approach**: Use the `/begin` skill itself to inject context directly (plain stdout with exit code 0 adds context):

```bash
#!/bin/bash
# In your /begin skill's preprocessing

MODE="$1"  # brainstorm or build

if [ "$MODE" = "brainstorm" ]; then
  cat /path/to/brainstorm-instructions.md
elif [ "$MODE" = "build" ]; then
  cat /path/to/build-instructions.md
fi
```

**Known issues**: There are several GitHub issues reporting SessionStart hook context not appearing correctly in certain scenarios, though the consensus is the context **is** loaded—it just may not display in the UI but Claude can still see it.

**Sources**: [Hooks reference](https://code.claude.com/docs/en/hooks), [LaunchDarkly SessionStart hook example](https://github.com/launchdarkly-labs/claude-code-session-start-hook), [GitHub issue #9591](https://github.com/anthropics/claude-code/issues/9591)

#### 4. Subagents with Context Fork

Skills can use `context: fork` to run in an isolated subagent with a completely different system prompt:

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:
1. Find relevant files
2. Analyze the code
3. Summarize findings
```

**How it works**:
- The skill content becomes the task prompt
- The `agent` field specifies which subagent configuration to use (Explore, Plan, general-purpose, or custom)
- The subagent runs in isolated context with its own system prompt
- Results are summarized and returned to main conversation

**Limitation**: This creates a **separate context**, not a mode switch in the main conversation. The subagent doesn't share your conversation history.

**Use case**: Perfect for isolating research or exploration (as you're already doing with `deep-research`), but not ideal for switching the main conversation's cognitive mode.

**Sources**: [Create custom subagents](https://code.claude.com/docs/en/sub-agents), [Extend Claude with skills](https://code.claude.com/docs/en/skills)

#### 5. The "Superpowers" Pattern

The open-source [Superpowers framework](https://github.com/obra/superpowers) implements exactly what you're describing: brainstorm → build → execute workflow using **separate skills**:

- `/superpowers:brainstorm` - Interactive design refinement (asks questions, explores alternatives)
- `/superpowers:write-plan` - Creates implementation plan
- `/superpowers:execute-plan` - Executes in batches with subagent-driven development

**Key insight**: They don't try to conditionally load CLAUDE.md. They use:
1. **Distinct skills** for each phase with `disable-model-invocation: true` (manual invocation only)
2. **Different system prompts** in each skill's content
3. **Orchestration** where one skill's output becomes context for the next

**Example structure**:

```yaml
# .claude/skills/brainstorm/SKILL.md
---
name: brainstorm
description: Interactive design refinement phase
disable-model-invocation: true
---

You are in BRAINSTORM mode. Your role is to refine rough ideas through questions.

Ask clarifying questions instead of jumping to code:
- What's the core user need?
- What constraints exist?
- What alternatives should we consider?

Save design document when approved.
```

```yaml
# .claude/skills/build-plan/SKILL.md
---
name: build-plan
description: Create implementation plan
disable-model-invocation: true
---

You are in BUILD mode. Create an implementation plan from the design.

Read the design document at: !`cat design.md`

Create a plan clear enough for a junior engineer:
- Break into discrete tasks
- Emphasize TDD (true red/green)
- Apply YAGNI and DRY principles
```

**Sources**: [Superpowers on GitHub](https://github.com/obra/superpowers), search results referencing the brainstorm/build/execute pattern

### Limitations & Gotchas

1. **No runtime conditional evaluation in CLAUDE.md**: You cannot have a single CLAUDE.md with `if (mode === X)` blocks. CLAUDE.md is markdown, not a templating language.

2. **`$1`, `$2`, `$3` positional args documented but not implemented**: Security concerns around bash injection. Only `$ARGUMENTS` works reliably.

3. **SessionStart `additionalContext` display bugs**: Multiple GitHub issues report the context loads but doesn't show in the UI. The context **is** there for Claude, just not visually obvious to users.

4. **`!`command`` is preprocessing, not conditional**: Commands execute once at skill load, not repeatedly during conversation. Can't use it for `if [ "$MODE" = "brainstorm" ]; then ...` logic.

5. **Skills don't inherit context between invocations**: Each skill invocation is fresh unless you use `context: fork` with a resumed subagent.

6. **Context budget constraints**: Loading large instruction sets into every session consumes your context window. The docs recommend keeping CLAUDE.md under 300 lines.

### Recommendations

Based on the research, here are actionable implementation paths ranked by viability:

#### Option 1: Separate Skills (Recommended - Cleanest)

Create `/brainstorm` and `/build` as distinct skills with different instructions:

```yaml
# .claude/skills/brainstorm/SKILL.md
---
name: brainstorm
description: Planning and design mode
disable-model-invocation: true
---

[Your planning-focused instructions]
```

```yaml
# .claude/skills/build/SKILL.md
---
name: build
description: Execution mode
disable-model-invocation: true
---

[Your execution-focused instructions]
```

**Pros**: 
- Clean separation
- No context pollution
- Follows established patterns (Superpowers)
- Works reliably with current Claude Code features

**Cons**: 
- Requires explicit skill invocation
- No shared state between modes (but you can read/write files)

#### Option 2: SessionStart Hook with File-Based Mode Storage

Have `/begin` write the mode to a file, then SessionStart hook reads it:

```bash
# /begin skill preprocessing
echo "$ARGUMENTS" > ~/.claude-mode

# SessionStart hook script
MODE=$(cat ~/.claude-mode 2>/dev/null || echo "build")

if [ "$MODE" = "brainstorm" ]; then
  jq -n --arg ctx "$(cat /path/to/brainstorm.md)" '{
    hookSpecificOutput: {
      hookEventName: "SessionStart",
      additionalContext: $ctx
    }
  }'
else
  jq -n --arg ctx "$(cat /path/to/build.md)" '{
    hookSpecificOutput: {
      hookEventName: "SessionStart",
      additionalContext: $ctx
    }
  }'
fi
```

**Pros**: 
- Mode persists across session restarts
- Loads appropriate context at session start
- Single command to set mode

**Cons**: 
- Requires session restart to change modes (or use `/clear`)
- File-based state management adds complexity
- SessionStart hook display bugs may confuse users

#### Option 3: UserPromptSubmit Hook for Dynamic Injection

Hook into every prompt and inject mode-specific context:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/inject-mode-context.sh"
          }
        ]
      }
    ]
  }
}
```

**Pros**: 
- Context injected on every interaction
- Can change modes mid-session

**Cons**: 
- Runs on **every** prompt (performance overhead)
- Context accumulates across conversation (bloat)
- Most invasive approach

#### Option 4: Hybrid - Skill + SessionStart Hook

Best of both worlds:

1. `/begin brainstorm` skill writes mode to file AND injects immediate context
2. SessionStart hook reads the file for session resumption
3. User gets instant feedback, mode persists across restarts

```yaml
# .claude/skills/begin/SKILL.md
---
name: begin
description: Start a session in a specific mode
argument-hint: [brainstorm|build]
---

!`echo "$ARGUMENTS" > ~/.claude-mode`
!`cat /path/to/$ARGUMENTS-mode.md`
```

**Pros**: 
- Immediate mode switch
- Persists across sessions
- Clean user experience

**Cons**: 
- Requires maintaining separate instruction files
- Relies on file system state

### Open Questions

1. **Can skill frontmatter be dynamically generated?** - No documented mechanism found. Frontmatter is static YAML parsed at load time.

2. **Can CLAUDE.md include other files conditionally?** - No. The `@AGENTS.md` import syntax exists but is static, not conditional.

3. **Will positional arguments (`$1`, `$2`, `$3`) ever be implemented?** - GitHub issues suggest it's blocked by security concerns. No timeline for implementation.

4. **Can hooks modify CLAUDE.md dynamically?** - Hooks can inject `additionalContext`, but cannot modify the CLAUDE.md file that was already loaded at session start.

5. **Is there a first-class "mode" concept coming?** - No indication in official roadmap or GitHub issues. Current thinking is skills + subagents provide sufficient primitives.

### Sources

1. [Extend Claude with skills - Claude Code Docs](https://code.claude.com/docs/en/skills)
2. [Creating the Perfect CLAUDE.md for Claude Code - Dometrain](https://dometrain.com/blog/creating-the-perfect-claudemd-for-claude-code/)
3. [Inside Claude Code Skills: Structure, prompts, invocation](https://mikhail.io/2025/10/claude-code-skills/)
4. [Claude Code Developer Cheatsheet](https://awesomeclaude.ai/code-cheatsheet)
5. [Hooks reference - Claude Code Docs](https://code.claude.com/docs/en/hooks)
6. [Create custom subagents - Claude Code Docs](https://code.claude.com/docs/en/sub-agents)
7. [GitHub - obra/superpowers](https://github.com/obra/superpowers)
8. [GitHub - ChrisWiles/claude-code-showcase](https://github.com/ChrisWiles/claude-code-showcase)
9. [GitHub - LaunchDarkly SessionStart hook](https://github.com/launchdarkly-labs/claude-code-session-start-hook)
10. [Pass arguments to custom slash commands in Claude Code - M.academy](https://m.academy/lessons/pass-arguments-custom-slash-commands-claude-code/)
11. [Claude Code customization guide - alexop.dev](https://alexop.dev/posts/claude-code-customization-guide-claudemd-skills-subagents/)
12. [Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices)
13. [Using CLAUDE.md files](https://claude.com/blog/using-claude-md-files)
14. [How to configure hooks](https://claude.com/blog/how-to-configure-hooks)
15. [GitHub Issue #9591 - SessionStart hook context not displayed](https://github.com/anthropics/claude-code/issues/9591)

---

## Key Sources

- [Claude Code settings](https://code.claude.com/docs/en/settings)
- [Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Hooks reference](https://code.claude.com/docs/en/hooks)
- [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices)

**Full sources:** [[research/outputs/OUTPUT-20260124-202744-claude-codes-capabilities-for-dynamic/sources]]
