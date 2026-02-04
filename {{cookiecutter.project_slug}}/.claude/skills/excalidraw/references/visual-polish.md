# Visual Polish Reference

Techniques to make diagrams visually impressive.

## Layered Elements

Stack elements for visual hierarchy:

```
┌─────────────────────────┐
│      ┌───────┐          │
│      │ ICON  │          │  ← Icon circle overlays rectangle
│      └───────┘          │
│                         │
│      TITLE              │  ← Bold/larger text
│      Subtitle           │  ← Smaller/muted text
└─────────────────────────┘
```

### Icon Circle on Shape

```json
[
  {
    "id": "card-1",
    "type": "rectangle",
    "x": 100,
    "y": 100,
    "width": 200,
    "height": 120,
    "backgroundColor": "#d0bfff",
    "strokeColor": "#7048e8",
    "roundness": { "type": 3 }
  },
  {
    "id": "icon-circle",
    "type": "ellipse",
    "x": 165,
    "y": 85,
    "width": 70,
    "height": 70,
    "backgroundColor": "#7048e8",
    "strokeColor": "#5f3dc4",
    "strokeWidth": 3
  },
  {
    "id": "icon-text",
    "type": "text",
    "x": 185,
    "y": 105,
    "text": "📣",
    "fontSize": 28,
    "containerId": null
  }
]
```

Position icon circle to overlap: `icon.y = card.y - icon.height/2 + 15`

## Text Hierarchy

Use different sizes and colors for title vs subtitle:

```json
{
  "id": "title",
  "type": "text",
  "text": "DISTRIBUTION",
  "fontSize": 20,
  "fontFamily": 1,
  "strokeColor": "#5f3dc4"
}
```

```json
{
  "id": "subtitle",
  "type": "text",
  "text": "Multi-Channel Reach",
  "fontSize": 14,
  "fontFamily": 1,
  "strokeColor": "#7048e8"
}
```

### Multi-Line in Single Text Element

```json
{
  "text": "DISTRIBUTION\nMulti-Channel Reach",
  "fontSize": 16,
  "textAlign": "center"
}
```

## Hand-Drawn Aesthetic

### Roughness Levels

| Value | Effect | Use For |
|-------|--------|---------|
| 0 | Clean/precise | Technical diagrams |
| 1 | Slight sketch | Default, balanced |
| 2 | More sketchy | Casual/brainstorm |

```json
{
  "roughness": 1,
  "strokeWidth": 2
}
```

### Rounded Corners

```json
{
  "roundness": { "type": 3 }
}
```

Type 3 gives natural rounded corners.

## Color Coordination

### Monochromatic Schemes

Pick one hue, vary saturation/lightness:

**Purple Theme:**
- Background: `#d0bfff` (light)
- Stroke: `#7048e8` (medium)
- Accent: `#5f3dc4` (dark)

**Blue Theme:**
- Background: `#a5d8ff`
- Stroke: `#1971c2`
- Accent: `#1864ab`

**Green Theme:**
- Background: `#b2f2bb`
- Stroke: `#2f9e44`
- Accent: `#237032`

### Icon Circle Colors

Make icon circle darker than card:
```
card.backgroundColor = light shade
icon.backgroundColor = medium shade
icon.strokeColor = dark shade
```

## Emoji Icons

Use emoji as visual anchors:

| Concept | Emoji |
|---------|-------|
| Distribution | 📣 📢 🔊 |
| Data | 📊 📈 💾 |
| User | 👤 👥 🧑‍💻 |
| Settings | ⚙️ 🔧 🛠️ |
| Security | 🔒 🛡️ 🔐 |
| AI/ML | 🤖 🧠 ✨ |
| Cloud | ☁️ 🌐 |
| Database | 🗄️ 💿 |
| Alert | ⚠️ 🚨 |
| Success | ✅ 🎯 |
| Money | 💰 💵 |
| Time | ⏰ 📅 |
| Location | 📍 🗺️ |
| Communication | 💬 📧 📱 |

