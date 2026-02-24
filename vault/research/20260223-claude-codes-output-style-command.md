---
type: research
date: 2026-02-23
topic: "Claude Code's `/output-style` command thoroughly. I need to understand:

1. Wha"
---

# Claude Code's `/output-style` command thoroughly. I need to understand:

1. Wha

**Question:** Research Claude Code's `/output-style` command thoroughly. I need to understand:

1. What does `/output-style` do exactly? How does it work?
2. What configuration options/parameters does it accept?
3....

---

## Findings

Perfect. Now I have comprehensive information. Let me compile a thorough research file for you.

Based on my thorough investigation of Claude Code's `/output-style` command and related documentation, here's the complete technical picture:

## Complete Technical Analysis: `/output-style` Command

### 1. What `/output-style` Does (Exactly)

`/output-style` modifies Claude Code's **system prompt** to change how Claude responds to you. It's not just a formatting preference — it fundamentally rewires Claude's instructions.

**Key mechanism:**
- Output styles **replace** parts of the default software-engineering-focused system prompt
- They inject custom instructions at the **end** of the modified system prompt
- All output styles **remove** efficiency instructions (like "respond concisely")
- This causes Claude to adopt different communication patterns, priorities, and behaviors

### 2. Configuration Options & Parameters

You have three ways to change output styles:

```bash
# Interactive menu
/output-style

# Direct selection
/output-style explanatory
/output-style learning
/output-style default

# Set in settings file
# .claude/settings.json or .claude/settings.local.json
{
  "outputStyle": "Explanatory"
}
```

The command accepts three **built-in presets** (case-insensitive):
- `default` — Software engineering optimized (existing system prompt)
- `explanatory` — Includes educational "Insights" between code tasks
- `learning` — Collaborative mode with `TODO(human)` markers for you to implement

### 3. Storage & Persistence

Output style preference is stored **project-scoped** at:

**Local level (most specific, used first):**
```
.claude/settings.local.json
```

**Project level (gitignored by default):**
```
.claude/settings.json
```

**User level (your machine, all projects):**
```
~/.claude/settings.json
```

**Precedence** (highest to lowest):
1. Managed settings (enterprise/IT deployed)
2. CLI arguments (`--output-style` if it existed as a flag)
3. Local project settings (`.claude/settings.local.json`)
4. Shared project settings (`.claude/settings.json`)
5. User settings (`~/.claude/settings.json`)

The setting is stored in the `outputStyle` field in these JSON files:
```json
{
  "outputStyle": "Explanatory"
}
```

### 4. Built-in Style Presets

**Default**
- The existing Claude Code system prompt
- Designed for efficient software engineering
- Includes instructions for: code verification, testing, git workflows, file management
- Emphasis on conciseness and efficiency

**Explanatory**
- Removes efficiency instructions
- Adds custom instruction: provide "Insights" between helping you code
- Explains implementation choices and codebase patterns
- Educational tone while maintaining coding capability
- Still includes coding instructions (unless `keep-coding-instructions: false` in frontmatter)

**Learning**
- Removes efficiency instructions
- Adds: "Insights" + asks you to implement strategic code pieces
- Inserts `TODO(human)` markers for your manual implementation
- Collaborative, learn-by-doing approach
- Still includes coding instructions by default

### 5. Custom Output Styles (DIY)

Yes, you can define custom output styles as Markdown files with YAML frontmatter.

**File structure:**
```markdown
---
name: My Custom Style
description: Brief description for the UI menu
keep-coding-instructions: false
---

# Custom Style Instructions

You are an interactive CLI tool that helps users with [your domain].

## Specific Behaviors

[Define how you should behave...]
```

**Save locations:**
- **User level** (all projects): `~/.claude/output-styles/my-style.md`
- **Project level** (this repo only): `.claude/output-styles/my-style.md`

**Frontmatter options:**

| Field | Purpose | Default |
|-------|---------|---------|
| `name` | Display name in `/output-style` menu | Inherits from filename (without `.md`) |
| `description` | Shown in UI | None |
| `keep-coding-instructions` | Whether to preserve Claude Code's coding-focused instructions | `false` |

**Example custom style for documentation writing:**
```markdown
---
name: Documentation Writer
description: Optimized for writing clear, comprehensive technical docs
keep-coding-instructions: false
---

# Documentation Writing Mode

You are a technical documentation specialist. Your role is to:

1. Write clear, structured documentation with proper hierarchy
2. Include examples and edge cases
3. Add "See Also" sections linking related topics
4. Verify all code examples actually run
5. Flag outdated or ambiguous sections

Use this tone: professional, direct, no marketing language.
```

Then invoke with: `/output-style documentation-writer`

### 6. System Prompt Interaction (How It Works)

**The Layer Cake (from bottom to top):**

1. **Base**: Claude Code's default system prompt
   - Software engineering instructions
   - Git workflow guidance
   - Code quality checks
   - Efficiency requirements

