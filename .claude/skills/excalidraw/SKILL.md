---
name: excalidraw
description: Generate Excalidraw diagrams for visual sense-making. Use when user asks to visualize, diagram, map out, sketch, draw, or create flowcharts/mind maps/timelines/system diagrams. Outputs Obsidian-compatible .excalidraw.md files.
allowed-tools: Bash(uv run *)
context: fork
---

# Excalidraw Diagram Generator

Create **visually impressive** diagrams for sense-making. Outputs to `vault/canvas/`.

## Visual Quality Goals

Every diagram should look polished:
- **Icon circles** on key elements (emoji inside colored circle)
- **Text hierarchy** (title + subtitle in cards)
- **Coordinated colors** (one hue family per diagram)
- **Rounded corners** (`roundness: { type: 3 }`)
- **Hand-drawn feel** (`roughness: 1`)
- **Generous spacing** (60-80px between elements)

Read `references/visual-polish.md` for techniques.

## Diagram Types

| Type | Use When | Layout |
|------|----------|--------|
| **Flowchart** | "How does X work?" | Vertical |
| **System** | "What are the parts?" | Grid/Hub |
| **Mind Map** | "What are our options?" | Radial |
| **Sequence** | "Who talks to whom?" | Columns |
| **Timeline** | "What's the plan?" | Horizontal |

## Workflow

### Preferred: Use Layout Engine (prevents overlaps)

1. **Understand** — What to visualize, which type, key elements
2. **Confirm** — "Creating {type} showing {summary}. Output: vault/canvas/{slug}.excalidraw.md"
3. **Write Python script** using `layout.py` (see Layout Engine section below)
4. **Run script** — Generates JSON with correct positioning
5. **Validate** — Run `uv run scripts/validate.py <json-file>`
6. **Compress** — Run `uv run scripts/compress.py <json-file> <output.excalidraw.md>`

### Fallback: Manual JSON (error-prone)

If layout engine doesn't fit, build JSON manually following `references/json-spec.md`.

---

## Layout Engine (Recommended)

The layout engine (`scripts/layout.py`) handles positioning, text sizing, element grouping, and arrow binding automatically.

### Quick Example

```python
import sys
sys.path.insert(0, ".claude/skills/excalidraw/scripts")
from layout import Diagram, Theme

diagram = Diagram(start_x=100, start_y=100)

# Title with subtitle — properly stacked
title = diagram.add_title("SYSTEM OVERVIEW", subtitle="Architecture & Data Flow")

# Card with icon — all elements (body, text, icon, emoji) auto-grouped
card = diagram.add_card("Title", subtitle="desc", icon="📦", theme=Theme.BLUE)

# Grid anchored below card — auto-sized cells, auto-grouped with parent
grid = diagram.add_grid(["Item A", "Item B", "Item C", "Item D"],
                        cols=2, theme=Theme.GREEN, below=card)

# Arrow with bound label — label sits ON the arrow, moves with it
diagram.add_arrow(card, grid, from_side="bottom", to_side="top",
                  label="produces")

diagram.to_json("output.json")
```

### Available Methods

| Method | Description |
|--------|-------------|
| `add_title(text, subtitle)` | Diagram title + subtitle, properly stacked vertically |
| `add_card(title, subtitle, icon, theme)` | Card with icon circle — all elements auto-grouped |
| `add_box(label, theme)` | Simple labeled rectangle |
| `add_grid(labels, cols, theme, below=parent)` | Grid of labeled boxes — auto-sized cells, anchors + groups with parent |
| `add_group(label, label_position)` | Dashed grouping rectangle (`"above-center"` default) |
| `add_panel(title, content, width, below=parent)` | Auto-sized panel — anchors + groups with parent |
| `add_arrow(from, to, routing, label)` | Arrow with smart routing — label bound to arrow |
| `add_text(text)` | Standalone text |
| `position_below(component)` | Get (x, y) below a component |
| `position_right_of(component)` | Get (x, y) to the right |

### Automatic Grouping

The engine auto-groups related elements so they move together in Excalidraw:

| What | Grouping | Behavior |
|------|----------|----------|
| Card (body + text + icon + emoji) | `card-group` | Click card → selects entire card unit |
| Parent + children (via `below=`) | `spoke-group` | Click any part → selects card + grid/panel together |
| Arrow + label | Bound via `containerId` | Label sits on arrow, moves natively with it |

Nested selection: first click selects the outer group (spoke), double-click selects inner group (card only), triple-click selects individual element.

### Grid Auto-Sizing

`add_grid()` auto-calculates cell width from the longest label when `box_width` is not specified. This prevents text overflow.

```python
# Auto-sized: cells fit "brainstorm.md" without overflow
grid = d.add_grid(["brainstorm.md", "build.md"], cols=2, theme=Theme.PURPLE)

# Explicit override when you want fixed-width cells
grid = d.add_grid(["A", "B", "C"], cols=3, theme=Theme.GREEN, box_width=100)
```

### Card with Children Pattern

When a card has associated sub-items (grid, panel), **always use the `below` parameter**. This anchors children below the parent AND groups them so they move together.

```python
# Parent card
protocols = d.add_card("Protocols", subtitle="Cognitive Modes",
                       icon="🧠", theme=Theme.PURPLE, x=100, y=200)

# Children grid — anchored + grouped with parent in one call
proto_grid = d.add_grid(["brainstorm.md", "build.md"], cols=2,
                        theme=Theme.PURPLE, below=protocols)

# Panel — same pattern
info = d.add_panel("Details", "Line 1\nLine 2", below=protocols)
```

