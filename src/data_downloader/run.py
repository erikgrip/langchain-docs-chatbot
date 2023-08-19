from src.data_downloader.data_downloader import download_zip_file, extract_files_by_extension


URL = "https://github.com/erikgrip/swedish_parliament_motion_summarization/archive/refs/heads/main.zip"  # pylint: disable=line-too-long
SAVE_PATH = "test.zip"
TARGET_EXTENSIONS = [".md", ".mdx"]
OUTPUT_PATH = "unzipped/"

download_zip_file(URL, SAVE_PATH)
extract_files_by_extension(SAVE_PATH, TARGET_EXTENSIONS, OUTPUT_PATH )
