#!/usr/bin/env python3
"""
Layout engine for Excalidraw diagrams.

Provides automatic positioning to prevent overlaps and layout errors.

Usage:
    from layout import Diagram, Theme

    diagram = Diagram()

    # Add elements with automatic positioning
    card = diagram.card("BaseNode", subtitle="id, name", icon="📦", theme=Theme.BLUE)

    # Create grids
    nodes = diagram.grid(["A", "B", "C", "D"], cols=2, theme=Theme.GREEN)

    # Export
    diagram.to_json("output.json")

Key features:
- Automatic coordinate calculation
- Collision-free positioning
- Component builders (cards, grids, groups)
- Consistent spacing and alignment
"""

from __future__ import annotations
import json
import uuid
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


# =============================================================================
# Color Themes
# =============================================================================

@dataclass(frozen=True)
class ColorTheme:
    """Color palette for elements."""
    background: str
    stroke: str
    text: str
    icon_bg: str
    icon_stroke: str


class Theme:
    """Predefined color themes."""
    BLUE = ColorTheme(
        background="#a5d8ff",
        stroke="#1971c2",
        text="#1864ab",
        icon_bg="#1971c2",
        icon_stroke="#1864ab",
    )
    GREEN = ColorTheme(
        background="#b2f2bb",
        stroke="#2f9e44",
        text="#237032",
        icon_bg="#2f9e44",
        icon_stroke="#237032",
    )
    PURPLE = ColorTheme(
        background="#d0bfff",
        stroke="#7048e8",
        text="#5f3dc4",
        icon_bg="#7048e8",
        icon_stroke="#5f3dc4",
    )
    ORANGE = ColorTheme(
        background="#ffd8a8",
        stroke="#e8590c",
        text="#c2410c",
        icon_bg="#e8590c",
        icon_stroke="#c2410c",
    )
    RED = ColorTheme(
        background="#ffa8a8",
        stroke="#c92a2a",
        text="#c92a2a",
        icon_bg="#c92a2a",
        icon_stroke="#a51111",
    )
    GRAY = ColorTheme(
        background="#e9ecef",
        stroke="#868e96",
        text="#495057",
        icon_bg="#868e96",
        icon_stroke="#495057",
    )
    AI = ColorTheme(
        background="#e599f7",
        stroke="#9c36b5",
        text="#862e9c",
        icon_bg="#be4bdb",
        icon_stroke="#9c36b5",
    )


# =============================================================================
# Bounding Box
# =============================================================================

@dataclass
class BBox:
    """Axis-aligned bounding box."""
    x: float
    y: float
    width: float
    height: float

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height

    @property
    def center_x(self) -> float:
        return self.x + self.width / 2

    @property
    def center_y(self) -> float:
        return self.y + self.height / 2

    def overlaps(self, other: BBox, margin: float = 0) -> bool:
        """Check if this bbox overlaps with another (with optional margin)."""
        return not (
            self.right + margin < other.x or
            other.right + margin < self.x or
            self.bottom + margin < other.y or
            other.bottom + margin < self.y
        )

    def expanded(self, margin: float) -> BBox:
        """Return a new bbox expanded by margin on all sides."""
        return BBox(
            x=self.x - margin,
            y=self.y - margin,
            width=self.width + 2 * margin,
            height=self.height + 2 * margin,
        )


# =============================================================================
# Element Builders
# =============================================================================

def _uid(prefix: str = "el") -> str:
    """Generate a unique element ID."""
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def _base_props(
    el_id: str,
    el_type: str,
    x: float,
    y: float,
    width: float,
    height: float,
) -> dict:
    """Base properties required by all elements."""
    return {
        "id": el_id,
        "type": el_type,
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "angle": 0,
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "seed": hash(el_id) % 100000,
        "version": 1,
        "versionNonce": hash(el_id) % 100000,
        "isDeleted": False,
        "updated": 1,
        "link": None,
        "locked": False,
    }


def make_rectangle(
    x: float,
    y: float,
    width: float,
    height: float,
    theme: ColorTheme,
    el_id: str | None = None,
    stroke_width: int = 2,
    stroke_style: str = "solid",
    rounded: bool = True,
) -> dict:
    """Create a rectangle element."""
    el_id = el_id or _uid("rect")
    el = _base_props(el_id, "rectangle", x, y, width, height)
    el.update({
        "strokeColor": theme.stroke,
        "backgroundColor": theme.background,
        "strokeWidth": stroke_width,
        "strokeStyle": stroke_style,
        "roundness": {"type": 3} if rounded else None,
        "boundElements": None,
    })
    return el


