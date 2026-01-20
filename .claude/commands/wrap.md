# Session Wrap-up Command

This command performs end-of-session tasks: update project documents, create session note with Handoff, and optionally commit changes.

## Instructions

When the user invokes `/wrap`, perform these steps in order:

### Step 1: Determine Session Number

Scan the Sessions folder to find the next session number:
- Check both `Sessions/` and `Sessions/transcripts/` for `session-N.md` files
- Find the highest N and use N+1 (or N if transcript already exists for this session)
- Session naming: `session-1`, `session-2`, etc.

```bash
ls -1 /home/berkaygkv/Dev/Docs/.obs-vault/notes/Sessions/*.md /home/berkaygkv/Dev/Docs/.obs-vault/notes/Sessions/transcripts/*.md 2>/dev/null | grep -oP 'session-\d+' | sort -t- -k2 -n | tail -1
```

### Step 1.5: Read Session Context

Check for session context from `/begin`:

```bash
cat /tmp/kh-session.json 2>/dev/null || echo "{}"
```

If present, use `topic` for the session note frontmatter.
If not present (session started without `/begin`), the `topic` field will be omitted (backward compatible).

### Step 2: Synthesize Session Work

Before updating any documents, synthesize what happened this session:
- What tasks were completed?
- What decisions were made (LOCKED vs OPEN)?
- What new tasks or blockers emerged?
- What is the current phase and next action?
- What should the next session start with?

This synthesis informs all document updates below.

### Step 3: Update Runbook

Read and update `notes/runbook.md` using Obsidian MCP:

1. **Mark completed tasks:** Change `- [ ]` to `- [x]` and add completion date `✅YYYY-MM-DD`
2. **Add new tasks:** If new work was identified, add to Upcoming section with `[phase:: x] [priority:: n]`
3. **Update frontmatter:**
   - `updated`: Today's date
   - `phase`: Current phase (infrastructure, validation, research, etc.)
   - `blockers`: Any blockers discovered, or "none"
4. **Update Progress section:** Add brief note about what was accomplished
5. **Update Knowledge Gaps:** Add any gaps discovered during the session

Use `mcp__obsidian__patch_note` for surgical updates or `mcp__obsidian__write_note` for full replacement.

### Step 4: Update Overview

Read and update `notes/overview.md` using Obsidian MCP:

1. **Update frontmatter:**
   - `updated`: Today's date
   - `current_phase`: Current phase
   - `next_action`: First item from Next Steps
2. **Update Current State table:** Phase, Next Action, Blockers
3. **Update Recent Sessions table:** Add this session (keep last 5 sessions)
   - Format: `| [[Sessions/session-{N}\|Session {N}]] | {date} | {outcome} | {primary topic} |`
4. **Update Active Research:** If research tasks are in progress

### Step 5: Update Locked Decisions (if applicable)

If any decisions were LOCKED this session, update `notes/locked.md`:
- Add to Decisions table with Area, Decision, Rationale
- Add any new schemas if defined

Skip this step if no new LOCKED decisions were made.

### Step 6: Generate Session Note (Handoff Document)

Create a session note following this schema:

```yaml
---
session: {N}
topic: "{topic}"  # From /tmp/kh-session.json if available
date: {YYYY-MM-DD}
project: kh
topics: [topic1, topic2]
outcome: successful | partial | blocked
continues_from: session-{N-1}
transcript: "[[Sessions/transcripts/session-{N}]]"
tags:
  - session
---

## Handoff

### Context
[What we were working on this session - 2-3 sentences summarizing the main focus]

### Decisions
- LOCKED: [decision] — [rationale]
- OPEN: [question still unresolved]

### Memory
[Important things to remember across sessions - facts, preferences, constraints discovered]

### Next Steps
[Where to pick up, what's pending - actionable items for the next session]
```

**Guidelines for Handoff generation:**

- **topics**: Extract 2-5 key topics/themes from the session (free-form tags)
- **outcome**:
  - `successful` = goals achieved, clear progress made
  - `partial` = some progress but incomplete
  - `blocked` = stuck on something, needs resolution
- **Context**: Brief summary of what the session focused on. This is what `/begin` will show to restore context.
- **Decisions**:
  - LOCKED = decisions that are final, with rationale
  - OPEN = questions still unresolved, need future attention
- **Memory**: Important facts discovered that should persist (e.g., "User prefers X over Y", "The API has limitation Z")
- **Next Steps**: Concrete, actionable items. What should the next session start with?

### Step 7: Write Session Note to Obsidian

Use the Obsidian MCP to write the session note:
- Path: `notes/Sessions/session-{N}.md`
- Use `mcp__obsidian__write_note`

### Step 8: Git Commit (Automatic)

Invoking `/wrap` signals approval to commit. Commit changes to the kh repo:

```bash
cd /home/berkaygkv/Dev/headquarter/kh
git status
git add -A
git commit -m "Session {N}: {brief summary}"
```

Skip commit if no changes. Report commit hash in Step 9.

After commit (or if skipped), clean up session context:

```bash
rm -f /tmp/kh-session.json
```

**Note:** Notes in Obsidian vault are not git-tracked.

### Step 9: Confirm Completion

Report what was done in a summary table:

```
## Session {N} Wrap-up Complete

| Document | Action |
|----------|--------|
| runbook.md | Updated: {tasks completed}, phase: {phase} |
| overview.md | Updated: added session to recent, next action: {action} |
| locked.md | {Updated with N decisions / No changes} |
| session-{N}.md | Created with handoff |

**Topics:** {topics}
**Outcome:** {outcome}

**Next Steps:**
1. {first next step}
2. {second next step}

**Git:** {committed (hash) / no changes}

Transcript will export automatically when session ends.
Use `/begin` in next session to resume.
```

## Example Output

```
## Session 15 Wrap-up Complete

| Document | Action |
|----------|--------|
| runbook.md | Updated: 2 tasks completed, phase: validation |
| overview.md | Updated: added session to recent, next action: Test transcript export |
| locked.md | No changes |
| session-15.md | Created with handoff |

**Topics:** [wrap-command-refinement, document-updates]
**Outcome:** successful

**Next Steps:**
1. Test transcript export hook
2. Begin research phase tasks

**Git:** Committed (abc1234)

Transcript will export automatically when session ends.
Use `/begin` in next session to resume.
```
