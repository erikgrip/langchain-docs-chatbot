import os
import zipfile

import requests

from src.utils.log import logger


def download_and_unzip(url, target_extensions, force_new_download=False):
    """
    Download a zip file from the given URL and extracts its contents.

    The contents of the zip file are extracted to atarget directory,
    filtering files by their extensions.

    Args:
        url (str): The URL of the zip file to download.
        target_extensions (list[str]): A list of file extensions to extract
        from the zip file.
        force_new_download (bool, optional): Whether to force a new download of the
        zip file, even if it already exists in the local filesystem. Defaults to False.

    Returns:
        str: The path to the directory where the zip file contents were extracted.
    """
    path_to_downloaded_zip = "data/zipped/tmp.zip"
    output_path = "data/unzipped/"

    os.makedirs(output_path, exist_ok=True)
    if not os.path.exists(path_to_downloaded_zip) and not force_new_download:
        logger.info("Downloading the repository from %s.", url)
        download_zip_file(url, path_to_downloaded_zip)
    else:
        logger.info("Using previously downloaded file %s.", path_to_downloaded_zip)
    logger.info(
        "Extracting files in %s with extensions %s to %s.",
        path_to_downloaded_zip,
        target_extensions,
        output_path,
    )
    extract_files_by_extension(path_to_downloaded_zip, target_extensions, output_path)
    return output_path


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
            logger.info("Downloaded zip file to %s directory", save_dir)
    else:
        logger.error("Failed to download the zip file: %s", response.status_code)


def extract_files_by_extension(zip_file_path, target_extensions, output_dir):
    """Extract given filetypes from zip file."""
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        for file_name in zip_ref.namelist():
            if file_name.endswith(tuple(target_extensions)):
                zip_ref.extract(file_name, output_dir)
