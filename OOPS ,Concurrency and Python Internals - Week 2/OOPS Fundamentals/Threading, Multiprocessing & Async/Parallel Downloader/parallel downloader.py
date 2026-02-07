import aiohttp
import asyncio
import os

SAVE_DIR = "Parallel Downloader/files"
os.makedirs(SAVE_DIR, exist_ok=True)


async def download_file(session, url):
    filename = url.split("/")[-1]
    filepath = os.path.join(SAVE_DIR, filename)

    async with session.get(url) as response:
        response.raise_for_status()
        content = await response.read()
        with open(filepath, "wb") as f:
            f.write(content)
    print(f"{filename} downloaded to {SAVE_DIR}/")


async def main():
    urls = [
        "https://www.kaggle.com/datasets/ibrahimshahrukh/tesla-stock-price-historical-dataset-2010-2025",
        "https://www.kaggle.com/datasets/wardabilal/customer-shopping-behaviour-analysis",
        "https://www.kaggle.com/datasets/hassanjameelahmed/store-sales"
    ]
    async with aiohttp.ClientSession() as session:
        tasks = [download_file(session, url) for url in urls]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())