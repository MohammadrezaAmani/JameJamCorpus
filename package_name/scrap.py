import asyncio
import aiohttp
import logging
from concurrent.futures import ProcessPoolExecutor
from package_name.utils.url import prepare_urls
from package_name.utils.process import extract_data
from package_name.utils.save import add_to_db
from package_name.config import START, END, BASE_URL, MAX_CALLS_PER_SECOND, DEBUG

if DEBUG:
    logging.basicConfig(level=logging.INFO)


async def fetch_data(url: str, semaphore: asyncio.Semaphore):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        text = await response.text()
                        data = extract_data(text)
                        data["id"] = int(url.split("/")[-1])
                        await add_to_db(data)
                        if DEBUG:
                            logging.info(f"Data fetched from {url}")
                    else:
                        raise Exception(
                            f"Failed to fetch data from {url}: {response.status}"
                        )
            except Exception as e:
                if DEBUG:
                    logging.error(
                        f"Failed to fetch data from {url.split('/')[-1]}: {str(e)[:60 if len(str(e)) > 60 else len(str(e))]}"
                    )


def synchronous_fetch_data(url, semaphore):
    return asyncio.run(fetch_data(url, semaphore))


async def main():
    urls = prepare_urls(BASE_URL, START, END)
    semaphore = asyncio.Semaphore(MAX_CALLS_PER_SECOND)

    with ProcessPoolExecutor() as executor:
        tasks = [
            executor.submit(synchronous_fetch_data, url, semaphore) for url in urls
        ]
        for task in tasks:
            task.result()


if __name__ == "__main__":
    asyncio.run(main())
