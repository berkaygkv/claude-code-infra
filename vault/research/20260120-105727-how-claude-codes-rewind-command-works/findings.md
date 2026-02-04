---
type: research-output
id: OUTPUT-20260120-105727-how-claude-codes-rewind-command-works
target: '[[research/targets/TARGET-20260120-102231-the-best-practices-for-using-claude]]'
created: 2026-01-20
researcher: claude-deep-research
tags:
  - research
---

# Research Output: how Claude Code's /rewind command works, specifically:

1. Does /rewind have an

**Target:** [[research/targets/TARGET-20260120-102231-the-best-practices-for-using-claude]]

**Question:** Research how Claude Code's /rewind command works, specifically:

1. Does /rewind have an option to restore code changes?
2. What are the exact options presented when using /rewind?
3. Under what condi...

---

## Findings

Excellent. Now I have the complete picture. Let me compile the findings:

## Research Findings: Claude Code's `/rewind` Command

Based on the official Claude Code documentation, here's what I found about the `/rewind` command:

### 1. Does /rewind have an option to restore code changes?

**Yes, absolutely.** The `/rewind` command offers three distinct restoration options:

- **Conversation only**: Rewind to a user message while keeping code changes
- **Code only**: Revert file changes while keeping the conversation  
- **Both code and conversation**: Restore both to a prior point in the session

### 2. What are the exact options presented when using /rewind?

The documentation shows these three options are presented in the rewind menu. You can access the rewind menu by pressing `Esc` twice (`Esc` + `Esc`) or using the `/rewind` command explicitly.

### 3. Under what conditions does the "restore code" option appear vs not appear?

**This is the critical issue:** The documentation does not explicitly state conditions under which the "restore code" option would be unavailable. However, based on the tracking mechanism documented below, the restore code option would only be available if code changes have actually been made during the session.

### 4. How does Claude Code track file changes for restoration?

Claude Code has **automatic checkpointing** with these specific mechanics:

- **Automatic tracking**: Claude Code tracks all changes made by its **file editing tools**
- **When checkpoints are created**: Every user prompt creates a new checkpoint
- **Persistence**: Checkpoints persist across sessions, so you can access them in resumed conversations
- **Cleanup**: Automatically cleaned up along with sessions after 30 days (configurable)

**Importantly, there are limitations on what gets tracked:**

- **Bash command changes are NOT tracked** - If Claude Code runs bash commands like `rm`, `mv`, or `cp`, these file modifications cannot be undone through rewind
- **External changes are NOT tracked** - Manual changes made outside Claude Code aren't captured (unless they happen to modify the same files)

### Why the user only sees "restore conversation"

If the user is only seeing "restore conversation" and not a "restore code" option, the likely reasons are:

1. **No file editing tools were used** - Only bash commands were executed, which aren't tracked
2. **No changes were made in the current session** - Checkpoints only track changes made through Claude's file editing tools during the active session
3. **All changes have been reverted** - If code was modified but has since been restored, there may be nothing to revert to

### Source

- **Official Documentation**: https://code.claude.com/docs/en/checkpointing.md
- **Slash Commands Reference**: https://code.claude.com/docs/en/slash-commands.md

The documentation is clear that the feature exists and supports restoring code, but the implementation is limited to direct file edits made by Claude's editor, not bash operations.

---

## Key Sources

*No high-relevance sources identified*

**Full sources:** [[research/outputs/OUTPUT-20260120-105727-how-claude-codes-rewind-command-works/sources]]
