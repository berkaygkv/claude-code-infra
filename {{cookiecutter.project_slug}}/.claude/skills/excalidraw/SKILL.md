---
name: excalidraw
description: Generate Excalidraw diagrams for visual sense-making. Use when user asks to visualize, diagram, map out, sketch, draw, or create flowcharts/mind maps/timelines/system diagrams. Outputs Obsidian-compatible .excalidraw.md files.
allowed-tools: Bash(uv run *)
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
**You MUST still run validate + compress (steps 5-6 above).** Never write `.excalidraw.md` directly.

---

## Layout Engine (Recommended)

The layout engine (`scripts/layout.py`) prevents positioning bugs automatically.

### Quick Example

```python
import sys
sys.path.insert(0, ".claude/skills/excalidraw/scripts")
from layout import Diagram, Theme

diagram = Diagram(start_x=100, start_y=100)

# Add elements - positions calculated automatically
card = diagram.add_card("Title", subtitle="desc", icon="📦", theme=Theme.BLUE)
grid = diagram.add_grid(["A", "B", "C", "D"], cols=2, theme=Theme.GREEN)
diagram.add_arrow(card, grid, from_side="bottom", to_side="top")

diagram.to_json("output.json")
```

### Available Methods

| Method | Description |
|--------|-------------|
| `add_card(title, subtitle, icon, theme)` | Card with icon circle (text auto-offset below icon) |
| `add_box(label, theme)` | Simple labeled rectangle |
| `add_grid(labels, cols, theme, center_last_row)` | Grid of labeled boxes (last row auto-centered) |
| `add_group(label, label_position)` | Dashed grouping rectangle (`"above-center"` default) |
| `add_panel(title, content, width)` | Auto-sized panel with title + body text |
| `add_arrow(from, to, routing, label)` | Arrow with smart routing and optional label |
| `add_text(text)` | Standalone text |
| `position_below(component)` | Get (x, y) below a component |
| `position_right_of(component)` | Get (x, y) to the right |

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

Arrow labels: `label="text"` auto-positions text at the arrow midpoint.

```python
# Feedback loop with label (auto U-shape)
d.add_arrow(store, context, from_side="left", to_side="left",
            stroke_style="dashed", label="Existing entities")
```

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

**Never use `label` property — it doesn't work in raw JSON.**

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
| `references/patterns.md` | **Read second** — Pipelines, feedback loops, panels, grids |
| `references/json-spec.md` | Element templates, required properties |
| `references/arrows.md` | Routing patterns, binding |
| `references/colors.md` | Semantic palettes |
| `references/layouts.md` | Diagram type templates |

## Output Format

**HARD CONSTRAINT:** NEVER write `.excalidraw.md` files by hand. The Obsidian Excalidraw plugin requires a specific internal format (LZ-string compressed JSON, `## Text Elements` section, `compressed-json` code blocks) that cannot be reliably reproduced manually. Manually written wrappers (frontmatter + fenced JSON) will fail to open.

**Always use the pipeline:**
1. Write raw JSON to a temp file (e.g., `/tmp/diagram.json`)
2. Validate: `uv run .claude/skills/excalidraw/scripts/validate.py /tmp/diagram.json`
3. Compress: `uv run .claude/skills/excalidraw/scripts/compress.py /tmp/diagram.json vault/canvas/{slug}.excalidraw.md`

The `compress.py` script generates the correct Obsidian-compatible `.excalidraw.md` with:
- YAML frontmatter (`excalidraw-plugin: parsed`)
- `## Text Elements` section for search indexing
- LZ-string compressed drawing data in `compressed-json` code blocks

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

**Output (critical):**
- [ ] JSON written to temp file first (NOT directly to `.excalidraw.md`)
- [ ] `validate.py` run with zero errors
- [ ] `compress.py` used to generate final `.excalidraw.md`

**Technical (required):**
- [ ] Every shape with label has `boundElements` array
- [ ] Every text has `containerId` pointing to parent shape
- [ ] Multi-point arrows have all three elbow properties
- [ ] No diamond shapes
- [ ] No duplicate IDs

**Visual (quality):**
- [ ] Key elements have icon circles with emoji
- [ ] Text uses title/subtitle hierarchy
- [ ] Colors from one hue family
- [ ] Rounded corners on rectangles
- [ ] Generous spacing (not cramped)

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
