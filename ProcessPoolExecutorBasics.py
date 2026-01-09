import concurrent.futures
import time
import math

def cpu_heavy_task(n):
    """A simulation of a CPU-heavy calculation (CPU bound)."""
    start_time = time.time()
    count = 0
    # A simple, inefficient way to burn CPU cycles
    while time.time() - start_time < 1:
        count += math.sqrt(n) # Intense calculation
    return f"Task with input {n} finished calculation in ~1s"


if __name__ == "__main__":

    INPUT_VALUES = [50000, 50001, 50002, 50003]
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        results = executor.map(cpu_heavy_task, INPUT_VALUES)

    for result in results:
        print(result)