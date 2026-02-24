# Scratch — Session 48

Session objective: [LOCKED] Design collaborative working surface + project management foundations

## Problem

Communication between sessions is lossy (handoff compression loses nuance) and within sessions is one-directional (chat turns have no positional feedback). No shared vocabulary for intent — user says "reflect on the plan" and hopes Claude infers correctly. Ideas have no lifecycle — they either become tasks instantly or disappear. Task list is a flat dump with no quality gate.

---

## Proposal: Collaborative Working Surface

### 1. scratch.md evolves

From "Claude's reasoning surface" to **shared working surface**. Both parties write, both annotate. Rewrite-not-append still applies — keep it live, not a log. This supersedes scratch-pad-v2.

### 2. Markup convention (Obsidian callouts)

Annotations use callouts — visually distinct in Obsidian, collapsible, semantic:

- `> [!question]` — Don't follow / needs clarification
- `> [!warning]` — Disagree / see a flaw
- `> [!tip]` — Extend this with...
- `> [!done]` — Agreed, move on
- `> [!info]` — Context or reference (either party)

Inline highlights `==like this==` for emphasis on specific phrases within text.

### 3. Content blocks are labeled

Every proposal section gets a short label (like `### 3. Content blocks are labeled`). References in chat use the label: "I marked up section 3." No ambiguity about what you're responding to.

### 4. Lifecycle

- Initialized at `/begin` (same as now)
- Either party writes content anytime
- **"Ready for marks"** = Claude signals structured content needs review
- **"Read it"** = user signals annotations are done
- Claude reads back, responds only to marked items
- Reset at `/wrap` — key reasoning migrates to handoff first

### 5. Context window insurance

File persists when early chat gets compressed. Critical reasoning, agreements, and open questions live in the file, not buried in scroll-away chat. Both parties can park things here specifically to survive context bloat.

### 6. User-initiated content

Not just annotations on Claude's output. User writes their own blocks anytime — ideas to carry, constraints to remember, questions to park. This is a shared surface, not Claude's notepad.

---

## Open Questions

- Does callout syntax feel fast enough for quick marks, or would lighter inline markers (`[?]`, `[!]`, `[+]`) be better for speed?
- Should resolved items get deleted immediately, or collect in a `## Resolved` section at the bottom before next rewrite?
- How does this interact with the broader project management design (lifecycle, shared language, quality gates)? Is this the foundation piece we build first, then layer the rest on top?