def make_ellipse(
    x: float,
    y: float,
    width: float,
    height: float,
    theme: ColorTheme,
    el_id: str | None = None,
) -> dict:
    """Create an ellipse element."""
    el_id = el_id or _uid("ellipse")
    el = _base_props(el_id, "ellipse", x, y, width, height)
    el.update({
        "strokeColor": theme.icon_stroke,
        "backgroundColor": theme.icon_bg,
        "roundness": {"type": 2},
        "boundElements": None,
    })
    return el


def make_text(
    x: float,
    y: float,
    text: str,
    font_size: int = 16,
    color: str = "#1e1e1e",
    align: str = "center",
    vertical_align: str = "middle",
    container_id: str | None = None,
    el_id: str | None = None,
) -> dict:
    """Create a text element."""
    el_id = el_id or _uid("text")
    lines = text.split("\n")
    height = len(lines) * font_size * 1.25
    # Estimate width based on character count
    max_chars = max(len(line) for line in lines) if lines else 0
    width = max_chars * font_size * 0.6

    el = _base_props(el_id, "text", x, y, width, height)
    el.update({
        "strokeColor": color,
        "backgroundColor": "transparent",
        "strokeWidth": 1,
        "roughness": 0,
        "roundness": None,
        "boundElements": None,
        "text": text,
        "fontSize": font_size,
        "fontFamily": 1,
        "textAlign": align,
        "verticalAlign": vertical_align,
        "baseline": int(font_size * 0.875),
        "containerId": container_id,
        "originalText": text,
        "lineHeight": 1.25,
    })
    return el


def make_arrow(
    start_x: float,
    start_y: float,
    points: list[tuple[float, float]],
    theme: ColorTheme | None = None,
    stroke_color: str | None = None,
    stroke_style: str = "solid",
    el_id: str | None = None,
) -> dict:
    """Create an arrow element."""
    el_id = el_id or _uid("arrow")
    color = stroke_color or (theme.stroke if theme else "#495057")

    # Calculate bounding box from points
    all_x = [p[0] for p in points]
    all_y = [p[1] for p in points]
    width = max(abs(x) for x in all_x)
    height = max(abs(y) for y in all_y)

    el = _base_props(el_id, "arrow", start_x, start_y, width, height)
    el.update({
        "strokeColor": color,
        "backgroundColor": "transparent",
        "strokeStyle": stroke_style,
        "roughness": 0,
        "roundness": None,
        "boundElements": None,
        "points": [list(p) for p in points],
        "lastCommittedPoint": None,
        "startBinding": None,
        "endBinding": None,
        "startArrowhead": None,
        "endArrowhead": "arrow",
        "elbowed": True,
    })
    return el


# =============================================================================
# Component Builders
# =============================================================================

@dataclass
class Component:
    """A group of elements that form a logical unit."""
    elements: list[dict]
    bbox: BBox

    def shift(self, dx: float, dy: float) -> Component:
        """Return a new component shifted by (dx, dy)."""
        new_elements = []
        for el in self.elements:
            new_el = el.copy()
            new_el["x"] = el["x"] + dx
            new_el["y"] = el["y"] + dy
            new_elements.append(new_el)
        new_bbox = BBox(
            x=self.bbox.x + dx,
            y=self.bbox.y + dy,
            width=self.bbox.width,
            height=self.bbox.height,
        )
        return Component(new_elements, new_bbox)


def labeled_box(
    x: float,
    y: float,
    width: float,
    height: float,
    label: str,
    theme: ColorTheme,
    font_size: int = 14,
) -> Component:
    """Create a rectangle with centered label."""
    box_id = _uid("box")
    text_id = _uid("text")

    box = make_rectangle(x, y, width, height, theme, el_id=box_id)
    box["boundElements"] = [{"type": "text", "id": text_id}]

    # Center text in box
    text = make_text(
        x=x + 5,
        y=y + (height - font_size * 1.25) / 2,
        text=label,
        font_size=font_size,
        color=theme.text,
        container_id=box_id,
        el_id=text_id,
    )
    text["width"] = width - 10
    text["height"] = font_size * 1.25 * len(label.split("\n"))

    return Component(
        elements=[box, text],
        bbox=BBox(x, y, width, height),
    )


