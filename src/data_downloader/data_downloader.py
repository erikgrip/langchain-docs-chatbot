import requests


URL = "https://github.com/erikgrip/swedish_parliament_motion_summarization/archive/refs/heads/main.zip"  # pylint: disable=line-too-long
SAVE_PATH = "test.zip"


def download_zip_file(url, save_path):
    """Download a ZIP file from a URL and save it to a local path."""
    response = requests.get(url, stream=True, timeout=5)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    else:
        print(f"Failed to download the ZIP file. Status code: {response.status_code}")
