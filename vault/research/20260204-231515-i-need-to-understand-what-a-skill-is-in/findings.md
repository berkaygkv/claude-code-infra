---
type: research
topic: I need to understand what a "skill" is in Claude Code. Specifically:

1. What is
status: open
created: 2026-02-04
completed: null
session: null
confidence: medium
led_to_decision: null
tags:
  - research
---

# Research: I need to understand what a "skill" is in Claude Code. Specifically:

1. What is

**Question:** I need to understand what a "skill" is in Claude Code. Specifically:

1. What is the correct file structure for a skill?
2. What is SKILL.md and its required YAML frontmatter?
3. What's the difference...

---

## Findings

Perfect! Now I have everything I need to provide a comprehensive answer. Let me create a complete guide:

---

## What is a Skill in Claude Code?

A **skill** is a reusable instruction set that extends Claude's capabilities. Skills are discovered and loaded automatically by Claude when relevant, or you can invoke them manually with `/skill-name`. They're the modern replacement for slash commands in `.claude/commands/` (though existing commands still work).

**Key distinction:** Skills are **more than slash commands**. While both create `/commands`, skills add optional features like supporting files, frontmatter-based invocation control, and automatic loading based on relevance.

---

## 1. File Structure for Skills

Skills live in **three possible locations** (priority order):

| Location   | Path                                     | Scope              |
|------------|------------------------------------------|-------------------|
| Enterprise | Managed by org                           | All users         |
| Personal   | `~/.claude/skills/<skill-name>/SKILL.md` | All your projects |
| Project    | `.claude/skills/<skill-name>/SKILL.md`   | This project only |

Your project uses `.claude/commands/` which still works but is considered the legacy approach.

**Standard directory structure:**

```
my-skill/
├── SKILL.md                    # Required: core instructions + YAML frontmatter
├── scripts/                    # Optional: executable code (Python, Bash, etc.)
│   ├── helper.py
│   └── validate.sh
├── references/                 # Optional: documentation loaded as needed
│   ├── api-reference.md
│   └── examples.md
└── assets/                     # Optional: templates, icons, fonts for output
    ├── template.html
    └── logo.png
```

Each directory serves a distinct purpose in the **progressive disclosure** pattern (explained below).

---

## 2. SKILL.md and YAML Frontmatter

Every skill **must** have a `SKILL.md` file with two parts:

**Part 1: YAML Frontmatter (between `---` markers)**

Only two fields are required:

```yaml
---
name: my-skill
description: What the skill does and when to use it
---
```

| Field | Required | Purpose |
|-------|----------|---------|
| `name` | No* | Skill name for `/` commands (lowercase, hyphens, max 64 chars). If omitted, uses directory name. |
| `description` | Recommended | **The primary triggering mechanism.** Claude reads this to decide when to load the skill. Include BOTH what it does AND specific triggers. |

**Part 2: Markdown Body**

Instructions Claude follows when the skill is invoked:

```markdown
When explaining code, always include:
1. Start with an analogy
2. Draw a diagram
3. Walk through step-by-step
4. Highlight a gotcha
```

**Critical design principle:** Keep the body under **500 lines**. Move detailed reference material to separate files in `references/` to avoid bloating context on every activation.

### Example: Your `/excalidraw` Skill

Looking at your `/excalidraw` command (which is actually a skill in legacy format):

```yaml
---
name: excalidraw
description: Generate diagrams as .excalidraw files for visual sense-making. Use when user asks to visualize, diagram, map out, sketch, or draw anything. Supports flowcharts, system diagrams, mind maps, sequences, and timelines.
---
```

This is perfect because:
- **Description** lists all the trigger phrases ("visualize", "diagram", "map out", "sketch")
- **Body** contains focused instructions with references to supporting files (`excalidraw/core-spec.md`, etc.)

---

## 3. Directory Purposes: scripts/, references/, assets/

### **scripts/**
Executable code Claude can run. Files here are **executed, not loaded into context**:
- Python scripts for complex logic
- Bash scripts for system integration
- Any language the environment supports

```yaml
# In SKILL.md:
allowed-tools: Bash(python *)
```

Example from your codebase explorer skill:
```bash
python ~/.claude/skills/codebase-visualizer/scripts/visualize.py .
```

### **references/**
Documentation and detailed information Claude loads **only when needed**:
- API specifications
- Detailed guides
- Code examples
- Reference material

These files load into context **after the skill is triggered**, not initially. This saves tokens.

From your `/excalidraw`:
```markdown
## Reference Files
- `excalidraw/core-spec.md` — Always read before generating
- `excalidraw/arrows.md` — When diagram has connections
- `excalidraw/diagram-types.md` — For type-specific templates
```

Your skill structure shows this pattern in action:
```
.claude/commands/
├── excalidraw.md              # Main skill (references files below)
└── excalidraw/                # Reference directory
    ├── core-spec.md           # Loaded on demand
    ├── arrows.md              # Loaded on demand
    ├── colors.md              # Loaded on demand
    └── diagram-types.md       # Loaded on demand
```

### **assets/**
Non-executable files for output generation:
- HTML templates
- CSS stylesheets
- Icon files
- Font files
- Any binary assets

These are referenced by scripts but not directly executed by Claude.

---

## 4. Progressive Disclosure Pattern

Skills use a **three-level disclosure system** for efficiency:

