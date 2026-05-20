import asyncio
import requests

def make_api_call(url):
    result = requests.get(url)
    return result.json()

    # with urllib.request.urlopen(url) as response:
        # return json.loads(response.read().decode())
    
    # requests is a third party library that provides a more user-friendly API for making HTTP requests compared to urllib.request. It is widely used in the Python community for its simplicity and ease of use. However, it is a blocking library, which means that it will block the execution of your program while waiting for a response from the server. This can be problematic in an asynchronous context, as it can prevent other tasks from running concurrently. To work around this, you can use asyncio.to_thread() to run the blocking requests.get() function in a separate thread, allowing your async code to continue running without being blocked.

async def main():
    results = await asyncio.gather(
        asyncio.to_thread(make_api_call, 'https://fake-json-api.mock.beeceptor.com/users'),
        asyncio.to_thread(make_api_call, 'https://fake-json-api.mock.beeceptor.com/companies')
    )
    print(results) 

if __name__ == "__main__":
    asyncio.run(main())


# urllib.request: Python's standard, built-in library for making HTTP requests.requests is blocking: It stops the entire event loop while waiting for the network.asyncio.to_thread(): Safely runs blocking functions in a separate thread so your async loop keeps running.
# In this example, we use asyncio.to_thread() to run the blocking make_api_call function in a separate thread, allowing our main async function to await the results without blocking the event loop.
# asyncio.gather(): A convenient way to run multiple async tasks concurrently and wait for all of them to finish. It returns a list of results in the same order as the input tasks.
# If you want to make actual asynchronous HTTP requests, consider using aiohttp instead of requests, which is designed for async programming.
    
