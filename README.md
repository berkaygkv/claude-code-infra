# kh - Claude Code Session Framework

A cookiecutter template for structured Claude Code sessions with context handoffs, decision tracking, and automated transcript export.

## Quick Start

### Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code)
- [uv](https://docs.astral.sh/uv/) (for running Python hooks)
- Git
- [Obsidian](https://obsidian.md/) (optional, for vault browsing)

### Generate a project

```bash
uvx cookiecutter gh:berkaygkv/claude-code-infra
```

Answer the prompts:
- **project_name**: Human-readable name (e.g., "My Project")
- **project_description**: What this project does
- **author**: Your name

### Bootstrap

```bash
cd my-project
git init && git add . && git commit -m "Initial commit"
```

Open Obsidian → "Open folder as vault" → select the `my-project/` directory inside your project. This is your session vault — Dataview and Excalidraw plugins are pre-configured.

### Start working

```bash
claude
```

Then use `/begin` to start a session and `/wrap` to end it.

## Commands

| Command | Description |
|---------|-------------|
| `/begin` | Start session, load previous context |
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
│   ├── skills/         # Excalidraw diagrams, upgrade tool
│   └── settings.json   # Permissions and hooks config
├── .mcp.json           # Obsidian MCP server config
├── protocols/          # Mode-specific instructions
├── scripts/            # Shell utilities
├── my-project/         # Obsidian-compatible vault (named after project)
│   ├── state.md        # Current phase, focus, tasks
│   ├── dashboard.md    # Dataview queries
│   ├── sessions/       # Session handoff notes
│   ├── decisions/      # LOCKED decisions (one per file)
│   ├── plans/          # Implementation plans
│   ├── research/       # Research outputs (flat files)
│   ├── canvas/         # Excalidraw diagrams
│   └── reference/      # Reference documents
├── scratch.md          # Per-session working memory
└── CLAUDE.md           # Project instructions for Claude
```

## How It Works

1. **Session Start (`/begin`)**: Loads `state.md` + last session handoff for cold start context
2. **During Session**: Use `scratch.md` to capture decisions, tasks, and notes
3. **Session End (`/wrap`)**: Creates session handoff, decision files, updates state, prepares for next session
4. **Automatic Export**: Hooks export transcripts and capture research outputs

## Vault Integration

The vault directory is Obsidian-compatible. Open it in Obsidian for:
- Graph view of connected notes
- Dataview queries on dashboard
- Quick search across sessions
- Excalidraw diagram editing

**Pre-configured plugins:** Dataview, Excalidraw (settings in `.obsidian/`)

## MCP Server

The project includes a pre-configured `.mcp.json` that sets up the Obsidian MCP server pointing at your vault. This gives Claude native Obsidian search, directory listing, and frontmatter queries.

To add a **brain vault** (personal cross-project knowledge base), add a second server to `~/.claude.json`:

```json
{
  "mcpServers": {
    "brain": {
      "type": "stdio",
      "command": "npx",
      "args": ["@mauricio.wolff/mcp-obsidian@latest", "/path/to/your/notes"]
    }
  }
}
```

## License

MIT