**Never** let auto-layout position grids independently — they will detach from their parent card. Always pass `below=parent_card`.

### Arrow Labels (Bound to Arrow)

Arrow labels are **bound to the arrow element** via `boundElements`/`containerId`. The label sits directly on the arrow path and moves with it natively — no manual positioning needed.

```python
# Label is bound to arrow — Excalidraw positions it on the path
d.add_arrow(hub, vault, from_side="bottom", to_side="top",
            label="persists to", theme=Theme.GREEN)

# Dashed arrow with label
d.add_arrow(scratch, vault, from_side="bottom", to_side="left",
            stroke_style="dashed", label="/wrap processes", theme=Theme.ORANGE)
```

### Arrow Routing

`add_arrow` supports smart routing via the `routing` parameter:

| Routing | When To Use | Auto-Detected? |
|---------|-------------|----------------|
| `"auto"` | Default — infers from connection geometry | Yes (default) |
| `"straight"` | Aligned vertical/horizontal connections | Yes, when aligned |
| `"z-mid"` | Offset vertical connections (current → target at different x) | Yes, for opposite unaligned |
| `"l-right-down"` | Horizontal first, then vertical | Yes, for perpendicular |
| `"l-down-right"` | Vertical first, then horizontal | Yes, for perpendicular |
| `"u-left"` | Feedback loops going left (same-side connections) | Yes, when from_side == to_side (left/top) |
| `"u-right"` | Feedback loops going right | Yes, when from_side == to_side (right/bottom) |

### Themes

| Theme | Use For |
|-------|---------|
| `Theme.BLUE` | Base classes, primary elements |
| `Theme.GREEN` | Node types, success states |
| `Theme.PURPLE` | Enums, data types |
| `Theme.ORANGE` | Edge types, relationships |
| `Theme.RED` | Hub elements, unions |
| `Theme.GRAY` | Grouping boxes, neutral |
| `Theme.AI` | AI/ML components |

### Positioning

The engine automatically prevents overlaps. For explicit positioning:

```python
# Position relative to another component
x, y = diagram.position_below(card, offset=40)
box = diagram.add_box("Label", x=x, y=y)

# Or specify absolute coordinates
box = diagram.add_box("Label", x=500, y=200)
```

## Critical Rules

### 1. Labels Need TWO Elements

```json
// Shape references text
{"id": "box", "boundElements": [{"type": "text", "id": "box-text"}]}

// Text references shape
{"id": "box-text", "containerId": "box", "text": "Label"}
```

**This applies to shapes AND arrows.** The layout engine handles this automatically.

### 2. Elbow Arrows Need THREE Properties

```json
{"roughness": 0, "roundness": null, "elbowed": true}
```

### 3. NO Diamond Shapes

Use styled rectangles instead:
- Decision: Orange `#ffd8a8`/`#e8590c` + dashed stroke
- Hub: Coral `#ffa8a8`/`#c92a2a` + strokeWidth: 3

### 4. Arrow Edge Points

| Edge | X | Y |
|------|---|---|
| Top | `x + width/2` | `y` |
| Bottom | `x + width/2` | `y + height` |
| Left | `x` | `y + height/2` |
| Right | `x + width` | `y + height/2` |

## Reference Files

Read before generating:

| File | Content |
|------|---------|
| `references/visual-polish.md` | **Read first** — Icon circles, text hierarchy, min font sizes |
| `references/patterns.md` | **Read second** — Pipelines, feedback loops, panels, grids, hub-and-spoke |
| `references/json-spec.md` | Element templates, required properties |
| `references/arrows.md` | Routing patterns, binding |
| `references/colors.md` | Semantic palettes |
| `references/layouts.md` | Diagram type templates |

## Output Format

Files are saved as `.excalidraw.md` (Obsidian-compatible):
- LZ-string compressed JSON
- `## Text Elements` section for search indexing
- YAML frontmatter

The `scripts/compress.py` handles this automatically.

## Quick Color Reference

| Element | Background | Stroke |
|---------|------------|--------|
| Process | `#a5d8ff` | `#1971c2` |
| Decision | `#ffd8a8` | `#e8590c` |
| Start/End | `#b2f2bb` | `#2f9e44` |
| Data | `#d0bfff` | `#7048e8` |
| External | `#ffc9c9` | `#e03131` |
| Hub | `#ffa8a8` | `#c92a2a` |

## Validation Checklist

**Technical (required):**
- [ ] Every shape with label has `boundElements` array
- [ ] Every text has `containerId` pointing to parent shape
- [ ] Arrow labels bound via `boundElements`/`containerId` (not floating text)
- [ ] Multi-point arrows have all three elbow properties
- [ ] No diamond shapes
- [ ] No duplicate IDs

**Visual (quality):**
- [ ] Key elements have icon circles with emoji
- [ ] Text uses title/subtitle hierarchy
- [ ] Colors from one hue family
- [ ] Rounded corners on rectangles
- [ ] Generous spacing (not cramped)
- [ ] All grids/panels use `below=parent` for anchoring

## Modification Flow

1. Read existing `.excalidraw.md`
2. Decompress JSON (use `scripts/compress.py --decompress`)
3. Modify elements
4. Validate and compress

## Example Usage

```bash
# Validate JSON
uv run .claude/skills/excalidraw/scripts/validate.py /tmp/diagram.json

# Generate .excalidraw.md
uv run .claude/skills/excalidraw/scripts/compress.py /tmp/diagram.json vault/canvas/my-diagram.excalidraw.md

# Decompress existing file
uv run .claude/skills/excalidraw/scripts/compress.py --decompress vault/canvas/existing.excalidraw.md /tmp/extracted.json
```
