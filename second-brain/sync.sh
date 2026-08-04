#!/bin/bash
# 볼트 자동 git 동기화.
# 훅 호출: stdin의 JSON에서 file_path를 읽어 볼트 내부 파일일 때만 동기화.
# 수동 호출: `bash second-brain/sync.sh` (인자/stdin 없이) → 무조건 동기화.
V="$(cd "$(dirname "$0")" && pwd)"

if [ ! -t 0 ]; then
  f=$(python3 -c 'import json,sys;print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))' 2>/dev/null)
  if [ -n "$f" ]; then
    case "$f" in "$V"/*) ;; *) exit 0 ;; esac
  fi
fi

cd "$V" || exit 0
git add -A .
git diff --cached --quiet -- . && exit 0
git commit -qm "wiki: auto-sync $(date +%F' '%T)" -- . && git push -q >/dev/null 2>&1
exit 0
