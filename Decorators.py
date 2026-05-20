import functools
import time


def monitor_execution(func):
    """Simple decorator: add behavior before/after a function runs."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()

        try:
            result = func(*args, **kwargs)
            print(f"{func.__name__}: SUCCESS")
            return result
        except Exception as exc:
            print(f"{func.__name__}: FAILED ({exc})")
            raise
        finally:
            duration = time.perf_counter() - start
            print(f"{func.__name__}: took {duration:.4f}s")

    return wrapper


def repeat(times):
    """Parameterized decorator: accepts arguments before wrapping a function."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None

            for attempt in range(1, times + 1):
                print(f"Run {attempt}/{times}")
                result = func(*args, **kwargs)

            return result

        return wrapper

    return decorator


def require_role(required_role):
    """Parameterized decorator commonly used for authorization checks."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(user, *args, **kwargs):
            if user.get("role") != required_role:
                raise PermissionError(
                    f"{user['name']} needs role '{required_role}'"
                )

            return func(user, *args, **kwargs)

        return wrapper

    return decorator


@monitor_execution
def process_video_task(task_name, duration=0.5):
    print(f"Processing video task: {task_name}")
    time.sleep(duration)
    return "video-ready.mp4"


@repeat(times=3)
def send_notification(message):
    print(f"Sending notification: {message}")


@monitor_execution
@require_role("admin")
def delete_user(user, username):
    print(f"{user['name']} deleted user: {username}")


def show_function_metadata(func):
    print(f"name: {func.__name__}")
    print(f"doc: {func.__doc__}")


if __name__ == "__main__":
    print("\n--- Basic decorator ---")
    output_file = process_video_task("compress-upload")
    print(f"Result: {output_file}")

    print("\n--- Parameterized decorator ---")
    send_notification("Build completed")

    print("\n--- Stacked decorators ---")
    admin = {"name": "Suyash", "role": "admin"}
    delete_user(admin, "test_user")

    print("\n--- Metadata preserved by functools.wraps ---")
    show_function_metadata(process_video_task)

    print("\n--- Authorization failure example ---")
    guest = {"name": "Guest", "role": "viewer"}
    try:
        delete_user(guest, "test_user")
    except PermissionError as exc:
        print(f"Blocked: {exc}")
