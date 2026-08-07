"""Slack → llm-wiki 봇. Socket Mode 상주 프로세스.

실행: cd slack-bot && python3 app.py  (.env 필요 — .env.example 참조)
"""
import logging
import logging.handlers
import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import handlers
from worker import SerialWorker

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.handlers.RotatingFileHandler(
            os.path.join(LOG_DIR, "bot.log"), maxBytes=5_000_000, backupCount=3
        ),
    ],
)
log = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
CHANNEL = os.environ["WIKI_CHANNEL_ID"]

app = App(token=BOT_TOKEN)
worker = SerialWorker()


@app.event("message")
def on_message(event, say):
    log.info(
        "message event: channel=%s subtype=%s bot_id=%s thread_ts=%s",
        event.get("channel"), event.get("subtype"),
        event.get("bot_id"), event.get("thread_ts"),
    )
    if not handlers.should_capture(event, CHANNEL):
        return
    text, ts = event["text"], event["ts"]

    def job():
        say(text="🐢 적재 시작...", thread_ts=ts)
        result = handlers.process("capture", text)
        status = "❌ 적재 실패" if result.startswith("오류:") else "✅ 적재 완료"
        result = handlers.to_mrkdwn(f"{status}\n{result}")
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
            result = handlers.to_mrkdwn(handlers.process(kind, text))
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
