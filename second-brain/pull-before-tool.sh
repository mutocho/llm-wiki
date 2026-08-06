#!/bin/bash
# Codex PreToolUse hook: update this repository only when it is safe.

SCRIPT_DIR="${BASH_SOURCE[0]%/*}"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT" || exit 0

# Never overwrite, stash, or merge over local work.
if [ -n "$(git status --porcelain --untracked-files=normal 2>/dev/null)" ]; then
  exit 0
fi

# Refuse merge commits and diverged histories; a later tool can surface the issue.
git pull --ff-only -q >/dev/null 2>&1 || exit 0
exit 0
