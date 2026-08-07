"""이벤트 필터링과 처리 로직. Slack SDK 객체에 의존하지 않는다."""
import logging

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


def split_message(text, limit=3900):
    return [text[i:i + limit] for i in range(0, len(text), limit)] or [text]


def process(kind, text):
    try:
        out = runner.run_codex(runner.build_prompt(kind, text))
        if kind in runner.NEEDS_SYNC:
            runner.run_sync()
        return out.strip() or "(출력 없음)"
    except Exception as e:
        log.exception("process failed: kind=%s", kind)
        return f"오류: {e}"
