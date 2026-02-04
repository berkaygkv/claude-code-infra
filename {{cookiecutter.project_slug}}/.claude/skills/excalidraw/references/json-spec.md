# Excalidraw JSON Specification

## File Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "kh-excalidraw-skill",
  "elements": [],
  "appState": {
    "gridSize": 20,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

## Element Types

| Type | Use For |
|------|---------|
| `rectangle` | Processes, components, containers |
| `ellipse` | Start/end points, users |
| `text` | Labels (must bind to shapes) |
| `arrow` | Connections |
| `line` | Separators, grouping |

**BANNED:** `diamond` — breaks in raw JSON

## Required Properties (All Elements)

```json
{
  "id": "unique-id",
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "width": 180,
  "height": 80,
  "angle": 0,
  "strokeColor": "#1971c2",
  "backgroundColor": "#a5d8ff",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": { "type": 3 },
  "seed": 1,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1,
  "link": null,
  "locked": false
}
```

## Text Binding (Critical)

Every labeled shape needs TWO elements:

### Shape with boundElements

```json
{
  "id": "box-1",
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "width": 180,
  "height": 80,
  "boundElements": [{ "type": "text", "id": "box-1-text" }]
}
```

### Text with containerId

```json
{
  "id": "box-1-text",
  "type": "text",
  "x": 105,
  "y": 125,
  "width": 170,
  "height": 30,
  "text": "Label Text",
  "fontSize": 16,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": "box-1",
  "originalText": "Label Text",
  "lineHeight": 1.25,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "boundElements": null,
  "roundness": null
}
```

### Text Positioning

```
text.x = shape.x + 5
text.y = shape.y + (shape.height - text.height) / 2
text.width = shape.width - 10
```

## Arrow Properties

```json
{
  "id": "arrow-1",
  "type": "arrow",
  "x": 190,
  "y": 180,
  "width": 0,
  "height": 50,
  "points": [[0, 0], [0, 50]],
  "strokeColor": "#1971c2",
  "strokeWidth": 2,
  "roughness": 0,
  "roundness": null,
  "elbowed": true,
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "startBinding": null,
  "endBinding": null
}
```

### Elbow Mode (Required for Multi-Point)

```json
{
  "roughness": 0,
  "roundness": null,
  "elbowed": true
}
```

### Width/Height Calculation

```
points = [[0, 0], [-200, 0], [-200, 80]]
width = max(abs(p[0]) for p in points) = 200
height = max(abs(p[1]) for p in points) = 80
```

## Grouping Rectangles

```json
{
  "id": "group-box",
  "type": "rectangle",
  "strokeColor": "#868e96",
  "backgroundColor": "transparent",
  "strokeStyle": "dashed",
  "roughness": 0,
  "roundness": null,
  "boundElements": null
}
```

## Complete Templates

### Rectangle with Label

```json
[
  {
    "id": "box-1",
    "type": "rectangle",
    "x": 100,
    "y": 100,
    "width": 180,
    "height": 80,
    "angle": 0,
    "strokeColor": "#1971c2",
    "backgroundColor": "#a5d8ff",
    "fillStyle": "solid",
    "strokeWidth": 2,
    "strokeStyle": "solid",
    "roughness": 1,
    "opacity": 100,
    "groupIds": [],
    "frameId": null,
    "roundness": { "type": 3 },
    "seed": 1,
    "version": 1,
    "versionNonce": 1,
    "isDeleted": false,
    "boundElements": [{ "type": "text", "id": "box-1-text" }],
    "updated": 1,
    "link": null,
    "locked": false
  },
  {
    "id": "box-1-text",
    "type": "text",
    "x": 105,
    "y": 125,
    "width": 170,
    "height": 30,
    "angle": 0,
    "strokeColor": "#1e1e1e",
    "backgroundColor": "transparent",
    "fillStyle": "solid",
    "strokeWidth": 1,
    "strokeStyle": "solid",
    "roughness": 0,
    "opacity": 100,
    "groupIds": [],
    "frameId": null,
    "roundness": null,
    "seed": 2,
    "version": 1,
    "versionNonce": 2,
    "isDeleted": false,
    "boundElements": null,
    "updated": 1,
    "link": null,
    "locked": false,
    "text": "Label",
    "fontSize": 16,
    "fontFamily": 1,
    "textAlign": "center",
    "verticalAlign": "middle",
    "baseline": 14,
    "containerId": "box-1",
    "originalText": "Label",
    "lineHeight": 1.25
  }
]
```

### Ellipse with Label

```json
[
  {
    "id": "start",
    "type": "ellipse",
    "x": 155,
    "y": 100,
    "width": 100,
    "height": 60,
    "angle": 0,
    "strokeColor": "#2f9e44",
    "backgroundColor": "#b2f2bb",
    "fillStyle": "solid",
    "strokeWidth": 2,
    "strokeStyle": "solid",
    "roughness": 1,
    "opacity": 100,
    "groupIds": [],
    "frameId": null,
    "roundness": { "type": 2 },
    "seed": 1,
    "version": 1,
    "versionNonce": 1,
    "isDeleted": false,
    "boundElements": [{ "type": "text", "id": "start-text" }],
    "updated": 1,
    "link": null,
    "locked": false
  },
  {
    "id": "start-text",
    "type": "text",
    "x": 180,
    "y": 117,
    "width": 50,
    "height": 25,
    "angle": 0,
    "strokeColor": "#1e1e1e",
    "backgroundColor": "transparent",
    "fillStyle": "solid",
    "strokeWidth": 1,
    "strokeStyle": "solid",
    "roughness": 0,
    "opacity": 100,
    "groupIds": [],
    "frameId": null,
    "roundness": null,
    "seed": 2,
    "version": 1,
    "versionNonce": 2,
    "isDeleted": false,
    "boundElements": null,
    "updated": 1,
    "link": null,
    "locked": false,
    "text": "Start",
    "fontSize": 16,
    "fontFamily": 1,
    "textAlign": "center",
    "verticalAlign": "middle",
    "baseline": 14,
    "containerId": "start",
    "originalText": "Start",
    "lineHeight": 1.25
  }
]
```

### Arrow (Vertical)

```json
{
  "id": "arrow-1",
  "type": "arrow",
  "x": 205,
  "y": 180,
  "width": 0,
  "height": 50,
  "angle": 0,
  "strokeColor": "#1971c2",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": null,
  "seed": 3,
  "version": 1,
  "versionNonce": 3,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1,
  "link": null,
  "locked": false,
  "points": [[0, 0], [0, 50]],
  "lastCommittedPoint": null,
  "startBinding": null,
  "endBinding": null,
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "elbowed": true
}
```
