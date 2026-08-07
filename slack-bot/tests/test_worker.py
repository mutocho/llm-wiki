import threading
import time

from worker import SerialWorker


def test_jobs_run_sequentially_in_order():
    w = SerialWorker()
    w.start()
    results = []
    lock_check = []

    def make_job(i):
        def job():
            lock_check.append("in")
            assert lock_check.count("in") - lock_check.count("out") == 1
            time.sleep(0.05)
            results.append(i)
            lock_check.append("out")
        return job

    for i in range(3):
        w.submit(make_job(i))
    deadline = time.time() + 5
    while len(results) < 3 and time.time() < deadline:
        time.sleep(0.01)
    assert results == [0, 1, 2]


def test_exception_does_not_kill_worker():
    w = SerialWorker()
    w.start()
    done = threading.Event()

    def bad():
        raise RuntimeError("fake failure")

    w.submit(bad)
    w.submit(done.set)
    assert done.wait(timeout=5)
