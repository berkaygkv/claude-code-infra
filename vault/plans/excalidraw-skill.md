---
type: plan
status: approved
created: 2026-02-04
project: kh
topic: excalidraw-skill
---

# Excalidraw Skill Plan

## Summary

Create a comprehensive excalidraw skill that produces quality diagrams on first attempt, supporting 5 diagram types with modification capability.

## Decisions (LOCKED)

| Decision | Detail |
|----------|--------|
| Diagram types | Flowchart, System, Mind Map, Sequence, Timeline |
| Output location | `vault/canvas/{slug}.excalidraw` |
| Naming | Claude picks contextual slug |
| Invocation | Auto-detect drawing requests + manual `/excalidraw` |
| Modification | Support editing existing diagrams |

## Diagram Types

| Type | Purpose | When to Use |
|------|---------|-------------|
| Flowchart | Process logic, decisions | "How does X work?" |
| System | Components & connections | "What are the parts?" |
| Mind Map | Idea exploration | "What are our options?" |
| Sequence | Interactions over time | "Who talks to whom?" |
| Timeline | Phases & milestones | "What's the plan?" |

## File Structure

```
.claude/commands/
  excalidraw.md                    # Main skill file
  excalidraw/                      # Reference directory
    ├── core-spec.md               # JSON structure, critical rules
    ├── arrows.md                  # Routing, bindings, edge math
    ├── colors.md                  # Semantic palette
    └── diagram-types.md           # Layout templates per type
```

## Workflow

### Generation Flow

1. **UNDERSTAND** — What to visualize, which type, key elements
2. **CONFIRM** — Brief confirmation before generating
3. **GENERATE** — Load references, apply template, create JSON
4. **VALIDATE** — Check labels, arrows, spacing, proportions
5. **WRITE** — Save to vault/canvas/{slug}.excalidraw

### Modification Flow

1. **READ** existing diagram
2. **PARSE** current elements
3. **APPLY** changes (add/remove/move)
4. **RE-VALIDATE**
5. **WRITE** updated file

## Critical Technical Rules

### Labels (Two-Element Binding)

Every labeled shape needs TWO elements:
- Shape with `boundElements: [{ id: "text-id", type: "text" }]`
- Text with `containerId: "shape-id"`

The `label` property does NOT work in raw JSON.

### Arrows (Elbow Configuration)

Three required properties for 90-degree arrows:
```json
{
  "elbowed": true,
  "roughness": 0,
  "roundness": null
}
```

### Edge Point Calculations

| Edge | Formula |
|------|---------|
| Top | `(x + width/2, y)` |
| Bottom | `(x + width/2, y + height)` |
| Left | `(x, y + height/2)` |
| Right | `(x + width, y + height/2)` |

### Shape Restrictions

- NO diamond shapes (break in raw JSON)
- Use styled rectangles for decision points (orange, dashed stroke)

## Implementation Phases

### Phase 1: Core Infrastructure
- [ ] Create `excalidraw.md` main skill file
- [ ] Create `excalidraw/core-spec.md` with JSON format rules
- [ ] Create `vault/canvas/` directory

### Phase 2: Arrow System
- [ ] Create `excalidraw/arrows.md` with routing logic
- [ ] Document edge calculations and binding patterns

### Phase 3: Visual System
- [ ] Create `excalidraw/colors.md` with semantic palette
- [ ] Define spacing constants and proportions

### Phase 4: Diagram Templates
- [ ] Create `excalidraw/diagram-types.md`
- [ ] Flowchart template and layout
- [ ] System diagram template and layout
- [ ] Mind map template and layout
- [ ] Sequence diagram template and layout
- [ ] Timeline template and layout

### Phase 5: Validation & Polish
- [ ] Add validation checklist to main skill
- [ ] Add modification workflow
- [ ] Test with sample diagrams

## Auto-Detection Triggers

Skill should activate when user says:
- "Draw a diagram of..."
- "Visualize the flow..."
- "Create a flowchart..."
- "Map out the system..."
- "Show me a timeline..."
- "Sketch out..."
- "Diagram the..."

## Quality Checklist (Pre-Output)

- [ ] All shapes have bound text labels (two-element pattern)
- [ ] All arrows use elbow configuration
- [ ] All arrows connect to shape edges (within 5px)
- [ ] No overlapping elements
- [ ] Consistent spacing (40-50px gaps)
- [ ] Proportional sizing (width accommodates label + padding)
- [ ] Color palette applied semantically

## References

- Source: https://github.com/ooiyeefei/ccc/tree/main/skills/excalidraw
- Excalidraw JSON format documentation
- Obsidian Excalidraw plugin compatibility
