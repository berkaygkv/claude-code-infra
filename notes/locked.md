---
type: locked-decisions
project: kh
updated: '2026-01-20'
---
# Locked Decisions

> This document contains committed decisions for the KH project. Changes require explicit rationale and approval. Edit with care.

## Target
<!-- 2-3 sentences: what we're building, the end state -->

Building a symbiotic collaboration framework that enables seamless session handoffs between human and AI collaborators. The end state is a persistent knowledge system where context flows naturally across sessions without loss.

## Decisions
<!-- Table: Area, Decision, Rationale -->

| Area | Decision | Rationale |
|------|----------|-----------|
| File Location | Notes live in `kh/notes/`, symlinked into Obsidian vault | Git can't track files through symlinks; this direction required for versioning |
| Task Format | Dataview inline fields `[phase:: x] [priority:: n]` | Enables queryable checklists while keeping markdown readable |
| Git Exclusions | `.obsidian/` excluded via `.gitignore` | Workspace config is local, not versioned |

## Schemas

### Session Note Schema

Session notes live in `notes/Sessions/session-{N}.md` and capture the state at session end for handoff.

**Frontmatter:**

```yaml
session: {N}              # Sequential session number
date: 'YYYY-MM-DD'        # Session date
project: kh               # Project identifier
topics:                   # Array of topic tags
  - topic-one
  - topic-two
outcome: successful       # Enum: successful | blocked | partial
continues_from: session-{N-1}  # Optional: previous session reference
transcript: '[[Sessions/transcripts/session-{N}]]'  # Link to full transcript
tags:
  - session
```

**Outcome values:**
- `successful` — Goals achieved, clear next steps defined
- `blocked` — Hit an impediment that prevents progress
- `partial` — Some progress made but session ended early

**Content structure:**

```markdown
## Handoff

### Context
<!-- 2-4 sentences: What this session focused on, what was accomplished -->

### Decisions
<!-- Bulleted list of decisions made this session -->
<!-- Format: "- LOCKED: {decision} — {rationale}" or "- OPEN: {issue} — {current thinking}" -->

### Memory
<!-- Technical facts, paths, quirks, workarounds discovered -->
<!-- These persist across sessions and inform future work -->

### Next Steps
<!-- Prioritized list of what to do next -->
<!-- These become suggestions in the next /begin -->
```

### Handoff Section Guidelines

**Context:** Brief narrative summary. Should be enough to understand what happened without reading the transcript. Focus on outcomes, not process.

**Decisions:** Distinguish between:
- `LOCKED` — Committed decisions that shouldn't change without good reason
- `OPEN` — Identified issues or questions still being explored

**Memory:** Facts that future sessions need to know:
- File paths and configurations
- Tool quirks and workarounds
- Environment-specific details
- API behaviors discovered

**Next Steps:** Ordered by priority. First item becomes the default suggestion for `/begin`.


