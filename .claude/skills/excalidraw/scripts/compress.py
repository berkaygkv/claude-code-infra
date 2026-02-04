#!/usr/bin/env python3
"""
Compress/decompress Excalidraw JSON for Obsidian .excalidraw.md format.

Usage:
    python compress.py <input.json> <output.excalidraw.md>
    python compress.py --decompress <input.excalidraw.md> <output.json>
"""

import sys
import json
import re
from pathlib import Path

# LZ-String compression implementation (compatible with JavaScript LZString.compressToBase64)
# Based on https://github.com/gkovacs/lz-string-python

KEY_STR_BASE64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
BASE_REVERSE_DIC = {}

def _get_base_value(char: str, alphabet: str) -> int:
    if alphabet not in BASE_REVERSE_DIC:
        BASE_REVERSE_DIC[alphabet] = {c: i for i, c in enumerate(alphabet)}
    return BASE_REVERSE_DIC[alphabet].get(char, -1)

def compress_to_base64(uncompressed: str) -> str:
    """Compress string to base64 (LZString.compressToBase64 compatible)."""
    if not uncompressed:
        return ""
    compressed = _compress(uncompressed, 6, lambda a: KEY_STR_BASE64[a])
    # Pad to multiple of 4
    remainder = len(compressed) % 4
    if remainder:
        compressed += "=" * (4 - remainder)
    return compressed

def decompress_from_base64(compressed: str) -> str:
    """Decompress base64 string (LZString.decompressFromBase64 compatible)."""
    if not compressed:
        return ""
    # Remove newlines and padding
    compressed = compressed.replace('\n', '').replace('\r', '').rstrip('=')
    return _decompress(len(compressed), 32, lambda i: _get_base_value(compressed[i], KEY_STR_BASE64))

def _compress(uncompressed: str, bits_per_char: int, get_char_from_int) -> str:
    if not uncompressed:
        return ""

    context_dictionary = {}
    context_dictionary_to_create = {}
    context_c = ""
    context_wc = ""
    context_w = ""
    context_enlarge_in = 2
    context_dict_size = 3
    context_num_bits = 2
    context_data = []
    context_data_val = 0
    context_data_position = 0

    for ii in range(len(uncompressed)):
        context_c = uncompressed[ii]
        if context_c not in context_dictionary:
            context_dictionary[context_c] = context_dict_size
            context_dict_size += 1
            context_dictionary_to_create[context_c] = True

        context_wc = context_w + context_c
        if context_wc in context_dictionary:
            context_w = context_wc
        else:
            if context_w in context_dictionary_to_create:
                if ord(context_w[0]) < 256:
                    for _ in range(context_num_bits):
                        context_data_val = (context_data_val << 1)
                        if context_data_position == bits_per_char - 1:
                            context_data_position = 0
                            context_data.append(get_char_from_int(context_data_val))
                            context_data_val = 0
                        else:
                            context_data_position += 1
                    value = ord(context_w[0])
                    for _ in range(8):
                        context_data_val = (context_data_val << 1) | (value & 1)
                        if context_data_position == bits_per_char - 1:
                            context_data_position = 0
                            context_data.append(get_char_from_int(context_data_val))
                            context_data_val = 0
                        else:
                            context_data_position += 1
                        value >>= 1
                else:
                    value = 1
                    for _ in range(context_num_bits):
                        context_data_val = (context_data_val << 1) | value
                        if context_data_position == bits_per_char - 1:
                            context_data_position = 0
                            context_data.append(get_char_from_int(context_data_val))
                            context_data_val = 0
                        else:
                            context_data_position += 1
                        value = 0
                    value = ord(context_w[0])
                    for _ in range(16):
                        context_data_val = (context_data_val << 1) | (value & 1)
                        if context_data_position == bits_per_char - 1:
                            context_data_position = 0
                            context_data.append(get_char_from_int(context_data_val))
                            context_data_val = 0
                        else:
                            context_data_position += 1
                        value >>= 1
                context_enlarge_in -= 1
                if context_enlarge_in == 0:
                    context_enlarge_in = 2 ** context_num_bits
                    context_num_bits += 1
                del context_dictionary_to_create[context_w]
            else:
                value = context_dictionary[context_w]
                for _ in range(context_num_bits):
                    context_data_val = (context_data_val << 1) | (value & 1)
                    if context_data_position == bits_per_char - 1:
                        context_data_position = 0
                        context_data.append(get_char_from_int(context_data_val))
                        context_data_val = 0
                    else:
                        context_data_position += 1
                    value >>= 1
            context_enlarge_in -= 1
            if context_enlarge_in == 0:
                context_enlarge_in = 2 ** context_num_bits
                context_num_bits += 1
            context_dictionary[context_wc] = context_dict_size
            context_dict_size += 1
            context_w = context_c

    if context_w:
        if context_w in context_dictionary_to_create:
            if ord(context_w[0]) < 256:
                for _ in range(context_num_bits):
                    context_data_val = (context_data_val << 1)
                    if context_data_position == bits_per_char - 1:
                        context_data_position = 0
                        context_data.append(get_char_from_int(context_data_val))
                        context_data_val = 0
                    else:
                        context_data_position += 1
                value = ord(context_w[0])
                for _ in range(8):
                    context_data_val = (context_data_val << 1) | (value & 1)
                    if context_data_position == bits_per_char - 1:
                        context_data_position = 0
                        context_data.append(get_char_from_int(context_data_val))
                        context_data_val = 0
                    else:
                        context_data_position += 1
                    value >>= 1
            else:
                value = 1
                for _ in range(context_num_bits):
                    context_data_val = (context_data_val << 1) | value
                    if context_data_position == bits_per_char - 1:
                        context_data_position = 0
                        context_data.append(get_char_from_int(context_data_val))
                        context_data_val = 0
                    else:
                        context_data_position += 1
                    value = 0
                value = ord(context_w[0])
                for _ in range(16):
                    context_data_val = (context_data_val << 1) | (value & 1)
                    if context_data_position == bits_per_char - 1:
                        context_data_position = 0
                        context_data.append(get_char_from_int(context_data_val))
                        context_data_val = 0
                    else:
                        context_data_position += 1
                    value >>= 1
            context_enlarge_in -= 1
            if context_enlarge_in == 0:
                context_enlarge_in = 2 ** context_num_bits
                context_num_bits += 1
            del context_dictionary_to_create[context_w]
        else:
            value = context_dictionary[context_w]
            for _ in range(context_num_bits):
                context_data_val = (context_data_val << 1) | (value & 1)
                if context_data_position == bits_per_char - 1:
                    context_data_position = 0
                    context_data.append(get_char_from_int(context_data_val))
                    context_data_val = 0
                else:
                    context_data_position += 1
                value >>= 1

    # End marker
    value = 2
    for _ in range(context_num_bits):
        context_data_val = (context_data_val << 1) | (value & 1)
        if context_data_position == bits_per_char - 1:
            context_data_position = 0
            context_data.append(get_char_from_int(context_data_val))
            context_data_val = 0
        else:
            context_data_position += 1
        value >>= 1

    while True:
        context_data_val = (context_data_val << 1)
        if context_data_position == bits_per_char - 1:
            context_data.append(get_char_from_int(context_data_val))
            break
        else:
            context_data_position += 1

    return "".join(context_data)

