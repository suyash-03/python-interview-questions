import time

TTL_DEFAULT = 300  # Default time-to-live for cache entries in seconds
cache = {}

async def fetch_data_by_id(id: str) -> dict:
    if id in cache and (time.time() - cache[id]["timestamp"] < TTL_DEFAULT):
        print("Cache hit for ID:", id)
        return cache[id]["data"]
    # Simulate data fetching
    data = {"id": id, "value": f"Data for {id}"}
    cache[id] = {"data": data, "timestamp": time.time()}
    print("Cache miss for ID:", id)
    return data

async def invalidate_cache(id: str):
    if id in cache:
        cache.pop(id)
        print("Cache invalidated for ID:", id)
    else:
        print("No cache entry to invalidate for ID:", id)   

# Example usage:
import asyncio
async def main():
    data1 = await fetch_data_by_id("123")
    print(data1)
    data2 = await fetch_data_by_id("123")  # Should hit cache
    print(data2)
    await invalidate_cache("123")
    data3 = await fetch_data_by_id("123")  # Should miss cache again
    print(data3)

asyncio.run(main())