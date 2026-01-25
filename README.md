# kh - Claude Code Session Framework

A cookiecutter template for structured Claude Code sessions with context handoffs, decision tracking, and automated transcript export.

## Quick Start

```bash
# Generate a new project
uvx cookiecutter gh:berkaygkv/claude-code-infra

# Answer the prompts
# - project_name: My Project
# - project_description: What this project does
# - author: Your name

# Enter the project
cd my-project
git init && git add . && git commit -m "Initial commit"

# Start Claude Code
claude
```

Then use `/begin` to start a session and `/wrap` to end it.

## Commands

| Command | Description |
|---------|-------------|
| `/begin` | Start session, load previous context (quick fix mode) |
| `/begin brainstorm` | Start in planning/alignment mode |
| `/begin build` | Start in execution mode with active plan |
| `/wrap` | End session, create handoff note, update vault |

## Project Structure

```
my-project/
├── .claude/
│   ├── commands/       # /begin and /wrap skills
│   ├── hooks/          # Auto-export transcripts
│   └── settings.json   # Permissions and hooks config
├── protocols/          # Mode-specific instructions
├── scripts/            # Shell utilities
├── vault/              # Obsidian-compatible knowledge base
│   ├── Sessions/       # Session handoff notes
│   ├── plans/          # Implementation plans
│   ├── research/       # Research outputs
│   ├── locked.md       # Committed decisions
│   ├── runbook.md      # Task tracking
│   └── overview.md     # Project dashboard
├── scratch.md          # Per-session working memory
└── CLAUDE.md           # Project instructions for Claude
```

## How It Works

1. **Session Start (`/begin`)**: Loads context from the previous session handoff note, displays current state from runbook
2. **During Session**: Use `scratch.md` to capture decisions, tasks, and notes
3. **Session End (`/wrap`)**: Creates handoff note, updates vault documents, prepares for next session
4. **Automatic Export**: `SessionEnd` hook exports conversation transcript to `vault/Sessions/transcripts/`

## Vault Integration

The `vault/` directory is Obsidian-compatible. You can open it directly in Obsidian for:
- Graph view of connected notes
- Quick search across sessions
- Frontmatter-based queries

## Requirements

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code)
- [uv](https://docs.astral.sh/uv/) (for running Python hooks)
- Git

## License

MIT
