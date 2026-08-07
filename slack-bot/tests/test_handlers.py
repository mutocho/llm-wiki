from unittest import mock

import handlers

CH = "C_FAKE"


def ev(**kw):
    base = {"channel": CH, "text": "fake note", "user": "U_FAKE"}
    base.update(kw)
    return base


def test_should_capture_plain_message():
    assert handlers.should_capture(ev(), CH) is True


def test_should_skip_other_channel():
    assert handlers.should_capture(ev(channel="C_OTHER"), CH) is False


def test_should_skip_bot_message():
    assert handlers.should_capture(ev(bot_id="B_FAKE"), CH) is False


def test_should_skip_thread_reply():
    assert handlers.should_capture(ev(thread_ts="123.456"), CH) is False


def test_should_skip_subtype_events():
    assert handlers.should_capture(ev(subtype="message_changed"), CH) is False


def test_should_skip_empty_text():
    assert handlers.should_capture(ev(text="  "), CH) is False


def test_split_message_short_is_single_chunk():
    assert handlers.split_message("abc") == ["abc"]


def test_split_message_long_is_chunked():
    chunks = handlers.split_message("x" * 8000, limit=3900)
    assert len(chunks) == 3
    assert "".join(chunks) == "x" * 8000


def test_process_capture_runs_codex_then_sync():
    with mock.patch.object(handlers.runner, "run_codex", return_value="saved: _raw/f.md") as rc, \
         mock.patch.object(handlers.runner, "run_sync") as rs:
        out = handlers.process("capture", "fake note")
    assert "saved: _raw/f.md" in out
    rc.assert_called_once()
    rs.assert_called_once()


def test_process_query_skips_sync():
    with mock.patch.object(handlers.runner, "run_codex", return_value="answer"), \
         mock.patch.object(handlers.runner, "run_sync") as rs:
        out = handlers.process("query", "q?")
    assert out == "answer"
    rs.assert_not_called()


def test_process_error_returns_message_not_raise():
    with mock.patch.object(handlers.runner, "run_codex", side_effect=RuntimeError("fake boom")):
        out = handlers.process("query", "q?")
    assert out.startswith("오류:")
    assert "fake boom" in out
