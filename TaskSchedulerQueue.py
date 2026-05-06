import threading
from queue import Queue
import time

def example_task(task_id):
    print(f"[{threading.current_thread().name}] Executing task {task_id} \n")
    time.sleep(1)

class TaskQueue:
    def __init__(self, num_workers=3):
        self.queue = Queue()
        self.workers = []
        self.num_workers = num_workers
        self._stop = False

    def worker(self):
        while not self._stop:
            try:
                func, args = self.queue.get(timeout=1)
                func(*args)
                self.queue.task_done()
            except:
                continue  # queue empty, keep checking

    def start(self):
        for i in range(self.num_workers):
            t = threading.Thread(target=self.worker, name=f"Worker-{i}")
            t.daemon = True
            t.start()
            self.workers.append(t)

    def add_task(self, func, *args):
        self.queue.put((func, args))

    def stop(self):
        self._stop = True
        for t in self.workers:
            t.join()

    def wait_completion(self):
        self.queue.join()


if __name__ == "__main__":
    tq = TaskQueue(num_workers=3)
    tq.start()

    for task in ["A", "B", "C", "D", "E"]:
        tq.add_task(example_task, task)

    tq.wait_completion()
    tq.stop()