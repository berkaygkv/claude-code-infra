#!/bin/bash
# Load protocol based on mode argument
# Usage: ./load-protocol.sh [brainstorm|build]

MODE="$1"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/.."
PROTOCOL_DIR="$PROJECT_ROOT/protocols"

if [ "$MODE" = "brainstorm" ]; then
    cat "$PROTOCOL_DIR/brainstorm.md"
elif [ "$MODE" = "build" ]; then
    cat "$PROTOCOL_DIR/build.md"
else
    cat "$PROTOCOL_DIR/base.md"
fi
