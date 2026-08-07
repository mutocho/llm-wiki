#!/bin/bash
# Codex PreToolUse/PostToolUse hook for the llm-wiki repository.
# Only second-brain/ is auto-committed. Merge conflicts prefer the remote side.

SCRIPT_DIR="${BASH_SOURCE[0]%/*}"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT" || exit 0

# This personal wiki is synchronized only on main.
[ "$(git branch --show-current 2>/dev/null)" = "main" ] || exit 0

# Do not stage, overwrite, or publish local work outside second-brain/.
if ! git diff --quiet -- . ':(exclude)second-brain' ||
   ! git diff --cached --quiet -- . ':(exclude)second-brain' ||
   [ -n "$(git ls-files --others --exclude-standard -- . ':(exclude)second-brain')" ]; then
  exit 0
fi

# Preserve local vault edits in a commit before integrating upstream changes.
git add -A -- second-brain
if ! git diff --cached --quiet -- second-brain; then
  git commit -qm "wiki: hook sync $(date +%F' '%T)" -- second-brain || exit 0
fi

# Prefer the remote version for conflicting hunks.
if ! git pull --no-rebase -X theirs -q; then
  # Authentication, network, and permission failures are not merge conflicts.
  if [ ! -f .git/MERGE_HEAD ] &&
     ! git diff --name-only --diff-filter=U | grep -q .; then
    exit 0
  fi
  git checkout --theirs -- . >/dev/null 2>&1 || true
  git add -A
  if git diff --name-only --diff-filter=U | grep -q .; then
    git merge --abort >/dev/null 2>&1 || true
    exit 0
  fi
  git commit -qm "wiki: auto-resolve merge conflicts (remote wins)" || true
fi

# Retry once if the remote moved between pull and push.
if ! git push -q; then
  git pull --no-rebase -X theirs -q || exit 0
  git push -q || exit 0
fi

exit 0
