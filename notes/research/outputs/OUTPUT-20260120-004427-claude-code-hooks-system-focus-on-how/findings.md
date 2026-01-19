---
type: research-output
id: OUTPUT-20260120-004427-claude-code-hooks-system-focus-on-how
target-id: TARGET-20260119-220941
status: draft
created: 2026-01-20
researcher: claude-deep-research
confidence: medium
---

# Research Output: Claude Code hooks system. Focus on how hooks are configured and triggered.

Sco

**Target:** [[research/targets/TARGET-20260119-220941-the-key-features-of-uv-package-manager]]

**Question:** Research Claude Code hooks system. Focus on how hooks are configured and triggered.

Scope: Understanding the hooks mechanism for session automation
Depth: 2-3 authoritative sources (official docs pre...

---

## Findings

Based on comprehensive investigation of official documentation and practical guides, here's what I found about Claude Code's hooks system:

## Research Summary

### Question/Topic
Understanding Claude Code's hooks mechanism for session automation: available hook types, configuration methods, and context data available to hooks.

### Key Findings

1. **10 distinct hook events** covering the full lifecycle from session start through tool execution to completion
2. **Two hook types**: Command hooks (bash scripts) and Prompt-based hooks (LLM-driven decisions)
3. **JSON-based configuration** in settings files with matcher patterns for selective triggering
4. **Rich context data** passed via stdin as JSON, including tool inputs, session details, and environment variables

### Detailed Analysis

#### Available Hook Types

Claude Code provides **10 hook events**:

| Event | Trigger Point | Supports Matchers | Can Block Action |
|-------|--------------|-------------------|------------------|
| **SessionStart** | Session initialization | Yes | No |
| **SessionEnd** | Session termination | No | No |
| **UserPromptSubmit** | User submits prompt | No | No |
| **PreToolUse** | Before tool execution | Yes | Yes (exit 2) |
| **PostToolUse** | After tool success | Yes | No |
| **PermissionRequest** | Permission dialog shown | Yes | Yes (allow/deny) |
| **Notification** | System notifications | Yes | No |
| **Stop** | Main agent finishes | No | Yes (continue) |
| **SubagentStop** | Subagent finishes | No | Yes (continue) |
| **PreCompact** | Before context compaction | Yes | No |

**Two implementation types:**
- **Command hooks** (`type: "command"`): Execute bash scripts
- **Prompt-based hooks** (`type: "prompt"`): Use LLM for intelligent decisions (Stop/SubagentStop only)

#### Configuration Method

Hooks are defined in JSON settings files with precedence hierarchy:

```
~/.claude/settings.json              (user-wide)
.claude/settings.json                (project, committed)
.claude/settings.local.json          (local, gitignored)
```

**Basic structure:**
```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "script-or-command",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

**Matcher patterns:**
- Exact: `"Bash"`, `"Edit"`, `"Write"`
- Regex: `"Edit|Write"`
- Wildcard: `"*"` (all tools)
- MCP tools: `"mcp__server__tool"`
- Omitted/empty: matches all

**Important security feature**: Direct edits to settings files require manual review via `/hooks` menu before taking effect.

#### Context Data Available to Hooks

**JSON input via stdin:**
```json
{
  "session_id": "unique-session-id",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default|plan|acceptEdits|dontAsk|bypassPermissions",
  "hook_event_name": "EventName",
  "tool_input": {
    "command": "ls -la",
    "description": "List directory contents",
    "file_path": "/path/to/file",
    "content": "file content"
  }
}
```

**Environment variables:**
- `CLAUDE_PROJECT_DIR`: Absolute path to project root
- `CLAUDE_CODE_REMOTE`: "true" for web environments, empty for CLI
- `CLAUDE_ENV_FILE`: Path to persist environment variables (SessionStart only)

**Hook output control (exit code 0 with JSON stdout):**
```json
{
  "continue": true,
  "stopReason": "Optional message",
  "suppressOutput": false,
  "systemMessage": "Optional warning",
  "hookSpecificOutput": {
    "permissionDecision": "allow|deny|ask"
  }
}
```

**Exit codes:**
- **0**: Success, proceed
- **2**: Block action (stderr becomes error message)
- **Other**: Non-blocking error (shown in verbose mode)

#### Practical Implementation Patterns

**SessionEnd transcript export** (mentioned in CLAUDE.md):
```json
{
  "hooks": {
    "SessionEnd": [{
      "hooks": [{
        "type": "command",
        "command": "export-transcript.sh"
      }]
    }]
  }
}
```

**SubagentStop auto-capture** (for research agent):
```json
{
  "hooks": {
    "SubagentStop": [{
      "hooks": [{
        "type": "command",
        "command": "capture-research-output.sh"
      }]
    }]
  }
}
```

### Limitations & Gotchas

- **Timeout default**: 60 seconds (configurable per hook)
- **No real-time config reload**: Hook changes require `/hooks` menu review
- **Security risk**: Hooks execute with full user account permissions
- **SessionEnd cannot block**: Session termination proceeds regardless of hook result
- **Prompt hooks limited**: Only available for Stop and SubagentStop events
- **No interactive input**: Hooks must be fully automated scripts

### Recommendations

1. **For session automation**: Use SessionEnd for transcript exports and cleanup operations
2. **For subagent output capture**: Use SubagentStop with matcher patterns or parsing logic to identify agent type
3. **Configuration location**: Use `.claude/settings.local.json` for personal workflows, `.claude/settings.json` (committed) for team-wide hooks
4. **Security**: Always validate and quote variables in bash scripts, avoid touching `.env`, `.git/`, credentials
5. **Debugging**: Use exit code 0 with JSON output for non-blocking logging; test hooks independently before registering

### Open Questions

- **SubagentStop agent identification**: The documentation doesn't specify if/how to distinguish which subagent triggered the hook (e.g., deep-research vs. plan vs. bash). May require parsing transcript or tool_input context.
- **Hook execution order**: When multiple hooks match, execution order isn't explicitly documented
- **Component-scoped hooks**: Skills/Agents can define their own hooks in frontmatter, but interaction with global hooks is unclear

### Sources

1. [Get started with Claude Code hooks - Claude Code Docs](https://code.claude.com/docs/en/hooks-guide) - Practical configuration guide with examples
2. [Hooks reference - Claude Code Docs](https://code.claude.com/docs/en/hooks) - Complete reference for all hook types, configuration structure, and context data
3. [Automate Your AI Workflows with Claude Code Hooks | Butler's Log](https://blog.gitbutler.com/automate-your-ai-workflows-with-claude-code-hooks) - Real-world use cases and automation patterns
4. [A complete guide to hooks in Claude Code](https://www.eesel.ai/blog/hooks-in-claude-code) - Comprehensive overview of hook system architecture

---

## Key Sources

- [Get started with Claude Code hooks - Claude Code Docs](https://code.claude.com/docs/en/hooks-guide)
- [Hooks reference - Claude Code Docs](https://code.claude.com/docs/en/hooks)

**Full sources:** [[research/outputs/OUTPUT-20260120-004427-claude-code-hooks-system-focus-on-how/sources]]

---

## Outcome

**Decision:** *[To be determined]*

**Confidence:** Medium

**Rationale:** *[To be filled]*

**Next Steps:**
- Review findings
- *[Add next steps]*
