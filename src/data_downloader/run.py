import os

from src.data_downloader.data_downloader import (
    download_zip_file,
    extract_files_by_extension,
)
from src.utils.log import logger


URL = "https://github.com/langchain-ai/langchain/archive/refs/heads/master.zip"
SAVE_PATH = "data/zipped/tmp.zip"
TARGET_EXTENSIONS = [".md", ".mdx"]
OUTPUT_PATH = "data/unzipped/"

# Avoid downloading over and over for now
if not os.path.exists(SAVE_PATH):
    logger.info("Downloading the repository from %s.", URL)
    download_zip_file(URL, SAVE_PATH)
else:
    logger.info("Using previously downloaded file %s.", SAVE_PATH)
extract_files_by_extension(SAVE_PATH, TARGET_EXTENSIONS, OUTPUT_PATH)
