import asyncio
import logging
import time

import aiohttp

from jamejam import STARTTIME
from jamejam.config import BASE_URL, DEBUG, END, MAX_CALLS_PER_SECOND, START
from jamejam.utils.process import extract_data
from jamejam.utils.save import add_to_db
from jamejam.utils.url import prepare_urls

if DEBUG:
    logging.basicConfig(level=logging.INFO)


async def fetch_data(url: str, semaphore: asyncio.Semaphore):
    count = 0
    id = int(url.split("/")[-1])
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        text = await response.text()
                        data = extract_data(text)
                        data["id"] = id
                        await add_to_db(data)
                        if DEBUG:
                            speed = (id - START + 1) / (STARTTIME - time.time())
                            remaining = (END + START - id - 1) / speed
                            logging.info(
                                f"Data fetched from {url}, {id}/{END} remaining: {remaining}, {speed} p/s"
                            )
                    else:
                        raise Exception(
                            f"Failed to fetch data from {url}: {response.status}"
                        )
            except Exception as e:
                if DEBUG:
                    logging.error(
                        f"Failed to fetch data from {id}: {str(e)[:60 if len(str(e)) > 60 else len(str(e))]}"
                    )
                while count < 5:
                    count += 1
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
                        break
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

    # with ProcessPoolExecutor(30) as executor:
    #     tasks = [
    #         executor.submit(synchronous_fetch_data, url, semaphore) for url in urls
    #     ]
    #     for task in tasks:
    #         task.result()

    tasks = [fetch_data(url, semaphore) for url in urls]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
