import asyncio

counter = 0
lock = asyncio.Lock()

async def increment():
    global counter

    async with lock:
        current = counter
        await asyncio.sleep(0.1)
        counter = current + 1

async def main():
    await asyncio.gather(
        increment(),
        increment(),
        increment(),
    )

    print(counter)

asyncio.run(main())

# In this example, we have a shared counter variable that multiple async tasks are trying to increment. To prevent race conditions and ensure that only one task can modify the counter at a time, we use an asyncio.Lock(). The async with lock: statement ensures that the block of code that modifies the counter is executed by only one task at a time, preventing data corruption and ensuring thread safety in an asynchronous context.
# Asyncio.lock are non-reentrant, meaning that if a task tries to acquire the same lock it already holds, it will result in a deadlock. Always ensure that locks are used correctly to avoid such issues.