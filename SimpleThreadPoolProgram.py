import concurrent.futures


def add(x, y):
    return x + y


if __name__ == "__main__":

    # Using executor.submit() to perform multiple additions in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for i in range(10):
            futures.append(executor.submit(add, i, i+1))
        
        for future in concurrent.futures.as_completed(futures):
            print(f"Result: {future.result()}")

    # Using executor.map() to perform additions in parallel
    # Results are returned in the same order as the input values.
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        numbers = range(10)
        results = executor.map(add, numbers, [i + 1 for i in numbers])

        for result in results:
            print(f"Map result: {result}")
