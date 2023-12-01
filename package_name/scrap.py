import asyncio
import aiohttp
from .config import START, END, BASE_URL
from package_name.utils.process import extract_data
from package_name.utils.save import add_to_db


async def fetch_data(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                text = await response.text()
                data = extract_data(text)
                data["id"] = url.split("/")[-1]
                await add_to_db(data)
            else:
                raise Exception(f"Failed to fetch data from {url}: {response.status}")


async def main():
    base_url = BASE_URL
    dynamic_id_range = range(START, END)
    urls = [f"{base_url}{i}" for i in dynamic_id_range]
    tasks = [asyncio.create_task(fetch_data(url)) for url in urls]
    results = await asyncio.gather(*tasks)

    print(results)


if __name__ == "__main__":
    asyncio.run(main())
