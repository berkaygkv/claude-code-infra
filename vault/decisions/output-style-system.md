---
type: decision
status: locked
date: 2026-02-23
session: "[[sessions/session-47]]"
---

# Output Style System

## Decision

Use Claude Code's native `/output-style` feature to apply mode-specific formatting discipline.

## Design

- **Brainstorm mode** → `kh-brainstorm` style (`keep-coding-instructions: false`). Reasoning-focused: compression, hierarchy, zero filler. No code written in brainstorm, so coding instructions are dead weight.
- **Build mode** → `default` style. Claude Code's built-in coding-optimized output. No custom constraints.
- **Direct execution** → no style override. Whatever was last active.

## Layer Split

- **CLAUDE.md** owns voice, stance, and identity (tone, opinions, challenge patterns)
- **Output style** owns structural formatting (compression rules, hierarchy, response patterns, anti-patterns)

No overlap. They complement, not compete.

## Activation

Manual toggle by user at session start:
- `/output-style kh-brainstorm` for brainstorm
- `/output-style default` for build

Reminder included in `/begin` mode-specific prompts and protocol files.

## File Location

`.claude/output-styles/kh-brainstorm.md`
