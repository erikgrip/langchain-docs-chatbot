import os

from src.data_downloader.data_downloader import (
    download_zip_file,
    extract_files_by_extension,
)


URL = "https://github.com/erikgrip/swedish_parliament_motion_summarization/archive/refs/heads/main.zip"  # pylint: disable=line-too-long  # noqa: E501
SAVE_PATH = "data/zipped/tmp.zip"
TARGET_EXTENSIONS = [".md", ".mdx"]
OUTPUT_PATH = "data/unzipped/"

# Avoid downloading over and over for now
if not os.path.exists(SAVE_PATH):
    print(f"Downloading the repository from {URL}")
    download_zip_file(URL, SAVE_PATH)
else:
    print(f"Using previously downloaded file {SAVE_PATH}")
extract_files_by_extension(SAVE_PATH, TARGET_EXTENSIONS, OUTPUT_PATH)
