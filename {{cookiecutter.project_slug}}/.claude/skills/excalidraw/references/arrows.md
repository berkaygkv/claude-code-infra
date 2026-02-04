# Arrow Routing Reference

## Edge Point Formulas

| Edge | X | Y |
|------|---|---|
| Top | `shape.x + shape.width/2` | `shape.y` |
| Bottom | `shape.x + shape.width/2` | `shape.y + shape.height` |
| Left | `shape.x` | `shape.y + shape.height/2` |
| Right | `shape.x + shape.width` | `shape.y + shape.height/2` |

## Elbow Mode (Required)

```json
{
  "roughness": 0,
  "roundness": null,
  "elbowed": true
}
```

All three properties required for 90-degree corners.

## Arrow Patterns

### Straight Down

```
Source bottom → Target top (aligned)

points = [[0, 0], [0, distance]]
width = 0
height = distance
```

### Straight Right

```
Source right → Target left (aligned)

points = [[0, 0], [distance, 0]]
width = distance
height = 0
```

### L-Shape (Right then Down)

```
Source right → Target top

dx = target_x - source_x
dy = target_y - source_y

points = [[0, 0], [dx, 0], [dx, dy]]
width = abs(dx)
height = abs(dy)
```

### L-Shape (Down then Right)

```
Source bottom → Target left

dx = target_x - source_x
dy = target_y - source_y

points = [[0, 0], [0, dy], [dx, dy]]
width = abs(dx)
height = abs(dy)
```

### U-Turn (Same Side)

```
Source right → Target right (below)

clearance = 50
dy = target_y - source_y
final_x = target_x - source_x

points = [[0, 0], [clearance, 0], [clearance, dy], [final_x, dy]]
width = max(abs(clearance), abs(final_x))
height = abs(dy)
```

## Worked Examples

### Example 1: Vertical (Bottom to Top)

```
Source: x=100, y=100, width=180, height=80
Target: x=100, y=230, width=180, height=80

source_bottom = (100 + 90, 100 + 80) = (190, 180)
target_top = (100 + 90, 230) = (190, 230)

Arrow:
  x = 190
  y = 180
  points = [[0, 0], [0, 50]]
  width = 0
  height = 50
```

### Example 2: L-Shape (Right then Down)

```
Source: x=100, y=100, width=180, height=80
Target: x=320, y=230, width=180, height=80

source_right = (100 + 180, 100 + 40) = (280, 140)
target_top = (320 + 90, 230) = (410, 230)

dx = 410 - 280 = 130
dy = 230 - 140 = 90

Arrow:
  x = 280
  y = 140
  points = [[0, 0], [130, 0], [130, 90]]
  width = 130
  height = 90
```

### Example 3: Fan-Out (One to Many)

```
Source: x=200, y=100, width=180, height=80
Targets at y=230: x=100, x=320, x=540

source_bottom = (200 + 90, 180) = (290, 180)

Arrow to Target 1:
  x = 290, y = 180
  dx = (100 + 90) - 290 = -100
  dy = 230 - 180 = 50
  points = [[0, 0], [-100, 0], [-100, 50]]
  width = 100, height = 50

Arrow to Target 2:
  x = 290, y = 180
  points = [[0, 0], [0, 50]]
  width = 0, height = 50

Arrow to Target 3:
  x = 290, y = 180
  dx = (540 + 90) - 290 = 340
  points = [[0, 0], [340, 0], [340, 50]]
  width = 340, height = 50
```

## Staggering Multiple Arrows

When N arrows leave from same edge:

```
For N arrows from bottom edge:
  positions = []
  for i in range(N):
    pct = 0.2 + (0.6 * i / (N - 1))
    x = shape.x + shape.width * pct
    positions.append(x)

2 arrows: 20%, 80%
3 arrows: 20%, 50%, 80%
4 arrows: 20%, 40%, 60%, 80%
```

## Width/Height Calculation

```
points = [[0, 0], [-200, 0], [-200, 80]]

width = max(abs(0), abs(-200), abs(-200)) = 200
height = max(abs(0), abs(0), abs(80)) = 80
```

## Arrow Bindings (Optional)

```json
{
  "startBinding": {
    "elementId": "source-id",
    "focus": 0,
    "gap": 1,
    "fixedPoint": [0.5, 1]
  },
  "endBinding": {
    "elementId": "target-id",
    "focus": 0,
    "gap": 1,
    "fixedPoint": [0.5, 0]
  }
}
```

### fixedPoint Values

| Position | Value |
|----------|-------|
| Top center | `[0.5, 0]` |
| Bottom center | `[0.5, 1]` |
| Left center | `[0, 0.5]` |
| Right center | `[1, 0.5]` |

## Bidirectional

```json
{
  "startArrowhead": "arrow",
  "endArrowhead": "arrow"
}
```

Arrowhead options: `null`, `"arrow"`, `"bar"`, `"dot"`, `"triangle"`