def _decompress(length: int, reset_value: int, get_next_value) -> str:
    dictionary = {}
    enlarge_in = 4
    dict_size = 4
    num_bits = 3
    entry = ""
    result = []

    data_val = get_next_value(0)
    data_position = reset_value
    data_index = 1

    for i in range(3):
        dictionary[i] = i

    bits = 0
    max_power = 2 ** 2
    power = 1
    while power != max_power:
        resb = data_val & data_position
        data_position >>= 1
        if data_position == 0:
            data_position = reset_value
            data_val = get_next_value(data_index)
            data_index += 1
        bits |= (1 if resb > 0 else 0) * power
        power <<= 1

    next_val = bits
    if next_val == 0:
        bits = 0
        max_power = 2 ** 8
        power = 1
        while power != max_power:
            resb = data_val & data_position
            data_position >>= 1
            if data_position == 0:
                data_position = reset_value
                data_val = get_next_value(data_index)
                data_index += 1
            bits |= (1 if resb > 0 else 0) * power
            power <<= 1
        c = chr(bits)
    elif next_val == 1:
        bits = 0
        max_power = 2 ** 16
        power = 1
        while power != max_power:
            resb = data_val & data_position
            data_position >>= 1
            if data_position == 0:
                data_position = reset_value
                data_val = get_next_value(data_index)
                data_index += 1
            bits |= (1 if resb > 0 else 0) * power
            power <<= 1
        c = chr(bits)
    elif next_val == 2:
        return ""

    dictionary[3] = c
    w = c
    result.append(c)

    while True:
        if data_index > length:
            return ""

        bits = 0
        max_power = 2 ** num_bits
        power = 1
        while power != max_power:
            resb = data_val & data_position
            data_position >>= 1
            if data_position == 0:
                data_position = reset_value
                data_val = get_next_value(data_index)
                data_index += 1
            bits |= (1 if resb > 0 else 0) * power
            power <<= 1

        c_val = bits
        if c_val == 0:
            bits = 0
            max_power = 2 ** 8
            power = 1
            while power != max_power:
                resb = data_val & data_position
                data_position >>= 1
                if data_position == 0:
                    data_position = reset_value
                    data_val = get_next_value(data_index)
                    data_index += 1
                bits |= (1 if resb > 0 else 0) * power
                power <<= 1
            dictionary[dict_size] = chr(bits)
            dict_size += 1
            c_val = dict_size - 1
            enlarge_in -= 1
        elif c_val == 1:
            bits = 0
            max_power = 2 ** 16
            power = 1
            while power != max_power:
                resb = data_val & data_position
                data_position >>= 1
                if data_position == 0:
                    data_position = reset_value
                    data_val = get_next_value(data_index)
                    data_index += 1
                bits |= (1 if resb > 0 else 0) * power
                power <<= 1
            dictionary[dict_size] = chr(bits)
            dict_size += 1
            c_val = dict_size - 1
            enlarge_in -= 1
        elif c_val == 2:
            return "".join(result)

        if enlarge_in == 0:
            enlarge_in = 2 ** num_bits
            num_bits += 1

        if c_val in dictionary:
            entry = dictionary[c_val]
        elif c_val == dict_size:
            entry = w + w[0]
        else:
            return None

        result.append(entry)
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        enlarge_in -= 1

        if enlarge_in == 0:
            enlarge_in = 2 ** num_bits
            num_bits += 1

        w = entry