def card_with_icon(
    x: float,
    y: float,
    width: float,
    height: float,
    title: str,
    subtitle: str | None = None,
    icon: str | None = None,
    theme: ColorTheme = Theme.BLUE,
    icon_size: int = 50,
    icon_overlap: float = 0.4,  # How much of icon overlaps into card (0-1)
) -> Component:
    """Create a card with optional icon circle and title/subtitle.

    The icon circle is centered horizontally on the card and overlaps
    the top edge. The emoji is centered within the circle.

    Args:
        x, y: Top-left corner of the card body
        width, height: Dimensions of the card body
        title: Main text
        subtitle: Secondary text (shown below title)
        icon: Emoji character for the icon circle
        theme: Color theme
        icon_size: Diameter of the icon circle
        icon_overlap: Fraction of icon that overlaps into the card (0.4 = 40%)
    """
    elements = []

    # Group all card elements so they move together in Excalidraw
    card_group_id = _uid("card-group")

    # --- Card body FIRST (renders behind icon) ---
    card_id = _uid("card")
    text_id = _uid("card-text")

    card = make_rectangle(x, y, width, height, theme, el_id=card_id)
    card["boundElements"] = [{"type": "text", "id": text_id}]
    card["groupIds"] = [card_group_id]

    # Text content
    text_content = title
    if subtitle:
        text_content = f"{title}\n{subtitle}"

    # When icon is present, prepend a blank line to push visible text
    # below the icon overlap zone. With verticalAlign="middle" and
    # containerId binding, Excalidraw centers the full text block in
    # the card body. The blank line shifts visible content downward.
    if icon:
        text_content = "\n" + text_content

    # Calculate text position
    line_count = len(text_content.split("\n"))
    text_height = line_count * 14 * 1.25

    if icon:
        # With icon: text starts below the icon overlap area
        text_top_margin = icon_size * icon_overlap + 5
        text_y = y + text_top_margin
    else:
        # No icon: center text vertically
        text_y = y + (height - text_height) / 2

    text = make_text(
        x=x + 5,
        y=text_y,
        text=text_content,
        font_size=14,
        color=theme.text,
        container_id=card_id,
        el_id=text_id,
    )
    text["width"] = width - 10
    text["height"] = text_height
    text["groupIds"] = [card_group_id]

    elements.extend([card, text])

    # --- Icon circle LAST (renders on top of card) ---
    if icon:
        # Center icon horizontally on card
        icon_x = x + (width - icon_size) / 2
        # Position so icon_overlap fraction is inside the card
        icon_y = y - icon_size * (1 - icon_overlap)

        circle_id = _uid("icon-circle")
        emoji_id = _uid("icon-emoji")

        circle = make_ellipse(icon_x, icon_y, icon_size, icon_size, theme, el_id=circle_id)
        circle["boundElements"] = [{"type": "text", "id": emoji_id}]
        circle["strokeWidth"] = 2
        circle["groupIds"] = [card_group_id]

        # Emoji sized proportionally to icon (roughly 50% of icon diameter)
        emoji_font_size = int(icon_size * 0.5)
        # Center emoji in circle
        emoji_x = icon_x + (icon_size - emoji_font_size) / 2
        emoji_y = icon_y + (icon_size - emoji_font_size) / 2

        emoji = make_text(
            x=emoji_x,
            y=emoji_y,
            text=icon,
            font_size=emoji_font_size,
            color="#ffffff",
            container_id=circle_id,
            el_id=emoji_id,
        )
        emoji["width"] = emoji_font_size
        emoji["height"] = emoji_font_size
        emoji["groupIds"] = [card_group_id]

        elements.extend([circle, emoji])

    # Calculate total bbox including icon
    if icon:
        icon_protrusion = icon_size * (1 - icon_overlap)  # Part of icon above card
        total_y = y - icon_protrusion
        total_height = height + icon_protrusion
    else:
        total_y = y
        total_height = height

    return Component(
        elements=elements,
        bbox=BBox(x, total_y, width, total_height),
    )


