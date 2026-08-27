# android_adbkit/core/downloader.py
import requests
from tqdm import tqdm





def download_file(url, dest_path):
    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()

    total = int(response.headers.get("content-length", 0))
    bar = tqdm(total=total, unit="iB", unit_scale=True, desc="Download progress")

    with open(dest_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                bar.update(f.write(chunk))
    bar.close()