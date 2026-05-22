import queue
import threading
import time

"""
Visually Mapping the Lifecycle
Think of the lifecycle as a two-stage filter that collapses down to a clean exit:
	1.	queue.join() ensures the backlog of tasks drops to zero.
	2.	The Poison Pill (None) is injected into the empty queue.
	3.	thread.join() ensures the operating system completely tears down the worker infrastructure, freeing up memory.
"""

class TaskQueueManager:
    def __init__(self, num_workers=3):
        self.num_workers = num_workers
        self.task_queue = queue.Queue()
        self.workers = []
        self._is_running = False

    def _worker_loop(self):
        """Internal loop executed by each worker thread."""
        while True:
            # Blocks until an item is available
            task = self.task_queue.get()
            
            # Poison pill pattern for graceful shutdown
            if task is None:
                self.task_queue.task_done()
                break
                
            # Execute the task
            func, args, kwargs = task
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(f"Error executing task: {e}")
            finally:
                # Always mark the task as done, even if it failed
                self.task_queue.task_done()

    def start(self):
        """Spins up the worker threads."""
        if self._is_running:
            print("Workers are already running.")
            return
            
        self._is_running = True
        for i in range(self.num_workers):
            t = threading.Thread(
                            target=self._worker_loop, 
                            daemon=True # Daemon ensures threads die if main process crashes
                        )
            t.start()
            self.workers.append(t)
        print(f"Started {self.num_workers} worker threads.")

    def add_task(self, func, *args, **kwargs):
        """Enqueues a function and its arguments as a task."""
        self.task_queue.put((func, args, kwargs))

    def join(self):
        """Blocks until all current tasks in the queue are processed."""
        self.task_queue.join()

    def stop(self):
        """Gracefully stops all worker threads."""
        if not self._is_running:
            return
            
        # Inject a poison pill for each worker
        for _ in range(self.num_workers):
            self.task_queue.put(None)
            
        # Wait for all worker threads to finish their current task and exit
        for t in self.workers:
            t.join()
            
        self.workers = []
        self._is_running = False
        print("All workers stopped gracefully.")


# --- Interview Demonstration / Usage Example ---
if __name__ == "__main__":
    # Sample task function
    def example_io_bound_task(name, delay):
        print(f"  Starting task: {name}")
        time.sleep(delay)
        print(f"  Finished task: {name}")

    # Initialize and start the queue manager
    manager = TaskQueueManager(num_workers=2)
    manager.start()

    # Add tasks dynamically
    manager.add_task(example_io_bound_task, "Download Image A", 1.5)
    manager.add_task(example_io_bound_task, "Fetch API Data", 0.5)
    manager.add_task(example_io_bound_task, "Write Log Entry", 1.0)

    print("Main thread: All tasks sent to queue. Waiting for completion...")
    manager.join()
    print("Main thread: All tasks are complete!")

    # Clean up resources
    manager.stop()
