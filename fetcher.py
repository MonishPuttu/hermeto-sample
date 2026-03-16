import aiohttp
import asyncio
from pathlib import Path


MAX_CONCURRENT_DOWNLOADS = 10
RETRIES = 3


async def async_download(session, url, package_name, version, output_root, semaphore):
    filename = url.split("/")[-1]

    pkg_dir = Path(output_root) / package_name / version
    pkg_dir.mkdir(parents=True, exist_ok=True)

    path = pkg_dir / filename

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


async def download_many(jobs, output_root):

    semaphore = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)

    timeout = aiohttp.ClientTimeout(total=60)

    async with aiohttp.ClientSession(timeout=timeout) as session:

        tasks = []

        for job in jobs:
            tasks.append(
                async_download(
                    session,
                    job["url"],
                    job["name"],
                    job["version"],
                    output_root,
                    semaphore
                )
            )

        return await asyncio.gather(*tasks)