2. **Output Style Layer** (this is where `/output-style` operates):
   - **REMOVES**: Efficiency instructions (respond concisely, etc.)
   - **REMOVES** (if custom style): All coding instructions (unless `keep-coding-instructions: true`)
   - **ADDS**: Custom instructions from the style file

3. **CLAUDE.md Layer** (your operational protocol):
   - Added as a **user message** (not system prompt)
   - Comes *after* the system prompt in Claude's context
   - Can override system prompt guidance through conversation context
   - Your CLAUDE.md is **NOT** replaced by output styles

4. **`--append-system-prompt` / `--system-prompt` flags**:
   - `--append-system-prompt`: Tacked to the *end* of the modified system prompt (after output style instructions)
   - `--system-prompt`: **Replaces** the entire system prompt entirely (ignores output style)

**Critical distinction:**
- Output styles **modify** the system prompt
- CLAUDE.md **doesn't touch** the system prompt (it's a user message)
- `--append-system-prompt` **adds to** the system prompt
- `--system-prompt` **replaces** the system prompt entirely

### 7. Examples of Good Output Style Configurations

**For Teaching/Onboarding:**
```markdown
---
name: Teaching Mode
description: Explains concepts and architecture while coding
---

# Teaching Mode

When helping with code:
1. Explain the "why" before the "what"
2. Point out design patterns you're using
3. Suggest learning resources for unfamiliar concepts
4. Ask questions to check understanding instead of assuming
5. Include comments explaining non-obvious code sections
```

**For Code Review:**
```markdown
---
name: Code Reviewer
description: Critical review focused on quality and best practices
keep-coding-instructions: true
---

# Code Review Mode

You are a senior engineer reviewing code. Focus on:
- Security vulnerabilities and data handling
- Performance implications
- Maintainability and readability
- Adherence to team conventions
- Missing error handling

Always suggest specific improvements, not just issues.
```

**For Research/Writing:**
```markdown
---
name: Research Assistant
description: Deep investigation with citations and source tracking
---

# Research Assistant

Your role is to:
1. Search multiple sources before concluding
2. Track all citations explicitly
3. Highlight areas of uncertainty or disagreement in sources
4. Organize findings with clear hierarchy
5. Separate facts from interpretations
```

### 8. Interaction with CLAUDE.md Instructions

**Key: They exist in separate layers and don't conflict.**

- **Output Style** = System prompt modification (Claude's behavior blueprint)
- **CLAUDE.md** = User message (conversation context)

**In practice:**

Your CLAUDE.md (from this project) specifies operational protocols, voice guidelines, and memory architecture. When you use `/output-style learning`:

1. Claude's system prompt changes to include learning-mode instructions
2. Your CLAUDE.md is still loaded as a user message
3. Claude tries to honor **both** sets of instructions
4. When they conflict (rare), the system prompt typically wins, but your CLAUDE.md provides strong contextual weight

**Example:**
- CLAUDE.md says: "Voice: Direct over diplomatic"
- Output style "Explanatory" says: "Provide educational insights"
- **Result:** Claude gives you direct explanations with educational context (not verbose tutoring)

**If you want output style to completely override CLAUDE.md**, use `--system-prompt` instead (which replaces the entire prompt), but you'd lose Claude Code's core capabilities.

### 9. What DOESN'T Happen

Important clarifications:

- `/output-style` does **NOT** change your file permissions or tool access
- It does **NOT** modify `.claude/settings.json` for other users (only your local settings or shared project settings if you commit)
- It does **NOT** persist across machines (stored locally)
- It does **NOT** affect MCP servers or skills
- It does **NOT** change the model you're using (use `--model` for that)

---

## Summary: Your Action Checklist

To use `/output-style` effectively in your project:

1. **Test built-in styles:**
   ```bash
   /output-style explanatory
   /output-style learning
   /output-style default
   ```

2. **Create custom styles for your workflow:**
   - Save to `.claude/output-styles/my-style.md` (project-shared)
   - Or `~/.claude/output-styles/my-style.md` (personal across all projects)

3. **For your "Symbiotic Partner" protocol:**
   - Output styles complement CLAUDE.md well
   - Consider a "Project Manager" style that reinforces your operational model
   - Or create a "Code Ownership" style for when you're in build mode

4. **Remember the precedence:**
   - CLI flags override everything
   - Local settings beat project settings beat user settings
   - `/output-style` is just setting the `outputStyle` field in settings

5. **When to use each system prompt layer:**
   - Use **output styles** for broad behavioral shifts (teaching vs. production, coding vs. writing)
   - Use **CLAUDE.md** for detailed project-specific protocols and memory architecture
   - Use **`--append-system-prompt`** for one-off instructions in headless/API mode
   - Use **`--system-prompt`** only when you need complete control (rare)

---

## Sources

*No sources identified*
