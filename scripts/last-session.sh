#!/bin/bash
# Get the last session number
# Usage: ./last-session.sh
#
# Returns:
#   "session-N" if sessions exist
#   "FIRST_RUN" if no sessions exist (first-run scenario)

SESSIONS_DIR="/home/berkaygkv/Dev/Docs/.obs-vault/notes/Sessions"

# Find last session
LAST_SESSION=$(ls -1 "$SESSIONS_DIR"/session-*.md 2>/dev/null | grep -oP 'session-\d+' | sort -t- -k2 -n | tail -1)

if [ -z "$LAST_SESSION" ]; then
    echo "FIRST_RUN"
else
    echo "$LAST_SESSION"
fi
