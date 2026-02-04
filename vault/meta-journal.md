---
type: meta-journal
project: kh
created: '2026-01-20'
updated: '2026-01-25'
tags:
  - meta
  - insights
---
# Meta-Journal

> Learnings about how we work together—what works, what doesn't, and what might. A diary for meta-level improvements.

---

## Entries

<!-- New entries are prepended below this line -->

### 2026-01-25 — [[sessions/session-19|session-19: cookiecutter-template-refactor]]

We needed to maintain both a development workspace (where `/begin` and `/wrap` work) and a distributable cookiecutter template. After merging the template to main, we lost the ability to develop—the `.claude/` directory was now nested inside `{{cookiecutter.project_slug}}/`.

The solution was trivially simple: **use git worktrees**—one for development (main), one for the template (template branch). Two directories, two purposes.

Instead, I proposed increasingly convoluted alternatives:
1. "Just work inside the template directory" (doesn't work—cookiecutter syntax breaks things)
2. "Abandon cookiecutter, use a setup script" (throwing away working code)
3. "Template-first development with regeneration" (unnecessary friction)
4. Multiple variations of the above

Each time the user pushed back, I proposed another complex solution instead of asking: "What's the simplest way to have two separate workspaces?"

**Insight:** When the user says "this is simple," stop and restate the problem in plain terms before proposing solutions. The failure pattern: I kept trying to make ONE location serve two purposes, when the obvious answer was TWO locations. Complexity bias—assuming a "real" solution must be clever. The user had to explicitly say "why can't we just use worktrees" before I stopped overengineering.

**Root cause:** Solution-first thinking. I jumped to "how do we solve this" before clearly articulating "what exactly is the problem." A 30-second problem statement ("we need a dev space AND a template space") would have led directly to "use two directories."

---

### 2026-01-25 — [[sessions/session-19|session-19: path-architecture-brainstorm]]

We were brainstorming a new path architecture to eliminate runtime config reads. I proposed using symlinks to create relative paths (`kh/notes/` → user's vault). Before committing to this approach, the user asked me to search previous discussions about symlinks.

The search returned hits across sessions 2, 4, and 5. Reading those handoffs revealed: we had already tried symlinks (session 2), discovered MCP search breaks through symlinks (session 4), and migrated to bare repo architecture as the deliberate solution (session 5). This was 15+ sessions ago.

**Insight:** The persistent session history prevented re-implementing a known-failed approach. The handoff notes—with their structured Decisions, Memory, and Context sections—made the rationale immediately clear. Without searchable session history, we would have wasted effort rediscovering the symlink limitation. This is the system working as designed: institutional memory that survives across sessions and prevents repeated mistakes.

---

### 2026-01-20 — [[sessions/session-8|session-8: rollback-refinement]]

We built a `/rollback` command in session 7 to handle mid-session file reversals after discovering Claude Code's `/rewind` is broken. The specific concern was that MCP tool writes (Obsidian vault changes) would never be tracked by `/rewind` even when fixed. So we invested effort building tooling to parse conversation history and reverse file changes.

Then we realized: the vault stores persistent artifacts—locked decisions, session handoffs, research outputs. These are written once, when we're confident. We shouldn't be making speculative writes that need rollback in the first place.

**Insight:** Procedural change before tooling change. We asked "how do we recover from MCP writes?" instead of "why would we need to recover from MCP writes?" This is a pattern: reaching for technical solutions before questioning whether the workflow itself is flawed. The fix was trivial—use ephemeral scratch files for working memory, only write to vault when ready—but we built a command first.

**Root cause:** Problem-solving momentum. Once we identified "/rewind doesn't track MCP writes" as a gap, we rushed to fill it technically rather than stepping back to ask if it was a gap that needed filling.

---
