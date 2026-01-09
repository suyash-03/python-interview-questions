import concurrent.futures


def add(x, y):
    return x + y


if __name__ == "__main__":
    # Using ThreadPoolExecutor to perform addition in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for i in range(10):
            futures.append(executor.submit(add, i, i+1))
        
        for future in concurrent.futures.as_completed(futures):
            print(f"Result: {future.result()}")