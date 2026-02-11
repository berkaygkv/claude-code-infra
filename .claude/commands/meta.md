# Meta-Journal Entry Command

Capture a learning or insight to the brain vault's meta-journal.

## Purpose

Record how we work together — flaws, patterns, hypotheses. These entries compound into collaboration improvements over time.

## Instructions

When the user invokes `/meta`, perform these steps:

### Step 1: Gather Context

From scratch.md Meta section or conversation, identify:
- Session number and project name
- What prompted the insight (the background)

If context is unclear, ask briefly.

### Step 2: Capture Entry

From the conversation context, extract:
- **Background:** What were we doing? (1-2 sentences)
- **Insight:** What did we learn? (the key takeaway)

If the insight isn't obvious from context, ask: "What's the takeaway?"

### Step 3: Write to Brain Vault

Use `mcp__brain__write_note` to create an individual file:

**Path:** `_meta/journal/{slug}.md`

**Content:**
```yaml
---
type: meta
created_by: claude-code
date: {YYYY-MM-DD}
project: {current project name}
---

# {Short title}

{Background paragraph}

**Insight:** {The key takeaway}

*Session {N}, {project} project*
```

Generate `{slug}` from the insight topic (lowercase, hyphens, max 40 chars).

### Step 4: Confirm

```
Meta-journal entry recorded: _meta/journal/{slug}.md
**Insight:** {insight}
```

## Notes

- No interactive two-prompt flow — capture directly from conversation
- Session reference is plain text, not wikilinks (brain vault doesn't have project sessions)
- One file per entry in `_meta/journal/`
- Search brain vault first (`mcp__brain__search_notes`) to avoid duplicating an existing insight
