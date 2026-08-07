from unittest import mock

import pytest

import runner


def test_build_prompt_capture_contains_message():
    p = runner.build_prompt("capture", "fake finding about X")
    assert "fake finding about X" in p
    assert "second-brain" in p


def test_build_prompt_query_contains_question():
    p = runner.build_prompt("query", "what is X?")
    assert "what is X?" in p
    assert "wiki-query" in p


def test_build_prompt_unknown_kind_raises():
    with pytest.raises(ValueError):
        runner.build_prompt("nope", "text")


def test_run_codex_returns_stdout():
    fake = mock.Mock(returncode=0, stdout="answer text", stderr="")
    with mock.patch("subprocess.run", return_value=fake) as m:
        out = runner.run_codex("do something")
    assert out == "answer text"
    cmd = m.call_args.args[0]
    assert cmd[:2] == ["codex", "exec"]
    assert "--cd" in cmd and runner.REPO in cmd


def test_run_codex_failure_raises():
    fake = mock.Mock(returncode=1, stdout="", stderr="boom")
    with mock.patch("subprocess.run", return_value=fake):
        with pytest.raises(RuntimeError):
            runner.run_codex("do something")


def test_run_sync_calls_sync_script():
    fake = mock.Mock(returncode=0, stdout="", stderr="")
    with mock.patch("subprocess.run", return_value=fake) as m:
        runner.run_sync()
    cmd = m.call_args.args[0]
    assert cmd[0] == "bash" and cmd[1].endswith("second-brain/sync.sh")