### Emoji Text Element

```json
{
  "id": "emoji-icon",
  "type": "text",
  "x": 185,
  "y": 105,
  "width": 30,
  "height": 30,
  "text": "📣",
  "fontSize": 28,
  "fontFamily": 1,
  "textAlign": "center",
  "containerId": null
}
```

## Card-Style Elements

Modern card look with shadow effect (via offset duplicate):

```json
[
  {
    "id": "shadow",
    "type": "rectangle",
    "x": 105,
    "y": 105,
    "width": 200,
    "height": 120,
    "backgroundColor": "#00000022",
    "strokeColor": "transparent",
    "strokeWidth": 0
  },
  {
    "id": "card",
    "type": "rectangle",
    "x": 100,
    "y": 100,
    "width": 200,
    "height": 120,
    "backgroundColor": "#d0bfff",
    "strokeColor": "#7048e8"
  }
]
```

Shadow offset: 5px right, 5px down, semi-transparent black.

## Arrows with Style

### Thicker for Emphasis

```json
{
  "strokeWidth": 3,
  "strokeColor": "#868e96"
}
```

### Dashed for Optional/Async

```json
{
  "strokeStyle": "dashed"
}
```

### Colored by Flow Type

| Flow | Color |
|------|-------|
| Primary | `#1971c2` |
| Secondary | `#868e96` |
| Error | `#e03131` |
| Success | `#2f9e44` |

## Spacing for Visual Balance

### Generous Padding

- Card internal padding: 20-30px
- Between elements: 60-80px (not cramped)
- Icon overlap: 10-20px into card

### Alignment

Align elements to grid:
- x positions: 100, 350, 600
- y positions: 100, 270, 440

## Complete Card Example

```json
[
  {
    "id": "card-distribution",
    "type": "rectangle",
    "x": 100,
    "y": 100,
    "width": 200,
    "height": 130,
    "angle": 0,
    "strokeColor": "#7048e8",
    "backgroundColor": "#d0bfff",
    "fillStyle": "solid",
    "strokeWidth": 2,
    "strokeStyle": "solid",
    "roughness": 1,
    "opacity": 100,
    "roundness": { "type": 3 },
    "boundElements": [{ "type": "text", "id": "card-distribution-text" }]
  },
  {
    "id": "card-distribution-text",
    "type": "text",
    "x": 105,
    "y": 155,
    "width": 190,
    "height": 50,
    "text": "DISTRIBUTION\nMulti-Channel Reach",
    "fontSize": 16,
    "fontFamily": 1,
    "textAlign": "center",
    "verticalAlign": "middle",
    "containerId": "card-distribution",
    "strokeColor": "#5f3dc4"
  },
  {
    "id": "icon-circle-distribution",
    "type": "ellipse",
    "x": 165,
    "y": 75,
    "width": 70,
    "height": 70,
    "strokeColor": "#5f3dc4",
    "backgroundColor": "#7048e8",
    "strokeWidth": 3,
    "roughness": 1,
    "roundness": { "type": 2 },
    "boundElements": [{ "type": "text", "id": "icon-emoji-distribution" }]
  },
  {
    "id": "icon-emoji-distribution",
    "type": "text",
    "x": 185,
    "y": 95,
    "width": 30,
    "height": 30,
    "text": "📣",
    "fontSize": 28,
    "textAlign": "center",
    "verticalAlign": "middle",
    "containerId": "icon-circle-distribution",
    "strokeColor": "#ffffff"
  }
]
```

## Quick Polish Checklist

- [ ] Consistent color theme (one hue family)
- [ ] Icon circles on key elements
- [ ] Multi-line text with title/subtitle
- [ ] Generous spacing (not cramped)
- [ ] Rounded corners (`roundness: { type: 3 }`)
- [ ] Slight roughness (1) for hand-drawn feel
- [ ] Aligned to grid
- [ ] Arrows match element colors
