"""이벤트 필터링과 처리 로직. Slack SDK 객체에 의존하지 않는다."""
import logging
import re
import time

import runner

log = logging.getLogger(__name__)


def should_capture(event, channel_id):
    if event.get("channel") != channel_id:
        return False
    if event.get("bot_id") or event.get("subtype"):
        return False
    if event.get("thread_ts"):
        return False
    if not (event.get("text") or "").strip():
        return False
    return True


def _convert_tables(text):
    """마크다운 테이블 블록 → 열 정렬된 코드블록 (Slack은 테이블 미지원)."""
    out, table = [], []

    def flush():
        if not table:
            return
        rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in table]
        rows = [r for r in rows if not all(re.fullmatch(r":?-+:?", c) for c in r)]
        widths = [max(len(r[i]) if i < len(r) else 0 for r in rows) for i in range(max(map(len, rows)))]
        lines = ["  ".join((r[i] if i < len(r) else "").ljust(widths[i]) for i in range(len(widths))).rstrip() for r in rows]
        out.append("```\n" + "\n".join(lines) + "\n```")
        table.clear()

    for line in text.splitlines():
        if line.lstrip().startswith("|"):
            table.append(line)
        else:
            flush()
            out.append(line)
    flush()
    return "\n".join(out)


# ponytail: 코드블록 내부까지 변환하는 naive regex — 문제가 보이면 블록 분리 파서로 업그레이드
def to_mrkdwn(text):
    """일반 markdown을 Slack mrkdwn으로 변환."""
    text = _convert_tables(text)
    text = re.sub(r"^#{1,6}\s+(.+)$", r"*\1*", text, flags=re.M)      # 헤더 → 굵게
    text = re.sub(r"\*\*(.+?)\*\*", r"*\1*", text)                    # **bold** → *bold*
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r"<\2|\1>", text)  # 링크
    text = re.sub(r"^(\s*)[-*]\s+", r"\1• ", text, flags=re.M)        # 불릿
    return text


def split_message(text, limit=3900):
    return [text[i:i + limit] for i in range(0, len(text), limit)] or [text]


def process(kind, text):
    t0 = time.monotonic()
    log.info("process start: kind=%s", kind)
    try:
        out = runner.run_codex(runner.build_prompt(kind, text))
        log.info("process done: kind=%s elapsed=%.1fs", kind, time.monotonic() - t0)
        if kind in runner.NEEDS_SYNC:
            runner.run_sync()
        return out.strip() or "(출력 없음)"
    except Exception as e:
        log.exception("process failed: kind=%s", kind)
        return f"오류: {e}"
