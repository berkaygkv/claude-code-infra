# Diagram Layouts

## Spacing Constants

| Constant | Value |
|----------|-------|
| Row gap | 130px |
| Column gap | 220px |
| Element width | 180px |
| Element height | 80px |
| Arrow gap | 50px |

## Flowchart (Vertical)

```
     Col 0 (x=100)

Row 0  [ Start ]      y=100   (ellipse, green)
          |
Row 1  [ Process ]    y=230   (rect, blue)
          |
Row 2  [ Decision ]   y=360   (rect, orange dashed)
         / \
Row 3  [Yes] [No]     y=490   (rect, blue)
          |
Row 4  [ End ]        y=620   (ellipse, green)
```

### Grid Positions

```
Rows:  100, 230, 360, 490, 620
Cols:  100, 320, 540
```

### Branch Pattern

Decision at Col 0 → Yes continues at Col 0, No goes to Col 1

## System Diagram (Grid)

```
     Col 0    Col 1    Col 2
     x=100    x=320    x=540

Row 0  [User]                  y=100
         |
Row 1  [Frontend]  [Admin]     y=230
         |
Row 2  [API]     [Auth]        y=380
         |
Row 3  [DB]      [Cache]       y=530
```

### Hub-and-Spoke

```
           [N]
            |
   [W] --- [HUB] --- [E]
            |
           [S]

Center: (400, 300)
Radius: 200px

N:  (400, 100)
E:  (600, 300)
S:  (400, 500)
W:  (200, 300)
```

## Mind Map (Radial)

```
        [Branch 1]
            |
[Branch 2] - [CENTER] - [Branch 3]
            |
        [Branch 4]

Center: (400, 300), size: 200x100

Level 1 positions:
  Right: (650, 275)
  Left:  (100, 275)
  Up:    (350, 100)
  Down:  (350, 450)

Level 2: offset 150px from parent
```

### Element Sizes by Level

| Level | Size |
|-------|------|
| Center | 200x100 |
| L1 | 160x70 |
| L2 | 140x60 |
| L3 | 120x50 |

## Sequence Diagram (Columns)

```
  Actor 1    Actor 2    Actor 3
  x=100      x=300      x=500
    |          |          |
    |--------->|          |  y=150 (message)
    |          |--------->|  y=220
    |          |<---------|  y=290 (response)
    |<---------|          |  y=360
```

### Positions

```
Actors: y=50, height=60
Columns: x=100, 300, 500 (200px spacing)
Messages: y starts at 150, 70px spacing
```

### Lifeline

Dashed vertical line from actor bottom:
```json
{
  "type": "line",
  "strokeStyle": "dashed",
  "strokeColor": "#868e96",
  "points": [[0, 0], [0, 400]]
}
```

## Timeline (Horizontal)

```
[Phase 1] --> [Phase 2] --> [Phase 3] --> [Phase 4]
   |             |             |
 Start       Milestone      Current
```

### Positions

```
Phases: y=200, x=100, 350, 600, 850 (250px spacing)
Milestones: y=350, below phases
Phase size: 180x80
Milestone size: 120x50
```

### Timeline Line (Optional)

```json
{
  "type": "line",
  "x": 190,
  "y": 240,
  "points": [[0, 0], [760, 0]],
  "strokeColor": "#868e96"
}
```

## Size Guidelines

| Type | Max Elements | Max Arrows |
|------|--------------|------------|
| Flowchart | 15-20 | 20-25 |
| System | 20-30 | 30-40 |
| Mind Map | 15-25 | 15-25 |
| Sequence | 5 actors | 15-20 |
| Timeline | 8-10 | 10-15 |

## Minimal Templates

### Flowchart (3 steps)

```
1 start + 1 process + 1 end
3 shapes + 3 texts + 2 arrows = 8 elements
```

### System (3 components)

```
3 rectangles + 3 texts + 2-3 arrows = 9-10 elements
```

### Mind Map (1+4)

```
1 center + 4 branches
5 rectangles + 5 texts + 4 lines = 14 elements
```

### Sequence (2 actors)

```
2 actors + 2 lifelines + 3 messages = 7 elements
```

### Timeline (3 phases)

```
3 phases + 2 arrows + 1 line = 6 elements
```
