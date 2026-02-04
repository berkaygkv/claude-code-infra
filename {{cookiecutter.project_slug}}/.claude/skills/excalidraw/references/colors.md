# Color Palettes

## Default (Sense-Making)

| Element | Background | Stroke |
|---------|------------|--------|
| Process/Action | `#a5d8ff` | `#1971c2` |
| Decision | `#ffd8a8` | `#e8590c` |
| Start/End | `#b2f2bb` | `#2f9e44` |
| Data/Storage | `#d0bfff` | `#7048e8` |
| External | `#ffc9c9` | `#e03131` |
| Highlight | `#ffec99` | `#f08c00` |
| Neutral | `#e9ecef` | `#495057` |
| Hub/Central | `#ffa8a8` | `#c92a2a` |
| User/Actor | `#e7f5ff` | `#1971c2` |

## System Diagram

| Component | Background | Stroke |
|-----------|------------|--------|
| Frontend | `#a5d8ff` | `#1971c2` |
| Backend/API | `#d0bfff` | `#7048e8` |
| Database | `#b2f2bb` | `#2f9e44` |
| Cache | `#ffe8cc` | `#fd7e14` |
| Queue | `#fff3bf` | `#fab005` |
| External | `#ffc9c9` | `#e03131` |
| AI/ML | `#e599f7` | `#9c36b5` |

## Mind Map Levels

| Level | Background | Stroke |
|-------|------------|--------|
| Center | `#ffa8a8` | `#c92a2a` |
| Level 1 | `#a5d8ff` | `#1971c2` |
| Level 2 | `#d0bfff` | `#7048e8` |
| Level 3 | `#b2f2bb` | `#2f9e44` |
| Level 4 | `#ffec99` | `#f08c00` |

## Timeline

| Element | Background | Stroke |
|---------|------------|--------|
| Phase | `#a5d8ff` | `#1971c2` |
| Current | `#ffa8a8` | `#c92a2a` |
| Milestone | `#b2f2bb` | `#2f9e44` |
| Future | `#e9ecef` | `#495057` |
| Deadline | `#ffc9c9` | `#e03131` |

## Stroke Styles

| Style | Properties |
|-------|------------|
| Normal | `strokeStyle: "solid"`, `strokeWidth: 2` |
| Decision | `strokeStyle: "dashed"`, `strokeWidth: 2` |
| Hub | `strokeStyle: "solid"`, `strokeWidth: 3` |
| Group | `strokeStyle: "dashed"`, `strokeWidth: 1` |

## Text Colors

| Context | Color |
|---------|-------|
| Labels | `#1e1e1e` |
| Annotations | `#868e96` |
| Group labels | `#495057` |

## Arrow Colors

Match arrow stroke to destination element, or use neutral `#495057` for all arrows.

## Example: Decision Box

```json
{
  "strokeColor": "#e8590c",
  "backgroundColor": "#ffd8a8",
  "strokeWidth": 2,
  "strokeStyle": "dashed"
}
```

## Example: Hub/Central

```json
{
  "strokeColor": "#c92a2a",
  "backgroundColor": "#ffa8a8",
  "strokeWidth": 3,
  "strokeStyle": "solid"
}
```

## Example: Group Boundary

```json
{
  "strokeColor": "#868e96",
  "backgroundColor": "transparent",
  "strokeWidth": 1,
  "strokeStyle": "dashed"
}
```
