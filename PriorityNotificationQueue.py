import heapq
import time

class NotificationPriorityService:
    def __init__(self):
        self.queue = []

    def add_notification_to_queue(self, priority: int, notification: str):
        heapq.heappush(self.queue, (priority, notification))

    def send_notification(self):
        if not self.queue:
            return

        priority, notification = heapq.heappop(self.queue)
        print(f"[Priority {priority}] {notification}")
        time.sleep(2)


def background_worker(service: NotificationPriorityService):
    ...


if __name__ == "__main__":
    nps = NotificationPriorityService()
    nps.add_notification_to_queue(1, "Sent on Email")
    nps.add_notification_to_queue(3, "Sent on WhatsApp")
    nps.add_notification_to_queue(2, "Sent on iMessage")

    # Simulate background worker
    while True:
        if nps.queue:
            nps.send_notification()
        else:
            time.sleep(1)  # avoid busy waiting