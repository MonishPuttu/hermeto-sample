import requests
from pathlib import Path

CACHE_DIR = Path("cache/wheels")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def download(url):
    filename = url.split("/")[-1]
    path = CACHE_DIR / filename

    r = requests.get(url)

    with open(path, "wb") as f:
        f.write(r.content)

    return path