def group_box(
    x: float,
    y: float,
    width: float,
    height: float,
    label: str | None = None,
    label_position: str = "above-center",
) -> Component:
    """Create a dashed grouping rectangle with optional label.

    Args:
        label_position:
            "above-center" — label centered above the box (avoids arrow collision)
            "inside-top-left" — label inside box at top-left (classic style)
    """
    elements = []

    box = make_rectangle(
        x, y, width, height,
        theme=Theme.GRAY,
        stroke_style="dashed",
        stroke_width=1,
        rounded=False,
    )
    box["backgroundColor"] = "transparent"
    elements.append(box)

    label_above_height = 0
    if label:
        if label_position == "above-center":
            label_above_height = 14 * 1.25 + 5  # ~22.5px
            label_text = make_text(
                x=x,
                y=y - label_above_height,
                text=label,
                font_size=14,
                color="#495057",
                align="center",
                vertical_align="top",
            )
            label_text["width"] = width
        else:  # inside-top-left
            label_text = make_text(
                x=x + 10,
                y=y + 10,
                text=label,
                font_size=14,
                color="#495057",
                align="left",
                vertical_align="top",
            )
        elements.append(label_text)

    # Include label area in bbox when positioned above
    bbox_y = y - label_above_height if label_above_height else y
    bbox_h = height + label_above_height if label_above_height else height

    return Component(
        elements=elements,
        bbox=BBox(x, bbox_y, width, bbox_h),
    )


# =============================================================================
# Layout Engine
# =============================================================================

@dataclass
class LayoutConfig:
    """Configuration for layout calculations."""
    spacing_x: float = 20
    spacing_y: float = 20
    min_margin: float = 10
    grid_size: float = 20  # Snap to grid


