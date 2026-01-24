#!/bin/bash
# Load protocol based on mode argument
# Usage: ./load-protocol.sh [brainstorm|build]

MODE="$1"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../.kh-config.json"

# Check config exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "ERROR: Config not found at $CONFIG_FILE" >&2
    exit 1
fi

# Get KH path from config
KH_PATH=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['kh_path'])")

if [ -z "$KH_PATH" ]; then
    echo "ERROR: Could not read kh_path from config" >&2
    exit 1
fi

PROTOCOL_DIR="$KH_PATH/protocols"

if [ "$MODE" = "brainstorm" ]; then
    cat "$PROTOCOL_DIR/brainstorm.md"
elif [ "$MODE" = "build" ]; then
    cat "$PROTOCOL_DIR/build.md"
else
    cat "$PROTOCOL_DIR/base.md"
fi