### **Level 1: Metadata (Always Loaded)**
- YAML frontmatter (`name`, `description`)
- Token cost: ~100 tokens
- Purpose: Claude scans available skills to identify relevant ones

Claude sees all skill descriptions initially so it knows what's available.

### **Level 2: Full Instructions (Loaded When Triggered)**
- `SKILL.md` body content
- Token cost: <5k tokens
- Loaded when Claude determines the skill applies

When you ask "visualize this code", Claude loads the full `/excalidraw` instructions.

### **Level 3: Supporting Resources (Loaded As Needed)**
- `scripts/` — executed on-demand
- `references/` — loaded when skill references them
- `assets/` — used by scripts

This prevents loading a 100-line API reference until Claude actually needs it.

**Why this matters:**
- With 50 skills, only descriptions (~100 tokens each) are loaded initially
- Full skill content only loads when invoked
- Reference files stay out of context until needed
- Scripts run on-demand without loading their full code

---

## 5. Skills vs. Slash Commands in `.claude/commands/`

Both create `/commands`, but **skills are the recommended approach**:

| Feature | Slash Command | Skill |
|---------|---------------|-------|
| Location | `.claude/commands/` | `.claude/skills/` |
| Main file | `command.md` | `SKILL.md` |
| Supporting files | Not organized | `scripts/`, `references/`, `assets/` |
| Frontmatter | Simple (if any) | Full YAML config |
| Auto-invocation | No (only manual) | Yes (if description matches) |
| Control invocation | No | `disable-model-invocation` |
| Hide from menu | No | `user-invocable: false` |

**Your project's status:**

You're using `.claude/commands/` (legacy):
- `/begin` → `.claude/commands/begin.md`
- `/wrap` → `.claude/commands/wrap.md`
- `/excalidraw` → `.claude/commands/excalidraw.md`

These still work perfectly. The official docs note: "Files in `.claude/commands/` still work and support the same [frontmatter](#frontmatter-reference). Skills are recommended since they support additional features like supporting files."

**Migration path** (if desired):
1. Create `.claude/skills/begin/SKILL.md` with your content
2. Add frontmatter: `name: begin`, `description: ...`
3. Keep `.claude/commands/begin.md` as-is (existing commands continue working)
4. Skill takes precedence if both exist

---

## Advanced Frontmatter Fields

Your basic commands don't use these, but here are options available:

```yaml
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true    # Only user can invoke (no auto-trigger)
user-invocable: false              # Only Claude can invoke (not in / menu)
allowed-tools: Bash(./deploy *)   # Tools Claude can use without asking
argument-hint: "[environment]"    # Help text for arguments
context: fork                      # Run in isolated subagent
agent: Explore                     # Which subagent type
model: claude-opus-4-5             # Override model for this skill
---
```

**Example: Your `/begin` command** could modernize:

```yaml
---
name: begin
description: Session begin command. Loads context from vault/state.md + last session handoff. Activate specified mode (quick-fix, brainstorm, or build).
disable-model-invocation: true     # Only user should trigger this
argument-hint: "[mode]"
---
```

---

## Practical Examples from Your Project

### `/excalidraw` (Skill-like, Auto-triggered)
```yaml
---
name: excalidraw
description: Generate diagrams... Use when user asks to visualize, diagram, map out, sketch...
---
```
✓ Claude can auto-detect when to load this
✓ Description covers all trigger phrases
✓ References support files instead of bloating SKILL.md

### `/wrap` (Command, Manual Only)
Would benefit from modernization:
```yaml
---
name: wrap
description: Session wrap-up command. Processes scratch.md, creates decision files, session handoff, updates vault/state.md.
disable-model-invocation: true     # Prevent accidental triggering
---
```

---

## Summary Table

| Question | Answer |
|----------|--------|
| **What is a skill?** | Reusable instruction set with optional supporting files, loaded automatically when relevant or manually via `/skill-name` |
| **File structure?** | `SKILL.md` (required) + optional `scripts/`, `references/`, `assets/` directories |
| **SKILL.md required fields?** | Only `name` (optional) and `description` (recommended) in frontmatter |
| **What's `description` for?** | Primary trigger mechanism — Claude reads it to decide when to auto-load the skill |
| **scripts/ vs references/ vs assets/?** | Scripts execute; references load on-demand into context; assets are output files |
| **Progressive disclosure?** | 3 levels: metadata (~100 tokens always), full instructions (<5k when triggered), resources (on-demand) |
| **Skills vs .claude/commands/?** | Both work, skills are recommended; skills support additional features like auto-invocation and file organization |

---

## Your Next Steps

1. **For immediate use:** Your `.claude/commands/` files work fine as-is. No action needed.

2. **For modernization:** Create `.claude/skills/` versions of your custom commands to enable auto-invocation and better file organization:
   ```bash
   mkdir -p ~/.claude/skills/begin
   mv .claude/commands/begin.md .claude/skills/begin/SKILL.md
   # Update frontmatter with description for auto-trigger
   ```

3. **For reference:** [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills.md)

Sources:
- [Extend Claude with skills - Claude Code Docs](https://code.claude.com/docs/en/skills.md)
- [The Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf?hsLang=en)
- [Anthropic Engineering: Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

---

## Key Sources

- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills.md)
- [The Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf?hsLang=en)
- [Anthropic Engineering: Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

**Full sources:** [[research/20260204-231515-i-need-to-understand-what-a-skill-is-in/sources]]
