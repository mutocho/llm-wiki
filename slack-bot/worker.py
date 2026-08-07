"""단일 스레드 순차 작업 큐 — codex/git 동시 실행 방지."""
import logging
import queue
import threading

log = logging.getLogger(__name__)


class SerialWorker:
    def __init__(self):
        self._q = queue.Queue()

    def start(self):
        threading.Thread(target=self._loop, daemon=True).start()

    def submit(self, fn):
        self._q.put(fn)

    def _loop(self):
        while True:
            fn = self._q.get()
            try:
                fn()
            except Exception:
                log.exception("job failed")
