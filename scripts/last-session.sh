#!/bin/bash
# Get the last session number
# Usage: ./last-session.sh

ls -1 /home/berkaygkv/Dev/Docs/.obs-vault/notes/Sessions/session-*.md 2>/dev/null | grep -oP 'session-\d+' | sort -t- -k2 -n | tail -1
