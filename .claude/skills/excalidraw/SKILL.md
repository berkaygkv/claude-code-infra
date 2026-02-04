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

1. **Understand** — What to visualize, which type, key elements
2. **Confirm** — "Creating {type} showing {summary}. Output: vault/canvas/{slug}.excalidraw.md"
3. **Generate** — Build JSON following spec (read `references/json-spec.md`)
4. **Validate** — Run `uv run scripts/validate.py <json-file>`
5. **Compress** — Run `uv run scripts/compress.py <json-file> <output.excalidraw.md>`

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
| `references/visual-polish.md` | **Read first** — Icon circles, text hierarchy, polish techniques |
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
