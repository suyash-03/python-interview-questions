from collections import deque

class NotificationQueue:
    def __init__(self):
        self.queue = deque()

    def add_notification(self, notification: str):
        """Add a notification to the queue."""
        self.queue.append(notification)
    
    def send_notification(self):
        if self.queue:
            notification = self.queue.popleft()
            print(f"Sending notification: {notification}")
            return notification
    
    def is_empty(self) -> bool:
        return len(self.queue) == 0

    def size(self) -> int:
        return len(self.queue)
    
if __name__ == "__main__":
    nq = NotificationQueue()
    nq.add_notification("You have a new message.")
    nq.add_notification("Your download is complete.")
    
    while not nq.is_empty():
        nq.send_notification()