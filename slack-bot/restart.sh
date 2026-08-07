#!/bin/bash
# slack wiki bot 재시작 (launchd 서비스 reload)
set -e
PLIST="$HOME/Library/LaunchAgents/com.muto.slack-wiki-bot.plist"

launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"

sleep 2
if launchctl list | grep -q com.muto.slack-wiki-bot; then
  echo "restarted: $(launchctl list | grep com.muto.slack-wiki-bot)"
  tail -3 "$(dirname "$0")/logs/bot.log" 2>/dev/null
else
  echo "FAILED: service not running — check logs/launchd.err.log" >&2
  exit 1
fi
