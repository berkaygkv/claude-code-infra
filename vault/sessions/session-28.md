---
type: session
session: 28
date: 2026-02-07
mode: brainstorm
topics: [excalidraw-skill, layout-engine, diagram-quality, grouping, arrow-binding]
outcome: successful
continues_from: "[[sessions/session-27]]"
decisions: []
---

# Session 28: Excalidraw Skill Engine Improvements

## Context
Tested the excalidraw skill end-to-end by generating a kh system architecture diagram. Identified concrete quality issues (text overflow in grids, title misalignment, parent-child detachment, arrow labels floating). Brainstormed approaches to improve — rejected over-engineering (constraint solver, declarative API) in favor of targeted engine improvements + accepting AI spatial variance with human refinement (Workflow 1). Implemented 4 engine-level improvements to layout.py and updated SKILL.md and patterns.md.

## Decisions

### Locked
None — iterative improvement session, no formal architectural decisions.

### Open
- Workflow 2 (AI self-refinement with vision feedback) — feasible if we find a lightweight Excalidraw-to-PNG renderer. Not pursued yet.
- Should we add high-level layout methods (add_hub_spoke, add_flowchart) to the engine? Parked — current approach of patterns + engine primitives is sufficient.

## Memory
- **Excalidraw skill workflow is Workflow 1:** AI produces ~90% diagram (content, colors, hierarchy, storytelling), human handles spatial refinement (~10% drag-and-drop)
- **4 concrete engine improvements to layout.py:**
  1. `add_grid()` auto-sizes cell width from longest label when `box_width=None` (prevents text overflow)
  2. `add_title(text, subtitle)` method for properly stacked diagram titles
  3. `below=parent` parameter on `add_grid()` and `add_panel()` — anchors + groups children with parent card
  4. Arrow labels bound to arrows via `boundElements`/`containerId` — labels sit ON arrows, move natively
- **Automatic grouping in engine:**
  - Card elements (body + text + icon + emoji) share `card-group` ID
  - Parent + children via `below=` share `spoke-group` ID (outer group)
  - Nested selection: first click = spoke, double-click = card, triple-click = element
- **Source string renamed:** "skb-layout-engine" → "kh-layout-engine"
- **Hub-and-spoke pattern added** to `references/patterns.md` with positioning constants
- AI spatial reasoning is unreliable — same prompt produces different layouts each run (variance, not regression)
- Test diagrams at `vault/canvas/kh-system-architecture.excalidraw.md` and `vault/canvas/kh-architecture-v2.excalidraw.md`

## Next Steps
1. Verify hook improvements from session 27 (capture-research, export-transcript) — still pending
2. Test excalidraw skill on a DIFFERENT diagram type (flowchart or timeline) to confirm generalizability
3. Optionally research Excalidraw-to-PNG rendering for Workflow 2 (AI self-refinement)
4. Plan next work area — project is in idle phase
