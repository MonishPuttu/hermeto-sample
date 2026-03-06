import requests

def download_artifact(url, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = url.split("/")[-1]
    file_path = output_dir / filename

    r = requests.get(url)

    with open(file_path, "wb") as f:
        f.write(r.content)

    return file_path