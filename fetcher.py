import aiohttp
import asyncio


MAX_CONCURRENT_DOWNLOADS = 10
RETRIES = 3


async def async_download(session, url, output_dir, semaphore):
    filename = url.split("/")[-1]
    path = output_dir / filename

    async with semaphore:

        for attempt in range(RETRIES):

            try:
                async with session.get(url) as resp:

                    if resp.status != 200:
                        raise RuntimeError(f"Download failed {url} status={resp.status}")

                    data = await resp.read()

                with open(path, "wb") as f:
                    f.write(data)

                return path

            except Exception:

                if attempt == RETRIES - 1:
                    raise

                await asyncio.sleep(1)


async def download_many(urls, output_dir):

    semaphore = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)

    timeout = aiohttp.ClientTimeout(total=60)

    async with aiohttp.ClientSession(timeout=timeout) as session:

        tasks = []

        for url in urls:
            tasks.append(async_download(session, url, output_dir, semaphore))

        return await asyncio.gather(*tasks)