class Diagram:
    """
    Main diagram builder with automatic layout.

    Example:
        diagram = Diagram(start_x=100, start_y=100)

        # Add a card
        card = diagram.add_card("Title", subtitle="desc", icon="📦")

        # Add a grid of boxes below
        grid = diagram.add_grid(
            labels=["A", "B", "C", "D"],
            cols=2,
            below=card,
        )

        # Export
        diagram.to_json("output.json")
    """

    def __init__(
        self,
        start_x: float = 100,
        start_y: float = 100,
        config: LayoutConfig | None = None,
    ):
        self.config = config or LayoutConfig()
        self.cursor_x = self._snap(start_x)
        self.cursor_y = self._snap(start_y)
        self.components: list[Component] = []
        self.elements: list[dict] = []
        self._placed_bboxes: list[BBox] = []

    def _snap(self, value: float) -> float:
        """Snap value to grid."""
        grid = self.config.grid_size
        return round(value / grid) * grid

    def _find_free_position(
        self,
        width: float,
        height: float,
        preferred_x: float | None = None,
        preferred_y: float | None = None,
    ) -> tuple[float, float]:
        """Find a position that doesn't overlap existing elements."""
        x = self._snap(preferred_x if preferred_x is not None else self.cursor_x)
        y = self._snap(preferred_y if preferred_y is not None else self.cursor_y)

        candidate = BBox(x, y, width, height)

        # Check for overlaps and adjust
        max_iterations = 100
        for _ in range(max_iterations):
            has_overlap = False
            for placed in self._placed_bboxes:
                if candidate.overlaps(placed, margin=self.config.min_margin):
                    has_overlap = True
                    # Move right or down
                    if candidate.right < placed.right + width + self.config.spacing_x:
                        x = self._snap(placed.right + self.config.spacing_x)
                    else:
                        x = self._snap(self.cursor_x)
                        y = self._snap(max(b.bottom for b in self._placed_bboxes) + self.config.spacing_y)
                    candidate = BBox(x, y, width, height)
                    break

            if not has_overlap:
                break

        return x, y

    def _register_component(self, component: Component):
        """Register a component's bbox and elements."""
        self.components.append(component)
        self.elements.extend(component.elements)
        self._placed_bboxes.append(component.bbox)
        # Update cursor to bottom of component
        self.cursor_y = self._snap(component.bbox.bottom + self.config.spacing_y)

    def add_card(
        self,
        title: str,
        subtitle: str | None = None,
        icon: str | None = None,
        theme: ColorTheme = Theme.BLUE,
        width: float = 160,
        height: float = 100,
        x: float | None = None,
        y: float | None = None,
    ) -> Component:
        """Add a card with icon."""
        # Account for icon overlap
        total_height = height + (25 if icon else 0)
        px, py = self._find_free_position(width, total_height, x, y)
        if icon:
            py += 25  # Adjust for icon overlap

        component = card_with_icon(px, py, width, height, title, subtitle, icon, theme)
        self._register_component(component)
        return component

    def add_box(
        self,
        label: str,
        theme: ColorTheme = Theme.BLUE,
        width: float = 80,
        height: float = 50,
        x: float | None = None,
        y: float | None = None,
        font_size: int = 14,
    ) -> Component:
        """Add a labeled box."""
        px, py = self._find_free_position(width, height, x, y)
        component = labeled_box(px, py, width, height, label, theme, font_size)
        self._register_component(component)
        return component

    def add_grid(
        self,
        labels: list[str],
        cols: int = 4,
        theme: ColorTheme = Theme.GREEN,
        box_width: float | None = None,
        box_height: float = 50,
        spacing: float = 10,
        x: float | None = None,
        y: float | None = None,
        center_last_row: bool = True,
        font_size: int = 14,
        below: Component | None = None,
        below_offset: float = 10,
    ) -> Component:
        """Add a grid of labeled boxes.

        Args:
            box_width: Width of each grid cell. If None, auto-calculated from
                the longest label text to prevent overflow.
            center_last_row: If True, center items in an incomplete last row
                within the grid width. Default True.
            font_size: Font size for labels (default 14). Used for auto-width
                calculation when box_width is None.
            below: Parent component to anchor this grid below. The grid is
                positioned directly below the parent with its left edge aligned.
                Overrides x/y if provided.
            below_offset: Gap between parent bottom and grid top (default 10px).
        """
        # Auto-size cell width from content if not explicitly set
        if box_width is None:
            char_width = font_size * 0.6
            padding = 20  # 10px padding on each side
            max_label_width = max(len(label) for label in labels) * char_width
            box_width = self._snap(max(80, max_label_width + padding))

        # Anchor below parent component if specified
        parent_child_group_id = None
        if below is not None:
            x, y = self.position_below(below, offset=below_offset)
            # Create outer group so parent + children move together
            parent_child_group_id = _uid("spoke-group")
            for el in below.elements:
                el["groupIds"].append(parent_child_group_id)

        rows = (len(labels) + cols - 1) // cols
        total_width = cols * box_width + (cols - 1) * spacing
        total_height = rows * box_height + (rows - 1) * spacing

        px, py = self._find_free_position(total_width, total_height, x, y)

        # Calculate last row info for centering
        last_row_idx = rows - 1
        last_row_count = len(labels) - last_row_idx * cols

        all_elements = []
        for i, label in enumerate(labels):
            row = i // cols
            col = i % cols

            # Center incomplete last row
            x_offset = 0.0
            if center_last_row and row == last_row_idx and last_row_count < cols:
                x_offset = (cols - last_row_count) * (box_width + spacing) / 2

            bx = px + col * (box_width + spacing) + x_offset
            by = py + row * (box_height + spacing)
            box = labeled_box(bx, by, box_width, box_height, label, theme, font_size)
            all_elements.extend(box.elements)

        # Add parent-child group to all grid elements
        if parent_child_group_id:
            for el in all_elements:
                el["groupIds"].append(parent_child_group_id)

        component = Component(
            elements=all_elements,
            bbox=BBox(px, py, total_width, total_height),
        )
        self._register_component(component)
        return component

    def add_group(
        self,
        label: str | None = None,
        width: float = 300,
        height: float = 200,
        x: float | None = None,
        y: float | None = None,
        label_position: str = "above-center",
    ) -> Component:
        """Add a grouping box (dashed rectangle with label).

        Args:
            label_position: "above-center" or "inside-top-left"
        """
        px, py = self._find_free_position(width, height, x, y)
        component = group_box(px, py, width, height, label, label_position)
        self._register_component(component)
        return component

    def add_panel(
        self,
        title: str,
        content: str,
        width: float = 300,
        padding: float = 20,
        title_font_size: int = 14,
        content_font_size: int = 13,
        title_color: str = "#495057",
        content_color: str = "#495057",
        x: float | None = None,
        y: float | None = None,
        below: Component | None = None,
        below_offset: float = 10,
    ) -> Component:
        """Add an auto-sized panel with title and content text.

        Creates a dashed group box with a title and body text,
        automatically calculating the height to fit content.
        No manual height calculation needed.

        Args:
            title: Panel header text
            content: Multi-line body text
            width: Panel width
            padding: Internal padding on all sides
            title_font_size: Header font size (default 14)
            content_font_size: Body text font size (default 13)
            title_color: Header text color
            content_color: Body text color
            below: Parent component to anchor this panel below.
            below_offset: Gap between parent and panel (default 10px).
        """
        # Anchor below parent component if specified
        parent_child_group_id = None
        if below is not None:
            x, y = self.position_below(below, offset=below_offset)
            # Create outer group so parent + children move together
            parent_child_group_id = _uid("spoke-group")
            for el in below.elements:
                el["groupIds"].append(parent_child_group_id)

        # Auto-calculate height from content
        title_height = title_font_size * 1.25
        content_lines = content.split("\n")
        content_height = len(content_lines) * content_font_size * 1.25
        gap = 8
        total_height = padding + title_height + gap + content_height + padding

        px, py = self._find_free_position(width, total_height, x, y)

        elements = []

        # Dashed group box
        box = make_rectangle(
            px, py, width, total_height,
            theme=Theme.GRAY,
            stroke_style="dashed",
            stroke_width=1,
            rounded=False,
        )
        box["backgroundColor"] = "transparent"
        elements.append(box)

        # Title text
        title_y = py + padding
        title_text = make_text(
            x=px + padding,
            y=title_y,
            text=title,
            font_size=title_font_size,
            color=title_color,
            align="left",
            vertical_align="top",
        )
        elements.append(title_text)

        # Content text
        content_y = title_y + title_height + gap
        content_text = make_text(
            x=px + padding,
            y=content_y,
            text=content,
            font_size=content_font_size,
            color=content_color,
            align="left",
            vertical_align="top",
        )
        elements.append(content_text)

        # Add parent-child group to all panel elements
        if parent_child_group_id:
            for el in elements:
                el["groupIds"].append(parent_child_group_id)

        component = Component(
            elements=elements,
            bbox=BBox(px, py, width, total_height),
        )
        self._register_component(component)
        return component

    def add_arrow(
        self,
        from_component: Component,
        to_component: Component,
        from_side: str = "bottom",
        to_side: str = "top",
        theme: ColorTheme | None = None,
        stroke_style: str = "solid",
        routing: str = "auto",
        clearance: float = 60,
        label: str | None = None,
        label_font_size: int = 13,
        label_color: str | None = None,
    ) -> Component:
        """Add an arrow between two components.

        Args:
            from_side/to_side: "top", "bottom", "left", "right"
            routing: Arrow path strategy:
                - "auto": Infer from from_side/to_side (recommended)
                - "straight": Direct line
                - "l-right-down": Horizontal then vertical
                - "l-down-right": Vertical then horizontal
                - "u-left": U-shape looping left (for same-side connections)
                - "u-right": U-shape looping right
                - "z-mid": Z-shape through vertical midpoint
            clearance: Offset distance for U-shape routing (default 60px)
            label: Optional text label placed at arrow midpoint
            label_font_size: Font size for the label (default 12)
            label_color: Label color (defaults to theme stroke or gray)
        """
        from_bbox = from_component.bbox
        to_bbox = to_component.bbox

        start_x, start_y = self._get_edge_point(from_bbox, from_side)
        end_x, end_y = self._get_edge_point(to_bbox, to_side)

        dx = end_x - start_x
        dy = end_y - start_y

        # Resolve auto routing
        if routing == "auto":
            routing = self._infer_routing(from_side, to_side, dx, dy)

        # Calculate points based on routing strategy
        points = self._route_arrow(routing, dx, dy, clearance)

        arrow = make_arrow(start_x, start_y, points, theme, stroke_style=stroke_style)
        arrow_elements = [arrow]

        # Bind label text to arrow — Excalidraw auto-positions it on the path
        if label:
            label_id = _uid("arrow-label")
            lbl_color = label_color or (theme.stroke if theme else "#495057")

            # Approximate midpoint for initial coordinates (Excalidraw adjusts on render)
            mid_x, mid_y = self._arrow_midpoint(start_x, start_y, points)

            lbl = make_text(
                x=mid_x, y=mid_y, text=label,
                font_size=label_font_size, color=lbl_color,
                align="center", vertical_align="middle",
                container_id=arrow["id"],
                el_id=label_id,
            )
            # Bind: arrow references text, text references arrow
            arrow["boundElements"] = [{"type": "text", "id": label_id}]
            arrow_elements.append(lbl)

        component = Component(
            elements=arrow_elements,
            bbox=BBox(
                min(start_x, end_x), min(start_y, end_y),
                max(abs(dx), 1), max(abs(dy), 1),
            ),
        )
        # Don't register arrow bbox to avoid affecting layout
        for el in arrow_elements:
            self.elements.append(el)
        return component

    def _infer_routing(
        self, from_side: str, to_side: str, dx: float, dy: float,
    ) -> str:
        """Infer arrow routing strategy from connection geometry."""
        # Same side → U-shape (feedback loops, parallel connections)
        if from_side == to_side:
            if from_side in ("left", "top"):
                return "u-left"
            return "u-right"

        # Opposite sides → straight if aligned, Z-mid otherwise
        opposite_pairs = {
            ("top", "bottom"), ("bottom", "top"),
            ("left", "right"), ("right", "left"),
        }
        if (from_side, to_side) in opposite_pairs:
            if from_side in ("top", "bottom") and abs(dx) < 5:
                return "straight"
            if from_side in ("left", "right") and abs(dy) < 5:
                return "straight"
            return "z-mid"

        # Perpendicular → L-shape
        if from_side in ("left", "right"):
            return "l-right-down"
        return "l-down-right"

    @staticmethod
    def _route_arrow(
        routing: str, dx: float, dy: float, clearance: float,
    ) -> list[tuple[float, float]]:
        """Calculate arrow points for a given routing strategy."""
        if routing == "straight":
            return [(0, 0), (dx, dy)]
        elif routing == "l-right-down":
            return [(0, 0), (dx, 0), (dx, dy)]
        elif routing == "l-down-right":
            return [(0, 0), (0, dy), (dx, dy)]
        elif routing == "u-left":
            return [(0, 0), (-clearance, 0), (-clearance, dy), (dx, dy)]
        elif routing == "u-right":
            return [(0, 0), (clearance, 0), (clearance, dy), (dx, dy)]
        elif routing == "z-mid":
            if abs(dx) < 5:
                return [(0, 0), (0, dy)]
            if abs(dy) < 5:
                return [(0, 0), (dx, 0)]
            return [(0, 0), (0, dy / 2), (dx, dy / 2), (dx, dy)]
        else:
            # Fallback to z-mid
            return [(0, 0), (0, dy / 2), (dx, dy / 2), (dx, dy)]

    @staticmethod
    def _arrow_midpoint(
        start_x: float, start_y: float,
        points: list[tuple[float, float]],
    ) -> tuple[float, float]:
        """Calculate the visual midpoint of an arrow path."""
        if len(points) <= 2:
            end = points[-1]
            return (start_x + end[0] / 2, start_y + end[1] / 2)

        # For multi-segment paths, use midpoint of the middle segment
        mid_idx = len(points) // 2
        p1 = points[mid_idx - 1]
        p2 = points[mid_idx]
        return (
            start_x + (p1[0] + p2[0]) / 2,
            start_y + (p1[1] + p2[1]) / 2,
        )

    def _get_edge_point(self, bbox: BBox, side: str) -> tuple[float, float]:
        """Get the center point of a bbox edge."""
        if side == "top":
            return bbox.center_x, bbox.y
        elif side == "bottom":
            return bbox.center_x, bbox.bottom
        elif side == "left":
            return bbox.x, bbox.center_y
        elif side == "right":
            return bbox.right, bbox.center_y
        else:
            raise ValueError(f"Invalid side: {side}")

    def add_text(
        self,
        text: str,
        font_size: int = 16,
        color: str = "#1e1e1e",
        x: float | None = None,
        y: float | None = None,
    ) -> Component:
        """Add standalone text."""
        lines = text.split("\n")
        height = len(lines) * font_size * 1.25
        width = max(len(line) for line in lines) * font_size * 0.6

        px, py = self._find_free_position(width, height, x, y)
        text_el = make_text(px, py, text, font_size, color, align="left", vertical_align="top")

        component = Component(
            elements=[text_el],
            bbox=BBox(px, py, width, height),
        )
        self._register_component(component)
        return component

    def add_title(
        self,
        text: str,
        subtitle: str | None = None,
        font_size: int = 28,
        subtitle_font_size: int = 16,
        color: str = "#1e1e1e",
        subtitle_color: str = "#868e96",
        x: float | None = None,
        y: float | None = None,
    ) -> Component:
        """Add a diagram title with optional subtitle, properly stacked.

        Creates a title text element and an optional subtitle below it.
        Both are left-aligned and vertically stacked with consistent spacing.

        Args:
            text: Main title text
            subtitle: Secondary description line (smaller, lighter)
            font_size: Title font size (default 28)
            subtitle_font_size: Subtitle font size (default 16)
            color: Title text color
            subtitle_color: Subtitle text color
        """
        title_height = font_size * 1.25
        char_width = font_size * 0.6
        title_width = len(text) * char_width

        # Account for subtitle width too
        total_width = title_width
        if subtitle:
            sub_width = len(subtitle) * subtitle_font_size * 0.6
            total_width = max(title_width, sub_width)

        # Calculate total height
        gap = 4
        subtitle_height = subtitle_font_size * 1.25 if subtitle else 0
        total_height = title_height + (gap + subtitle_height if subtitle else 0)

        px, py = self._find_free_position(total_width, total_height, x, y)

        elements = []

        # Title text
        title_el = make_text(
            px, py, text,
            font_size=font_size, color=color,
            align="left", vertical_align="top",
        )
        elements.append(title_el)

        # Subtitle text
        if subtitle:
            sub_y = py + title_height + gap
            sub_el = make_text(
                px, sub_y, subtitle,
                font_size=subtitle_font_size, color=subtitle_color,
                align="left", vertical_align="top",
            )
            elements.append(sub_el)

        component = Component(
            elements=elements,
            bbox=BBox(px, py, total_width, total_height),
        )
        self._register_component(component)
        return component

    def position_below(
        self,
        reference: Component,
        offset: float | None = None,
    ) -> tuple[float, float]:
        """Get position below a component."""
        gap = offset if offset is not None else self.config.spacing_y
        return reference.bbox.x, self._snap(reference.bbox.bottom + gap)

    def position_right_of(
        self,
        reference: Component,
        offset: float | None = None,
    ) -> tuple[float, float]:
        """Get position to the right of a component."""
        gap = offset if offset is not None else self.config.spacing_x
        return self._snap(reference.bbox.right + gap), reference.bbox.y

    def to_dict(self) -> dict:
        """Export diagram as Excalidraw-compatible dict."""
        return {
            "type": "excalidraw",
            "version": 2,
            "source": "kh-layout-engine",
            "elements": self.elements,
            "appState": {
                "gridSize": int(self.config.grid_size),
                "viewBackgroundColor": "#ffffff",
            },
            "files": {},
        }

    def to_json(self, path: str | Path, indent: int = 2) -> None:
        """Export diagram as JSON file."""
        path = Path(path)
        path.write_text(json.dumps(self.to_dict(), indent=indent), encoding="utf-8")


# =============================================================================
# CLI
# =============================================================================

def main():
    """Demo the layout engine."""
    diagram = Diagram(start_x=100, start_y=100)

    # Create a card with icon
    base_node = diagram.add_card(
        "BaseNode",
        subtitle="id, name, source_files[]",
        icon="📦",
        theme=Theme.BLUE,
        width=160,
        height=120,
    )

    # Create grid of node types below
    x, y = diagram.position_right_of(base_node, offset=80)
    nodes = diagram.add_grid(
        labels=["Process", "Requirement", "Document", "Decision", "Role", "System", "Term", "Project"],
        cols=4,
        theme=Theme.GREEN,
        x=x,
        y=y,
    )

    # Add arrow
    diagram.add_arrow(base_node, nodes, from_side="right", to_side="left")

    # Export
    diagram.to_json("demo_layout.json")
    print("Generated demo_layout.json")
    print(f"Total elements: {len(diagram.elements)}")


if __name__ == "__main__":
    main()
