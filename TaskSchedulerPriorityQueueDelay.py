import heapq
import time

def example_task(task_id):
    print(f"Executing task {task_id}")

class TaskScheduler:
    def __init__(self):
        self.taskQueue = []
    
    def schedule(self, func, *args, delay=0):
        run_at = time.time() + delay
        heapq.heappush(self.taskQueue, (run_at, func, args))

    def run(self):
        while self.taskQueue:
            run_at, func, args = heapq.heappop(self.taskQueue)
            now = time.time()
            if run_at > now:
                time.sleep(run_at - now)
            func(*args)


if __name__ == "__main__":
    scheduler = TaskScheduler()
    scheduler.schedule(example_task, "A", delay=2)
    scheduler.schedule(example_task, "B", delay=2)
    scheduler.schedule(example_task, "C", delay=1)
    scheduler.schedule(example_task, "D", delay=3)
    scheduler.run()
