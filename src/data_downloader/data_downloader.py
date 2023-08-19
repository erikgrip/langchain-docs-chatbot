import os
import zipfile

import requests


def download_zip_file(url, save_path):
    """Download a ZIP file from a URL and save it to a local path."""
    save_dir = save_path.rsplit("/", 1)[0]
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    response = requests.get(url, stream=True, timeout=5)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    else:
        print(f"Failed to download the ZIP file. Status code: {response.status_code}")


def extract_files_by_extension(zip_file_path, target_extensions, output_dir):
    """Extract given filetypes from zip file."""
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        for file_name in zip_ref.namelist():
            if file_name.endswith(tuple(target_extensions)):
                zip_ref.extract(file_name, output_dir)
