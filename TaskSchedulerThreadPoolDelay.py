from concurrent.futures import ThreadPoolExecutor
import heapq
import threading
import time


def example_task(name):
    print(f"Running {name}")
    time.sleep(1)


class SimpleScheduler:
    def __init__(self, workers=3):
        self.tasks = []
        self.lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=workers)
        self.running = True

    def schedule(self, func, *args, delay=0):
        run_at = time.time() + delay

        with self.lock:
            heapq.heappush(self.tasks, (run_at, func, args))

    def run_forever(self):
        while self.running:
            now = time.time()

            with self.lock:
                if self.tasks:
                    run_at, func, args = self.tasks[0]

                    if run_at <= now:
                        heapq.heappop(self.tasks)
                        self.executor.submit(func, *args)

            time.sleep(0.1)

    def stop(self):
        self.running = False
        self.executor.shutdown(wait=True)


if __name__ == "__main__":
    scheduler = SimpleScheduler(workers=3)

    scheduler.schedule(example_task, "email-user", delay=2)
    scheduler.schedule(example_task, "generate-report", delay=5)
    scheduler.schedule(example_task, "send-notification", delay=1)

    try:
        scheduler.run_forever()
    except KeyboardInterrupt:
        scheduler.stop()
