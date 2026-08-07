"""Slack → llm-wiki 봇. Socket Mode 상주 프로세스.

실행: cd slack-bot && python3 app.py  (.env 필요 — .env.example 참조)
"""
import logging
import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import handlers
from worker import SerialWorker

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
CHANNEL = os.environ["WIKI_CHANNEL_ID"]

app = App(token=BOT_TOKEN)
worker = SerialWorker()


@app.event("message")
def on_message(event, say):
    if not handlers.should_capture(event, CHANNEL):
        return
    text, ts = event["text"], event["ts"]

    def job():
        result = handlers.process("capture", text)
        for chunk in handlers.split_message(result):
            say(text=chunk, thread_ts=ts)

    worker.submit(job)


def make_command(kind, needs_text):
    def handle(ack, command, respond):
        text = (command.get("text") or "").strip()
        if needs_text and not text:
            ack(f"사용법: /wiki-{kind} <내용>")
            return
        ack("처리 중... 완료되면 결과를 보낼게요.")

        def job():
            result = handlers.process(kind, text)
            for chunk in handlers.split_message(result):
                respond(text=chunk, response_type="in_channel")

        worker.submit(job)
    return handle


app.command("/wiki-query")(make_command("query", needs_text=True))
app.command("/wiki-ingest")(make_command("ingest", needs_text=False))
app.command("/wiki-lint")(make_command("lint", needs_text=False))


if __name__ == "__main__":
    worker.start()
    log.info("starting slack wiki bot (channel=%s)", CHANNEL)
    SocketModeHandler(app, APP_TOKEN).start()
