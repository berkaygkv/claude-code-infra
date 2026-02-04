# kh - Claude Code Session Framework

A cookiecutter template for structured Claude Code sessions with context handoffs, decision tracking, and automated transcript export.

## Quick Start

```bash
# Generate a new project
uvx cookiecutter gh:berkaygkv/claude-code-infra --checkout template

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
| `/excalidraw` | Generate visual diagrams |

## Project Structure

```
my-project/
├── .claude/
│   ├── commands/       # /begin, /wrap, /meta commands
│   ├── hooks/          # Auto-export transcripts, capture research
│   ├── skills/         # Excalidraw diagram generation
│   └── settings.json   # Permissions and hooks config
├── protocols/          # Mode-specific instructions
├── scripts/            # Shell utilities
├── vault/              # Obsidian-compatible knowledge base
│   ├── state.md        # Current phase, focus, tasks
│   ├── dashboard.md    # Dataview queries
│   ├── sessions/       # Session handoff notes
│   ├── decisions/      # LOCKED decisions (one per file)
│   ├── plans/          # Implementation plans
│   ├── research/       # Research outputs with TARGET system
│   ├── canvas/         # Excalidraw diagrams
│   └── templates/      # Obsidian templates
├── scratch.md          # Per-session working memory
└── CLAUDE.md           # Project instructions for Claude
```

## How It Works

1. **Session Start (`/begin`)**: Loads `state.md` + last session handoff for cold start context
2. **During Session**: Use `scratch.md` to capture decisions, tasks, and notes
3. **Session End (`/wrap`)**: Creates session handoff, decision files, updates state, prepares for next session
4. **Automatic Export**: Hooks export transcripts and capture research outputs

## Vault Integration

The `vault/` directory is Obsidian-compatible. Open it in Obsidian for:
- Graph view of connected notes
- Dataview queries on dashboard
- Quick search across sessions
- Excalidraw diagram editing

**Recommended plugins:** Dataview, Excalidraw (configured in `.obsidian/`)

## Requirements

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code)
- [uv](https://docs.astral.sh/uv/) (for running Python hooks)
- Git
- [Obsidian](https://obsidian.md/) (optional, for vault browsing)

## License

MIT
