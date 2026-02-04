#!/usr/bin/env python3
"""
Validate Excalidraw JSON before compression.

Catches common issues that cause silent rendering failures:
- Missing text bindings (boundElements/containerId mismatch)
- Invalid arrow configurations
- Diamond shapes (broken in raw JSON)
- Duplicate IDs
- Invalid bounding boxes

Usage:
    python validate.py <input.json>

Exit codes:
    0 - Valid
    1 - Errors found (will not render correctly)
    2 - Warnings found (may have issues)
"""

import sys
import json
from pathlib import Path
from typing import List, Tuple

class ValidationResult:
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def error(self, msg: str):
        self.errors.append(f"ERROR: {msg}")

    def warning(self, msg: str):
        self.warnings.append(f"WARNING: {msg}")

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

def validate_excalidraw(data: dict) -> ValidationResult:
    """Validate Excalidraw JSON structure."""
    result = ValidationResult()
    elements = data.get('elements', [])

    # Build lookup tables
    elements_by_id = {el['id']: el for el in elements if 'id' in el}
    seen_ids = set()

    for el in elements:
        el_id = el.get('id', 'unknown')
        el_type = el.get('type', 'unknown')

        # Check for duplicate IDs
        if el_id in seen_ids:
            result.error(f"Duplicate ID: {el_id}")
        seen_ids.add(el_id)

        # Check for banned diamond shapes
        if el_type == 'diamond':
            result.error(f"Diamond shape found ({el_id}). Use styled rectangle instead.")

        # Validate text elements
        if el_type == 'text':
            container_id = el.get('containerId')
            if container_id:
                # This is a bound text - verify container exists and has boundElements
                if container_id not in elements_by_id:
                    result.error(f"Text {el_id} references missing container {container_id}")
                else:
                    container = elements_by_id[container_id]
                    bound_elements = container.get('boundElements') or []
                    text_bindings = [b for b in bound_elements if b.get('type') == 'text' and b.get('id') == el_id]
                    if not text_bindings:
                        result.error(f"Text {el_id} not in container's boundElements (container: {container_id})")

        # Validate shapes with boundElements
        if el.get('boundElements'):
            for binding in el['boundElements']:
                if binding.get('type') == 'text':
                    text_id = binding.get('id')
                    if text_id not in elements_by_id:
                        result.error(f"Shape {el_id} references missing text {text_id}")
                    else:
                        text_el = elements_by_id[text_id]
                        if text_el.get('containerId') != el_id:
                            result.error(f"Text {text_id} has wrong containerId (expected {el_id}, got {text_el.get('containerId')})")

        # Validate arrows
        if el_type == 'arrow':
            points = el.get('points', [])

            # Check elbow configuration for multi-point arrows
            if len(points) > 2:
                if el.get('roughness') != 0:
                    result.warning(f"Arrow {el_id} has {len(points)} points but roughness != 0 (may look curved)")
                if el.get('roundness') is not None:
                    result.warning(f"Arrow {el_id} has {len(points)} points but roundness is not null (may look curved)")
                if not el.get('elbowed'):
                    result.warning(f"Arrow {el_id} has {len(points)} points but elbowed != true")

            # Validate bounding box
            if points:
                max_x = max(abs(p[0]) for p in points)
                max_y = max(abs(p[1]) for p in points)
                declared_width = el.get('width', 0)
                declared_height = el.get('height', 0)

                if declared_width < max_x - 1:
                    result.warning(f"Arrow {el_id} width ({declared_width}) smaller than points extent ({max_x})")
                if declared_height < max_y - 1:
                    result.warning(f"Arrow {el_id} height ({declared_height}) smaller than points extent ({max_y})")

        # Check for null boundElements on shapes that should have it
        if el_type in ['rectangle', 'ellipse'] and el.get('boundElements') is None:
            # Check if any text element references this shape
            for other in elements:
                if other.get('type') == 'text' and other.get('containerId') == el_id:
                    result.error(f"Shape {el_id} has boundElements: null but text {other['id']} references it")

    # Validate file structure
    if 'type' not in data or data['type'] != 'excalidraw':
        result.warning("Missing or invalid 'type' field (should be 'excalidraw')")

    if 'version' not in data:
        result.warning("Missing 'version' field")

    if 'elements' not in data:
        result.error("Missing 'elements' array")

    if 'appState' not in data:
        result.warning("Missing 'appState' object")

    return result

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_path = Path(sys.argv[1])

    try:
        data = json.loads(input_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON - {e}")
        sys.exit(1)

    result = validate_excalidraw(data)

    # Print results
    for error in result.errors:
        print(error)
    for warning in result.warnings:
        print(warning)

    if result.is_valid:
        if result.warnings:
            print(f"\nValidation passed with {len(result.warnings)} warning(s)")
            sys.exit(2)
        else:
            print("Validation passed")
            sys.exit(0)
    else:
        print(f"\nValidation FAILED with {len(result.errors)} error(s)")
        sys.exit(1)

if __name__ == '__main__':
    main()