def chunk_string(s: str, chunk_size: int = 256) -> str:
    """Split string into chunks with double newlines between."""
    return '\n\n'.join(s[i:i+chunk_size] for i in range(0, len(s), chunk_size))

def extract_text_elements(elements: list) -> list:
    """Extract text elements for the ## Text Elements section."""
    text_items = []
    for el in elements:
        if el.get('type') == 'text' and el.get('containerId'):
            # This is a label text element
            text = el.get('originalText') or el.get('text', '')
            element_id = el.get('id', '')
            if text and element_id:
                text_items.append((element_id, text))
    return text_items

def generate_excalidraw_md(json_data: dict, compress: bool = True) -> str:
    """Generate Obsidian-compatible .excalidraw.md content."""

    elements = json_data.get('elements', [])
    text_elements = extract_text_elements(elements)

    # Build the markdown
    lines = [
        "---",
        "excalidraw-plugin: parsed",
        "---",
        "",
        "# Excalidraw Data",
        "",
        "## Text Elements"
    ]

    # Add text elements for search indexing
    for element_id, text in text_elements:
        lines.append(f"{text} ^{element_id}")
        lines.append("")

    # Add the drawing section
    json_string = json.dumps(json_data, indent='\t')

    if compress:
        compressed = compress_to_base64(json_string)
        chunked = chunk_string(compressed)
        lines.append("%%")
        lines.append("## Drawing")
        lines.append("```compressed-json")
        lines.append(chunked)
        lines.append("```")
        lines.append("%%")
    else:
        lines.append("%%")
        lines.append("## Drawing")
        lines.append("```json")
        lines.append(json_string)
        lines.append("```")
        lines.append("%%")

    return '\n'.join(lines)

def extract_json_from_excalidraw_md(content: str) -> dict:
    """Extract and decompress JSON from .excalidraw.md file."""

    # Try compressed format first
    compressed_match = re.search(r'```compressed-json\s*\n(.*?)\n```', content, re.DOTALL)
    if compressed_match:
        compressed_data = compressed_match.group(1)
        json_string = decompress_from_base64(compressed_data)
        return json.loads(json_string)

    # Try uncompressed format
    json_match = re.search(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
    if json_match:
        return json.loads(json_match.group(1))

    raise ValueError("Could not find Drawing section in file")

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == '--decompress':
        if len(sys.argv) < 4:
            print("Usage: compress.py --decompress <input.excalidraw.md> <output.json>")
            sys.exit(1)

        input_path = Path(sys.argv[2])
        output_path = Path(sys.argv[3])

        content = input_path.read_text(encoding='utf-8')
        json_data = extract_json_from_excalidraw_md(content)

        output_path.write_text(json.dumps(json_data, indent=2), encoding='utf-8')
        print(f"Decompressed to {output_path}")

    else:
        input_path = Path(sys.argv[1])
        output_path = Path(sys.argv[2])

        # Check for --no-compress flag
        compress = '--no-compress' not in sys.argv

        json_data = json.loads(input_path.read_text(encoding='utf-8'))
        md_content = generate_excalidraw_md(json_data, compress=compress)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(md_content, encoding='utf-8')
        print(f"Generated {output_path}")

if __name__ == '__main__':
    main()
