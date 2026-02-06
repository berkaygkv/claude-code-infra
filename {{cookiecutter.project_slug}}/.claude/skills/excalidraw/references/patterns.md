# Common Diagram Patterns

Reusable patterns for complex diagrams using the layout engine.

## Pipeline with Side Input

A vertical flow with an auxiliary element feeding into one stage.

```python
from layout import Diagram, Theme

d = Diagram(start_x=100, start_y=100)

# Main pipeline
stage1 = d.add_card("Stage 1", subtitle="Process data", icon="📦",
                     theme=Theme.BLUE, width=280, height=90, x=260, y=100)

stage2 = d.add_card("Stage 2", subtitle="Transform", icon="⚡",
                     theme=Theme.ORANGE, width=280, height=90, x=260, y=230)

# Side input (left of stage 1)
config = d.add_card("Config", subtitle="Settings",
                     icon="📋", theme=Theme.PURPLE, width=150, height=70, x=60, y=115)

# Arrows
d.add_arrow(stage1, stage2, from_side="bottom", to_side="top")
d.add_arrow(config, stage1, from_side="right", to_side="left", theme=Theme.PURPLE)
```

**Key points:**
- Side input card is shorter than main cards
- Position side input vertically centered on its target stage
- Use a distinct theme color for the side input

## Feedback Loop (U-Shape Arrow)

A connection that loops back from a later stage to an earlier one.

```python
# Main stages
context = d.add_card("Context Craft", subtitle="Query + Filter",
                      icon="🔍", theme=Theme.BLUE, width=280, height=90, x=260, y=300)

store = d.add_card("Store", subtitle="Neo4j graph",
                    icon="🗄️", theme=Theme.PURPLE, width=280, height=90, x=260, y=600)

# Feedback loop: store -> context (same side = auto U-shape)
d.add_arrow(store, context,
            from_side="left", to_side="left",   # same side triggers U-shape
            theme=Theme.PURPLE,
            stroke_style="dashed",
            label="Existing entities")           # auto-positioned label
```

**Key points:**
- Use `from_side` and `to_side` on the **same side** ("left"/"left") — auto-routing picks U-shape
- Or specify `routing="u-left"` explicitly
- `label` is auto-positioned at the midpoint of the vertical segment
- Use `dashed` stroke to distinguish feedback from primary flow
- `clearance=60` (default) controls how far the loop extends sideways

## Side Info Panels (Auto-Sized)

Reference panels positioned alongside the main diagram.

```python
# Auto-sized panel — no manual height calculation
schema_panel = d.add_panel(
    title="SCHEMA REFERENCE",
    content="Node Types: Process, Requirement,\n"
            "  Document, Decision, Role,\n"
            "  System, Term, Project\n"
            "Edge Types: contains, precedes,\n"
            "  depends_on, implements, ...",
    width=300,
    title_color="#2f9e44",    # green header
    x=650, y=200,
)

# Another panel below
rules_panel = d.add_panel(
    title="MERGE RULES",
    content="Scalars: doc timestamp wins\n"
            "Collections: union\n"
            "Edges: doc-scoped deletion",
    width=300,
    title_color="#e8590c",    # orange header
    x=650, y=schema_panel.bbox.bottom + 20,  # position below previous
)
```

**Key points:**
- `add_panel` auto-calculates height from content — no guessing
- Stack panels using `bbox.bottom + gap` for vertical spacing
- Use `title_color` to match the panel's topic (green for schema, orange for rules)

## Annotated Pipeline Flow

A complete pipeline with group boundary, side inputs, feedback, and side panels.

```python
d = Diagram(start_x=0, start_y=0)

# Title
d.add_text("SYSTEM OVERVIEW", font_size=28, color="#1864ab", x=260, y=20)

# Pre-section (dimmed)
DIMMED = ColorTheme("#f1f3f5", "#ced4da", "#868e96", "#ced4da", "#adb5bd")
pre = d.add_box("Input: Raw Data", theme=DIMMED, width=280, height=50, x=260, y=80)

# Group boundary
mvp_y = 170
# ... add all stages inside boundary ...
mvp_end_y = 900
d.add_group("PIPELINE", width=380, height=mvp_end_y - mvp_y,
            x=210, y=mvp_y)  # label defaults to above-center

# Post-section (dimmed)
post = d.add_box("Output: Results", theme=DIMMED, width=280, height=50, x=260, y=mvp_end_y + 30)
```

**Key points:**
- Group label defaults to `"above-center"` — no arrow collision
- Place group box AFTER all internal elements (renders behind them)
- Use dimmed theme for pre/post sections outside the main boundary

## Grid with Schema Reference

Display enumerated types in a clean grid.

```python
# Node types (2 columns, 8 items — fills evenly)
d.add_grid(
    ["Process", "Requirement", "Document", "Decision",
     "Role", "System", "Term", "Project"],
    cols=2, theme=Theme.GREEN,
    box_width=130, box_height=30, spacing=8,
    x=650, y=200,
)

# Edge types (3 columns, 13 items — last row centered)
d.add_grid(
    ["contains", "precedes", "depends_on",
     "implements", "documents", "owns",
     "consumes", "produces", "supersedes",
     "defines", "blocked_by", "applies_to",
     "references"],
    cols=3, theme=Theme.ORANGE,
    box_width=90, box_height=26, spacing=6,
    x=650, y=400,
    center_last_row=True,   # "references" centered in last row
)
```

**Key points:**
- `center_last_row=True` (default) centers incomplete last rows
- Choose `cols` to minimize orphan items (13 items / 3 cols = 4 full + 1 orphan)
- Use smaller `box_height` for compact grids (26-30px)

## Arrow Routing Quick Reference

| Scenario | `from_side` | `to_side` | Auto Route | Manual Override |
|----------|------------|-----------|------------|-----------------|
| Vertical flow | `bottom` | `top` | `straight` | — |
| Horizontal flow | `right` | `left` | `straight` | — |
| Offset vertical | `bottom` | `top` (different x) | `z-mid` | `routing="l-down-right"` |
| Side input | `right` | `left` (different y) | `z-mid` | `routing="l-right-down"` |
| Feedback loop | `left` | `left` | `u-left` | `clearance=80` for wider loop |
| Parallel return | `right` | `right` | `u-right` | — |

## Theme Quick Reference

| Theme | Use For | Icon |
|-------|---------|------|
| `Theme.BLUE` | Primary pipeline stages | 📦 🔍 |
| `Theme.GREEN` | Validation, success | ✅ |
| `Theme.PURPLE` | Data stores, schemas | 📋 🗄️ |
| `Theme.ORANGE` | Merge, transform, edges | ⚡ |
| `Theme.AI` | LLM/AI processing stages | 🤖 🧠 |
| `Theme.RED` | Hub elements, alerts | 🚨 |
| `Theme.GRAY` | Group boundaries, neutral | — |
| `DIMMED` (custom) | Pre/post MVP, inactive | 📄 |

Custom dimmed theme:
```python
DIMMED = ColorTheme("#f1f3f5", "#ced4da", "#868e96", "#ced4da", "#adb5bd")
```
