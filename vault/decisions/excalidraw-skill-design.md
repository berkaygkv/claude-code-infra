---
type: decision
title: Excalidraw Skill Design
status: locked
date: 2026-02-04
session: "[[sessions/session-22]]"
supersedes: null
superseded_by: null
related: []
tags:
  - decision
  - excalidraw
  - skill
---

## Decision

Custom excalidraw skill with:
- **Diagram types:** Flowchart, System, Mind Map, Sequence, Timeline
- **Output location:** vault/canvas/{slug}.excalidraw
- **Invocation:** Auto-detect drawing requests + manual /excalidraw
- **Modification:** Support editing existing diagrams
- **Naming:** Claude picks contextual slug based on content

## Rationale

1. **5 diagram types** cover the core sense-making needs: process (flowchart), structure (system), exploration (mind map), interaction (sequence), planning (timeline)

2. **vault/canvas/** integrates with Obsidian's Excalidraw plugin and keeps diagrams with other vault content

3. **Auto-detect + manual** provides flexibility — natural language triggers ("draw a diagram of...") plus explicit /excalidraw command

4. **Modification support** enables iterative refinement without regenerating from scratch

5. **Claude picks slug** reduces friction — no need to specify filename

## Alternatives Considered

- **Install ccc plugin** — Plugin marketplace install failed; also wanted tighter kh integration
- **More diagram types** — Scoped to 5 most useful; can expand later
- **Strict naming convention** — Rejected in favor of contextual slugs
