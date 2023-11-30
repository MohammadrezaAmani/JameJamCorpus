import asyncio
import aiohttp
from .config import START, END, BASE_URL


async def fetch_data(url):
    """
    Fetches data from the specified URL using the aiohttp library.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        dict: The JSON-formatted data fetched from the URL.

    Raises:
        Exception: If an error occurs while fetching the data.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                # Check if the response status is 200 (success)
                return response.text  # Return the JSON-formatted data
            else:
                # Raise an exception if the response status is not 200
                raise Exception(f"Failed to fetch data from {url}: {response.status}")


async def main():
    """
    Creates and executes tasks to fetch data from multiple URLs concurrently.

    The function creates a list of URLs, each with a dynamic ID ranging from 1000 to 1999. It then creates a list of asyncio tasks, each responsible for fetching data from a corresponding URL. The `asyncio.gather()` function is used to wait for all tasks to complete before printing the results.
    """
    # Define the base URL and the range of dynamic IDs
    base_url = BASE_URL
    dynamic_id_range = range(START, END)

    # Construct a list of URLs with dynamic IDs
    urls = [f"{base_url}{i}" for i in dynamic_id_range]

    # Create a list of asyncio tasks
    tasks = [asyncio.create_task(fetch_data(url)) for url in urls]

    # Wait for all tasks to complete and gather their results
    results = await asyncio.gather(*tasks)

    # Print the results
    print(results)


if __name__ == "__main__":
    # Run the main function using asyncio.run()
    asyncio.run(main())
