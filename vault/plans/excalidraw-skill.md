---
type: plan
status: complete
created: 2026-02-04
project: kh
topic: excalidraw-skill
---

# Excalidraw Skill Plan

## Summary

Create a proper Claude Code skill that produces Obsidian-compatible Excalidraw diagrams with validation and compression.

## Decisions (LOCKED)

| Decision | Detail |
|----------|--------|
| Diagram types | Flowchart, System, Mind Map, Sequence, Timeline |
| Output format | `.excalidraw.md` (Obsidian-compatible, LZ-string compressed) |
| Output location | `vault/canvas/{slug}.excalidraw.md` |
| Skill location | `.claude/skills/excalidraw/` |
| Validation | Script-based (`scripts/validate.py`) |
| Compression | Script-based (`scripts/compress.py`) |

## File Structure (Implemented)

```
.claude/skills/excalidraw/
├── SKILL.md                    # Main skill file (concise)
├── scripts/
│   ├── validate.py             # Validates JSON before writing
│   └── compress.py             # LZ-string compression for Obsidian
└── references/
    ├── json-spec.md            # Element templates, required properties
    ├── arrows.md               # Routing patterns, bindings
    ├── colors.md               # Semantic color palettes
    └── layouts.md              # Diagram type layouts
```

## Workflow

### Generation Flow

1. **UNDERSTAND** — What to visualize, which type, key elements
2. **CONFIRM** — "Creating {type} showing {summary}. Output: vault/canvas/{slug}.excalidraw.md"
3. **GENERATE** — Build JSON following spec (read references)
4. **VALIDATE** — `python scripts/validate.py <json-file>`
5. **COMPRESS** — `python scripts/compress.py <json-file> <output.excalidraw.md>`

### Modification Flow

1. **DECOMPRESS** — `python scripts/compress.py --decompress <file> /tmp/edit.json`
2. **MODIFY** — Edit JSON
3. **VALIDATE** — Run validation
4. **COMPRESS** — Write back

## Critical Technical Rules

### Labels (Two-Element Binding)
- Shape: `boundElements: [{ id: "text-id", type: "text" }]`
- Text: `containerId: "shape-id"`
- Never use `label` property

### Arrows (Elbow Configuration)
```json
{"roughness": 0, "roundness": null, "elbowed": true}
```

### Banned
- Diamond shapes (broken in raw JSON)

## Implementation Complete

- [x] SKILL.md with concise instructions
- [x] scripts/validate.py for pre-write validation
- [x] scripts/compress.py for LZ-string compression + Obsidian format
- [x] references/json-spec.md with element templates
- [x] references/arrows.md with routing patterns
- [x] references/colors.md with semantic palettes
- [x] references/layouts.md with diagram layouts
- [x] Round-trip compression test passed

## Key Improvements Over Initial Attempt

1. **Proper skill location**: `.claude/skills/` not `.claude/commands/`
2. **Obsidian compatibility**: LZ-string compression into `.excalidraw.md` format
3. **Validation script**: Catches silent rendering failures before write
4. **Progressive disclosure**: SKILL.md under 100 lines, details in references/
5. **Text Elements section**: For Obsidian search indexing

## Sources

- [Obsidian Excalidraw Plugin - File Formats](https://deepwiki.com/zsviczian/obsidian-excalidraw-plugin/3.1-file-formats-and-storage)
- [zsviczian/obsidian-excalidraw-plugin](https://github.com/zsviczian/obsidian-excalidraw-plugin)
- [ooiyeefei/ccc excalidraw skill](https://github.com/ooiyeefei/ccc/tree/main/skills/excalidraw)
