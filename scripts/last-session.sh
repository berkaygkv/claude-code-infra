#!/bin/bash
# Get the last session number
# Usage: ./last-session.sh
#
# Returns:
#   "session-N" if sessions exist
#   "FIRST_RUN" if no sessions exist (first-run scenario)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../.kh-config.json"

# Check config exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "ERROR: Config not found at $CONFIG_FILE" >&2
    exit 1
fi

# Get vault path from config
VAULT_ROOT=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['vault_root'])")

if [ -z "$VAULT_ROOT" ]; then
    echo "ERROR: Could not read vault_root from config" >&2
    exit 1
fi

SESSIONS_DIR="$VAULT_ROOT/notes/Sessions"

# Find last session
LAST_SESSION=$(ls -1 "$SESSIONS_DIR"/session-*.md 2>/dev/null | grep -oP 'session-\d+' | sort -t- -k2 -n | tail -1)

if [ -z "$LAST_SESSION" ]; then
    echo "FIRST_RUN"
else
    echo "$LAST_SESSION"
fi
