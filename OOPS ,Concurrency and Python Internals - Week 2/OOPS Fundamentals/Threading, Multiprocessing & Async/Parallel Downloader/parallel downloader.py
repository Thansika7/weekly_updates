import aiohttp
import asyncio
import os

Directory = "Parallel Downloader/files"
LINKS_FILE = "Parallel Downloader/files\links.txt"

os.makedirs(Directory, exist_ok=True)


def get_links():
    print("Enter file URLs to download (type 'download' to download the files):")

    with open(LINKS_FILE, "w") as f:
        while True:
            url = input("Link: ").strip()
            if url.lower() == "download":
                break
            if url:
                f.write(url + "\n")

def read_links():
    with open(LINKS_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]


async def download_file(session, url):
    filename = url.split("/")[-1]
    filepath = os.path.join(Directory, filename)

    try:
        async with session.get(url) as response:
            response.raise_for_status()
            content = await response.read()

            with open(filepath, "wb") as f:
                f.write(content)

        print(f"Downloaded: {filename}")

    except Exception as e:
        print(f"Failed to download {url} | Error: {e}")


async def main():
    urls = read_links()

    if not urls:
        print("No links found in links.txt")
        return

    async with aiohttp.ClientSession() as session:
        tasks = [download_file(session, url) for url in urls]
        await asyncio.gather(*tasks)

    print("\nAll downloads completed.")


if __name__ == "__main__":
    get_links()
    asyncio.run(main())
