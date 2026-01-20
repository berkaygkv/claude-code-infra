# Meta-Journal Entry Command

This command records an insight to the meta-journal, linking it to the current session.

## Purpose

Capture learnings about how we work together:
- **Flaws:** Reasoning patterns that didn't serve us
- **Patterns:** Approaches that work well
- **Hypotheses:** Ideas we think might work, to validate later

These entries become raw material for improving our collaborative approach over time.

## Instructions

When the user invokes `/meta`, perform these steps:

### Step 1: Load Session Context

Read the current session context:

```bash
cat /tmp/kh-session.json 2>/dev/null || echo "{}"
```

If the file exists, extract:
- `session_number` → for linking
- `topic` → for the session reference
- `date` → for the entry date

If the file doesn't exist or is empty, prompt:
```
⚠️ No active session context found.

Please provide:
- Session number:
- Session topic:
```

### Step 2: Gather Entry Details

Prompt for each field:

```
## Recording Meta-Journal Entry

Session: {session_number}: {topic}

**Background** (What were we doing? What prompted this insight?)
>
```

After user responds:

```
**Insight** (What did we learn? What works, what doesn't, or what might work?)
>
```

### Step 3: Format Entry

Build the entry using this format:

```markdown
### {YYYY-MM-DD} — [[Sessions/session-{N}|session-{N}: {topic}]]

{background}

**Insight:** {insight}

---
```

The background should flow naturally as a brief paragraph. The insight is the key takeaway.

### Step 4: Prepend to Meta-Journal

Read the current meta-journal:
```
mcp__obsidian__read_note: path="notes/meta-journal.md"
```

Use `mcp__obsidian__patch_note` to prepend the entry:
- `oldString`: `<!-- New entries are prepended below this line -->`
- `newString`: `<!-- New entries are prepended below this line -->\n\n{formatted entry}`

If the meta-journal doesn't exist, create it first with the initial template (see Notes section).

### Step 5: Update Frontmatter

Update the `updated` field in meta-journal frontmatter:

```
mcp__obsidian__patch_note:
  path: "notes/meta-journal.md"
  oldString: 'updated: "{old-date}"'
  newString: 'updated: "{today}"'
```

### Step 6: Confirm Entry

Display confirmation:

```
## Meta-Journal Entry Recorded

**Session:** session-{N}: {topic}
**Date:** {YYYY-MM-DD}

**Insight:** {insight}

Entry added to [[notes/meta-journal|meta-journal]].
```

## Edge Cases

### No Session Context

If `/begin` wasn't run and the user doesn't know session details:
1. Check for the most recent session number in the vault
2. Offer to use that as reference, or let them specify manually
3. Warn that linking may be approximate

### Meta-Journal Doesn't Exist

If `notes/meta-journal.md` doesn't exist, create it with:

```markdown
---
type: meta-journal
project: kh
created: "{today}"
updated: "{today}"
tags:
  - meta
  - principles
---

# Meta-Journal

> Cognitive and structural flaws observed during collaboration, with corrections and derived principles.

---

## Entries

<!-- New entries are prepended below this line -->
```

Then proceed with adding the entry.

### Multiple Entries Per Session

Each `/meta` invocation creates a separate entry. All entries from the same session will have the same session link, which is expected and useful for seeing all learnings from a single session.

## Example

**User:** `/meta`

**Claude:**
```
## Recording Meta-Journal Entry

Session: 8: meta-journal-system

**Background** (What were we doing? What prompted this insight?)
>
```

**User:** We built a /rollback command to handle MCP write reversals, then realized we were solving the wrong problem. The real issue was making speculative writes to the vault in the first place.

**Claude:**
```
**Insight** (What did we learn? What works, what doesn't, or what might work?)
>
```

**User:** Procedural change before tooling change. Don't build tools to recover from problems—eliminate the conditions that create them.

**Claude:**
```
## Meta-Journal Entry Recorded

**Session:** session-8: meta-journal-system
**Date:** 2026-01-20

**Insight:** Procedural change before tooling change. Don't build tools to recover from problems—eliminate the conditions that create them.

Entry added to [[notes/meta-journal|meta-journal]].
```

## Notes

- Entries are prepended (newest first) to make recent learnings visible
- The wikilink format `[[Sessions/session-{N}|session-{N}: {topic}]]` enables click-through in Obsidian
- Background provides context; insight is the key takeaway
- This is a diary, not a formal document—entries don't need to be perfect
- Use for flaws, working patterns, or hypotheses to validate later
