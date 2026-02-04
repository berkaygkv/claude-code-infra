---
type: research-output
id: OUTPUT-20260120-005512-the-claude-code-rewind-command-i-need
target-id: TARGET-20260119-220941
status: draft
created: 2026-01-20
researcher: claude-deep-research
confidence: medium
---

# Research Output: the Claude Code /rewind command. I need to understand:

1. What /rewind does ex

**Target:** [[research/targets/TARGET-20260119-220941-the-key-features-of-uv-package-manager]]

**Question:** Research the Claude Code /rewind command. I need to understand:

1. What /rewind does exactly - how it works, what it reverts
2. How it relates to conversation state and file changes
3. Any limitation...

---

## Findings

Perfect! Now I have comprehensive information. Let me compile a detailed research summary for you based on the official Claude Code documentation.

## Research Summary: Claude Code /rewind Command

Based on official Claude Code documentation, here's a complete breakdown of the `/rewind` command:

### 1. What /rewind Does Exactly

The `/rewind` command provides a **checkpoint-based recovery system** that lets you restore your session to a previous point. You access it in two ways:

- **Keyboard shortcut**: Press `Esc` twice (`Esc` + `Esc`)
- **Command**: Type `/rewind` in the session

When you open the rewind menu, you can choose between three restoration modes:

1. **Conversation only** - Revert Claude's responses while keeping code changes
2. **Code only** - Revert file changes while keeping the conversation
3. **Both** - Restore the entire session (conversation + code) to a prior state

### 2. How It Works (Checkpointing Mechanism)

**Automatic Checkpoint Creation:**
- Every user prompt creates a new checkpoint automatically
- Checkpoints capture the state of your code **before each edit**
- Checkpoints are created by Claude's file editing tools (Write tool, Edit tool, etc.)
- Checkpoints persist across sessions, so you can rewind even in resumed conversations
- Checkpoints are automatically cleaned up after **30 days** (configurable)

**Session Persistence:**
This is critical for your session state design—checkpoints survive session boundaries. If you resume a conversation, all previous checkpoints remain available for rewinding.

### 3. Key Limitations and Gotchas

This is important for your system design:

**What /rewind CANNOT track:**
- **Bash command file changes**: If Claude runs `rm file.txt`, `mv old.txt new.txt`, or `cp source.txt dest.txt`, these modifications cannot be undone through rewind
- **External file modifications**: Changes made manually outside Claude Code or by other concurrent sessions are not captured (unless they modify the same files as the current session)
- **Not a version control replacement**: Checkpoints are session-local undo, not permanent history

### 4. Git Interaction

The documentation does NOT describe any direct interaction between `/rewind` and git. Key points:

- `/rewind` operates independently of git
- It reverts only file content, not git state (branches, commits, staging area)
- It complements but does NOT replace git for permanent history
- For your system design: If you need to integrate rewind with git workflows, you'd need custom logic on top

### 5. Best Practices and Workflow Patterns

**Common Use Cases:**
1. **Exploring alternatives** - Try different implementation approaches, rewind if unsatisfied
2. **Recovering from mistakes** - Quickly undo changes that broke functionality or introduced bugs
3. **Iterating on features** - Experiment with variations knowing you can revert to working states

**For Your System Design:**

1. **Checkpoint Granularity** - Each prompt creates one checkpoint, so longer prompts = larger state deltas. Design prompts accordingly.

2. **Session Boundaries** - Checkpoints persist across sessions. Your session handoff system can reference them: users can resume an old session and still rewind to its checkpoints.

3. **Combined with Git** - Recommended practice:
   - Use `/rewind` for rapid iteration and experimentation within a session
   - Use git commits for permanent, shareable changes
   - Use hooks to capture session decisions to Obsidian (your `/wrap` command does this)

4. **Not for Permanent Recovery** - Don't rely on checkpoints for long-term undo. They auto-delete after 30 days, and they're local to sessions.

5. **Parallel Sessions** - If running parallel sessions (via git worktrees), each has its own checkpoint history. Rewinding in one session doesn't affect others.

### 6. Relevant Configuration

No configuration options are documented for `/rewind` behavior itself. However, related settings exist:

- Checkpoint cleanup: Runs after **30 days** (appears to be hardcoded/configurable but details not in public docs)
- Session lifetime: Checkpoints tied to session lifecycle

---

## Design Implications for Your Session State System

Based on this research, here's how it should inform your design:

1. **Checkpoint Model**: Rewind uses a **linear, prompt-indexed checkpoint system**—not branching. This is important if you're designing a more sophisticated state system.

2. **Persistence Layer**: Checkpoints are persisted across session boundaries but lost after 30 days. Your `/begin` and `/wrap` workflow should explicitly capture important state to Obsidian if it needs to survive beyond the 30-day window.

3. **Integration Point**: Your custom `/wrap` command could snapshot session checkpoints to your vault at session end, extending their lifetime beyond 30 days.

4. **Limitations to Document**: If you're building workflows that depend on rewind, document that bash-command-modified files cannot be recovered.

---

**Documentation Sources:**

- [Checkpointing - https://code.claude.com/docs/en/checkpointing.md](https://code.claude.com/docs/en/checkpointing.md)
- [Slash Commands - https://code.claude.com/docs/en/slash-commands.md](https://code.claude.com/docs/en/slash-commands.md)
- [Interactive Mode - https://code.claude.com/docs/en/interactive-mode.md](https://code.claude.com/docs/en/interactive-mode.md)

---

## Key Sources

- [Checkpointing - https://code.claude.com/docs/en/checkpointing.md](https://code.claude.com/docs/en/checkpointing.md)
- [Slash Commands - https://code.claude.com/docs/en/slash-commands.md](https://code.claude.com/docs/en/slash-commands.md)
- [Interactive Mode - https://code.claude.com/docs/en/interactive-mode.md](https://code.claude.com/docs/en/interactive-mode.md)

**Full sources:** [[research/outputs/OUTPUT-20260120-005512-the-claude-code-rewind-command-i-need/sources]]

---

## Outcome

**Decision:** *[To be determined]*

**Confidence:** Medium

**Rationale:** *[To be filled]*

**Next Steps:**
- Review findings
- *[Add next steps]*
