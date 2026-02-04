---
type: research-output
id: OUTPUT-20260120-110505-conduct-thorough-research-on-claude
target: '[[research/targets/TARGET-20260120-102231-the-best-practices-for-using-claude]]'
created: 2026-01-20
researcher: claude-deep-research
tags:
  - research
---

# Research Output: on Claude Code's /rewind command and checkpointing system. We need to understand

**Target:** [[research/targets/TARGET-20260120-102231-the-best-practices-for-using-claude]]

**Question:** Conduct thorough research on Claude Code's /rewind command and checkpointing system. We need to understand exactly how it works and why a user might not see the "restore code" option.

## Context
- Us...

---

## Findings

Now I have comprehensive information. Let me compile this into a structured research report.

This research investigates Claude Code's /rewind command and checkpointing system, focusing on why users may not see the "restore code" option despite making file changes. The investigation reveals a complex situation involving multiple Claude Code interfaces, a critical server-side bug, and fundamental limitations in what operations are tracked.

## Research Summary

### Question/Topic
Why does Claude Code's /rewind command only show "Restore conversation" option without "restore code" capability, even when file changes were made using the Edit tool and MCP (Obsidian) tools?

### Key Findings

1. **Critical Bug (Issue #15403)**: A server-side change on December 25, 2025 broke code restoration for all new checkpoints. The system switched from inline backup storage to external file references, but the rewind functionality was not updated to read these external files.

2. **Interface-Specific Availability**: Checkpointing features vary dramatically across Claude Code interfaces:
   - **CLI (Terminal)**: Full /rewind support available ✅
   - **VS Code Extension**: No checkpoint/rewind functionality ❌
   - **Web Interface (claude.ai/code)**: Unclear/undocumented availability

3. **Tool Tracking Limitations**: Only three built-in tools are tracked for checkpointing:
   - Write
   - Edit  
   - NotebookEdit
   
   **MCP tools are NOT tracked**, including Obsidian MCP operations.

4. **Bash Exclusion**: Any file modifications made through Bash commands are permanently excluded from checkpointing and cannot be restored.

5. **Environment Variable Requirement**: The SDK requires `CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING=1` to be set, but this appears to be SDK-specific, not affecting the standard CLI.

### Detailed Analysis

#### Checkpoint Mechanics

Checkpointing in Claude Code operates by creating backups before file modifications. According to the official documentation, when file checkpointing is enabled, the SDK creates backups of files before modifying them through the Write, Edit, or NotebookEdit tools. Each user message in the response stream includes a checkpoint UUID that serves as a restore point.

**Checkpoint Creation:**
- Automatically triggered before each file edit
- One checkpoint created per user prompt
- Checkpoints persist across sessions
- Automatic cleanup after 30 days (configurable)

**Storage Architecture (Post-Dec 25, 2025):**
- Early system: Backups stored inline in session JSONL files
- Current system: External file references with pattern `{backupFileName: "36df1dac6388d763@v1"}`
- External files stored in `~/.claude/file-history/{sessionId}/`

#### The December 25, 2025 Bug

A critical issue was identified in GitHub Issue #15403. User hasen6 provided detailed forensic analysis:

**Timeline:**
- **Before Dec 25, 13:30 GMT+7**: Checkpoints functional with inline storage
- **After Dec 25, 13:30 GMT+7**: Server-side change to external file references
- **Result**: Rewind functionality unable to read external backup files

**Technical Root Cause:**
The `trackedFileBackups` structure changed from:
```json
{"backupFileName": null, "version": 1, ...}  // Inline storage
```
to:
```json
{"backupFileName": "36df1dac6388d763@v1", "version": 1, ...}  // External reference
```

The backup files ARE being created and contain correct data, but the rewind code was not updated to:
1. Check if `backupFileName` is null (inline) or has a value (external)
2. Read from the external file path when present
3. Apply that content during restoration

**User Impact:**
- All checkpoints created before Dec 25, 13:30 GMT+7 still work
- All checkpoints created after this time show "code will be unchanged"
- Affects all platforms (confirmed on macOS, likely universal)

#### Interface-Specific Limitations

**CLI (Command Line Interface):**
- ✅ Full /rewind functionality
- Access: Press `Esc` twice or type `/rewind`
- Three restore options: conversation only, code only, or both
- ⚠️ UI issues: garbled text, laggy scrolling, 100% CPU spikes reported

**VS Code Extension:**
- ❌ No checkpoint/rewind functionality (as of Jan 2026)
- GitHub Issue #10352 (open since Oct 26, 2025)
- Community impact statement (Jan 11, 2026): "It's now been 103 days since the Rewind feature was announced, but it's still unavailable in the now-default VS Code UI"
- Workarounds: Switch to CLI for rewind-critical sessions, use git, plan prompts carefully

**Web Interface:**
- Documentation does not explicitly confirm /rewind availability for claude.ai/code
- Features appear exclusive to CLI and VS Code extension (when implemented)

#### Tool Coverage: What Gets Tracked vs Not Tracked

**✅ TRACKED (Restorable via /rewind):**

| Tool | Description |
|------|-------------|
| Write | Creates new file or overwrites existing file |
| Edit | Makes targeted edits to specific parts of existing file |
| NotebookEdit | Modifies cells in Jupyter notebooks (.ipynb files) |

**❌ NOT TRACKED (Cannot be restored):**

| Category | Examples | Reason |
|----------|----------|--------|
| Bash commands | `rm`, `mv`, `cp`, `echo >`, `sed -i` | Explicitly excluded from checkpoint system |
| MCP tool operations | Obsidian MCP write operations | MCP tools are external to tracked tools |
| External modifications | Manual edits outside Claude Code | Only current session tracked |
| Concurrent sessions | Changes from other Claude Code instances | Session-specific tracking |
| Directory operations | Creating/moving/deleting directories | Only file content tracked |
| Non-file operations | API calls, database queries | File-only system |

**Critical Finding for User's Scenario:**
The user made changes via:
1. Edit tool to CLAUDE.md → Should be tracked ✅
2. MCP (Obsidian) to note file → **NOT tracked** ❌

This explains why code restore might not appear—if the only tracked changes (Edit to CLAUDE.md) were made before the Dec 25 bug, or if the system only detected the untracked MCP changes.

#### Configuration and Settings

**For CLI Users:**
- No configuration required
- Checkpointing enabled by default
- No settings to disable/enable

**For SDK Users (Programmatic Access):**

Required configuration:
```python
options = ClaudeAgentOptions(
    enable_file_checkpointing=True,
    permission_mode="acceptEdits",
    extra_args={"replay-user-messages": None},
    env={**os.environ, "CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING": "1"}
)
```

Key parameters:
- `enable_file_checkpointing`: Activates backup creation
- `replay-user-messages`: Required to receive checkpoint UUIDs
- `CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING`: Environment variable gate

**Checkpoint Cleanup:**
- Default: 30 days
- Configurable in SDK
- Automatic cleanup with sessions

#### Edge Cases and Gotchas

1. **New Files vs Existing Files**
   - Both tracked equally
   - Rewinding deletes created files, restores modified files

2. **Files Outside Working Directory**
   - Local files only
   - Remote/network files not tracked

3. **Session Boundaries**
   - Checkpoints persist across resumed sessions
   - Can rewind in later session if session ID retained

4. **Concurrent Modifications**
   - Only same-file overlaps captured
   - Generally unreliable for concurrent sessions

5. **Process Timing**
   - Calling `rewindFiles()` after stream completes causes "ProcessTransport is not ready" error
   - Solution: Resume session with empty prompt first

6. **Destructive Operations**
   - `git push`, database operations, external API calls cannot be undone
   - Checkpointing is code-state only, not system-state

### Limitations & Gotchas

**The MCP Blind Spot:**
This is the most critical limitation for users integrating Claude Code with external systems. MCP tools—including the Obsidian MCP server used for vault operations—perform file modifications that are completely invisible to Claude Code's checkpointing system. When you ask Claude to update a note via Obsidian MCP, that change is permanent and unrewindable.

**The Bash Black Hole:**
Any operation performed through Bash is permanent. This includes:
- File deletion (`rm`)
- File moves (`mv`)  
- Stream edits (`sed -i`)
- Output redirection (`echo >`)
- In-place transformations

These operations may be trackable via git, but Claude Code's /rewind cannot help.

**The December 25 Bug Impact:**
If you're experiencing missing "restore code" options on checkpoints created after December 25, 2025, this is a confirmed bug, not user error. The backup data exists, but the UI cannot access it. Workaround: Create a new session and make the changes again, or manually recover from `~/.claude/file-history/{sessionId}/` if comfortable with terminal operations.

**Version Control is Still Required:**
Checkpointing is not a replacement for git. It's designed for quick, session-level undo operations. For permanent history, collaboration, and recovery beyond 30 days, proper version control is essential.

**Interface Fragmentation:**
If you're using the VS Code extension (now the default interface for many users), you don't have access to /rewind at all. This creates a significant usability gap and forces users to choose between clean UI (VS Code) and safety features (CLI).

### Recommendations

1. **For Users Experiencing Missing "Restore Code" Options:**
   - Check your checkpoint creation date—if after Dec 25, 2025 13:30 GMT+7, you're affected by Issue #15403
   - Try rewinding to checkpoints created before that date if available
   - Consider switching to CLI if currently using VS Code extension
   - Monitor GitHub Issue #15403 for resolution updates

2. **For MCP + Claude Code Workflows:**
   - **Accept that MCP tool operations are not checkpointed**
   - Use git commits before MCP-heavy operations
   - Consider third-party MCP checkpoint servers like Rewind-MCP or ClaudePoint
   - Structure workflows to minimize MCP file operations or batch them with explicit save points

3. **For Mission-Critical Work:**
   - Use Claude Code CLI (not VS Code extension) until rewind parity achieved
   - Establish explicit git checkpoint strategy independent of /rewind
   - Consider third-party solutions: Checkpoints for Claude Code, ccundo, Rewind-MCP
   - Test /rewind functionality at session start with a throwaway file

4. **For Developers Building with SDK:**
   - Always set `CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING=1`
   - Capture both checkpoint UUID and session ID for later rewind
   - Implement validation logic to detect when rewind capability exists
   - Handle "no file checkpoint found" errors gracefully

5. **Workflow Architecture:**
   - Separate tracked operations (Edit/Write) from untracked (Bash/MCP)
   - Create explicit checkpoints (via user messages) before risky operations
   - Use git for operations involving Bash or MCP tools
   - Document which parts of workflow are rewindable vs permanent

### Open Questions

1. **MCP Tool Tracking Architecture:**
   - Could MCP tools theoretically integrate with Claude Code's checkpoint system?
   - Would this require changes to MCP protocol specification?
   - Are there technical barriers preventing MCP checkpoint integration?

2. **Resolution Timeline for Issue #15403:**
   - When will Anthropic deploy a fix for the December 25 external file bug?
   - Will the fix be retroactive (making existing broken checkpoints work)?
   - Or will it only apply to new checkpoints going forward?

3. **VS Code Extension Roadmap:**
   - When will checkpoint/rewind functionality reach the VS Code extension?
   - Will it have feature parity with CLI or a different implementation?
   - Is there a beta program for early access?

4. **Web Interface Capabilities:**
   - Does the claude.ai/code web interface support /rewind?
   - If not, is it planned?
   - What is the official support matrix across CLI/Extension/Web?

5. **Configuration Expansion:**
   - Will there be settings to control checkpoint frequency?
   - Could users configure which tools are tracked?
   - Are there plans for checkpoint size/retention controls?

6. **Third-Party Integration:**
   - Will Anthropic provide official APIs for third-party checkpoint tools?
   - Could the MCP protocol be extended to support checkpoint hooks?
   - Are there plans to incorporate features from popular third-party tools (ccundo, ClaudePoint) into official product?

### Sources

1. [Checkpointing - Claude Code Docs](https://code.claude.com/docs/en/checkpointing) - Official documentation
2. [Rewind file changes with checkpointing - Claude Docs](https://platform.claude.com/docs/en/agent-sdk/file-checkpointing) - SDK documentation with technical implementation details
3. [ClaudeLog - Rewind Mechanics](https://claudelog.com/mechanics/rewind/) - Community documentation
4. [GitHub Issue #15403 - Checkpoints cannot be restored](https://github.com/anthropics/claude-code/issues/15403) - Critical bug report with detailed forensic analysis
5. [GitHub Issue #10352 - Migrate checkpoint/rollback to VSCode extension](https://github.com/anthropics/claude-code/issues/10352) - Feature parity request
6. [GitHub Issue #9480 - Code Restore/Rewind Not Working](https://github.com/anthropics/claude-code/issues/9480) - Related bug report
7. [GitHub Issue #8850 - /rewind not working properly](https://github.com/anthropics/claude-code/issues/8850) - Additional bug reports
8. [Claude Code CLI vs VS Code Extension Comparison - ClaudeLog](https://claudelog.com/faqs/claude-code-cli-vs-vscode-extension-comparison/) - Interface feature comparison
9. [How to Use Checkpoints in Claude Code - ClaudeLog](https://claudelog.com/faqs/how-to-use-checkpoints-in-claude-code/) - Usage guide
10. [Enabling Claude Code to work more autonomously - Anthropic](https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously) - Official announcement
11. [Rewind-MCP GitHub Repository](https://github.com/khalilbalaree/Rewind-MCP) - Third-party MCP checkpoint solution
12. [ClaudePoint GitHub Repository](https://github.com/andycufari/ClaudePoint) - Third-party checkpoint tool
13. [Checkpoints for Claude Code](https://claude-checkpoints.com/) - Commercial checkpoint solution
14. [Obsidian Claude Code MCP](https://github.com/iansinnott/obsidian-claude-code-mcp) - Obsidian MCP integration documentation

---

## Key Sources

- [Checkpointing - Claude Code Docs](https://code.claude.com/docs/en/checkpointing)
- [Enabling Claude Code to work more autonomously - Anthropic](https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously)

**Full sources:** [[research/outputs/OUTPUT-20260120-110505-conduct-thorough-research-on-claude/sources]]
