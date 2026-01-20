# Session Rollback Command

This command reverses file changes made after a specified point in the conversation, enabling a clean `/rewind`.

## Background

Claude Code's `/rewind` restores conversation but not code (bug #15403). MCP tool calls are never tracked. This command uses the conversation history itself as a changelog to reverse file changes before the user runs `/rewind`.

## Instructions

When the user invokes `/rollback`, they will provide a description or partial quote of the target message. Your job is to:
1. Identify the target message
2. Find all file changes made AFTER that message
3. Reverse those changes
4. Report what was rolled back
5. Prompt the user to `/rewind`

### Step 1: Identify Target Message

The user will describe the message they want to roll back to, such as:
- "rollback to before 'Let's build something clever...'"
- "rollback to my message asking about the architecture"
- "rollback to before we started the refactor"

Scan your conversation history and identify the specific message they're referring to. If ambiguous, ask for clarification.

**Confirm with the user:**
```
I'll roll back to before: "{identified message preview}..."
This will reverse all file changes made after that point.

Proceed? (yes/no)
```

### Step 2: Inventory Changes to Reverse

Scan the conversation AFTER the target message for all file-modifying operations:

**Track these tool calls:**
- `Edit` → Record: file_path, old_string, new_string
- `Write` → Record: file_path, content written
- `NotebookEdit` → Record: notebook_path, cell changes
- `mcp__obsidian__write_note` → Record: path, content written
- `mcp__obsidian__patch_note` → Record: path, changes
- `mcp__obsidian__delete_note` → Record: path

**Also note any preceding Read operations** that captured the original state:
- `Read` → Original content before modification
- `mcp__obsidian__read_note` → Original content before modification

Build a chronological list of changes with their original states (if available).

### Step 3: Reverse Changes (Reverse Chronological Order)

Process changes from MOST RECENT to OLDEST:

**For Edit:**
```
Edit: old_string={new_string}, new_string={old_string}
```
(Swap the strings to reverse the edit)

**For Write (existing file):**
- If you Read the file earlier in conversation, Write the original content
- If no Read exists, warn user: "Cannot restore {file} - original content unknown"

**For Write (new file created):**
```bash
rm {file_path}
```

**For mcp__obsidian__write_note (existing note):**
- If you read_note earlier, write_note with original content
- If no read exists, warn user

**For mcp__obsidian__write_note (new note):**
```
mcp__obsidian__delete_note: path
```

**For mcp__obsidian__delete_note:**
- If you read_note before deletion, write_note to restore
- If no read exists, warn user: "Cannot restore deleted note - content unknown"

### Step 4: Report Results

Present a summary table:

```
## Rollback Complete

Rolled back to: "{target message preview}..."

| File | Action | Status |
|------|--------|--------|
| path/to/file.ts | Edit reversed | ✓ |
| path/to/new-file.ts | Deleted (was created after target) | ✓ |
| notes/overview.md | Content restored | ✓ |
| notes/other.md | ⚠️ Could not restore - original unknown | |

**Warnings:**
{list any files that couldn't be fully restored}
```

### Step 5: Prompt for /rewind

```
Files have been rolled back.

Now run `/rewind` and select the message:
> "{target message preview}..."

This will restore both conversation and files to that point.
```

## Handling Edge Cases

### Bash Commands
Bash commands that modified files CANNOT be reversed by this command. Warn the user:
```
⚠️ Bash commands were executed after the target message that may have modified files:
- `rm some-file.txt`
- `mv old.txt new.txt`

These changes cannot be automatically reversed. You may need to restore manually via git.
```

### External State Changes
Operations like `git push`, API calls, database writes cannot be undone. Note them:
```
⚠️ The following external operations cannot be reversed:
- git push origin main
- API call to external service
```

### No Changes Found
If no file changes exist after the target message:
```
No file changes found after the target message.
You can safely `/rewind` without needing to rollback files.
```

### Ambiguous Target
If multiple messages match the user's description:
```
I found multiple messages matching your description:

1. (12 messages ago): "Let's build something clever for the API"
2. (8 messages ago): "Let's build something clever for the UI"

Which one should I roll back to? (1 or 2)
```

## Example

**User:** `/rollback` to before "let's test the rewind behavior"

**Claude:**
```
I'll roll back to before: "let's test the rewind behavior"
This will reverse all file changes made after that point.

Proceed? (yes/no)
```

**User:** yes

**Claude:**
```
## Analyzing Changes

Found 3 file modifications after target message:

1. Edit to CLAUDE.md - added test marker
2. MCP write to notes/overview.md - added frontmatter field
3. Edit to CLAUDE.md - removed test marker (already reversed)

## Rolling Back

| File | Action | Status |
|------|--------|--------|
| CLAUDE.md | Edit reversed | ✓ |
| notes/overview.md | Content restored | ✓ |

## Rollback Complete

Files have been rolled back.

Now run `/rewind` and select the message:
> "let's test the rewind behavior"

This will restore both conversation and files to that point.
```

## Notes

- Always confirm before making changes
- Process in reverse chronological order to handle dependent changes correctly
- If unsure about original state, err on the side of caution and warn the user
- This command complements git - for session-boundary rollbacks, git checkout is simpler
- After rollback, the user MUST run `/rewind` to sync conversation state
