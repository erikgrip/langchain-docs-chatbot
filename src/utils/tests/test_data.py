# pylint: disable=missing-docstring
import os
import zipfile
from unittest.mock import patch

import pytest

from src.data_downloader.data_downloader import (
    download_zip_file,
    extract_files_by_extension,
)

# Define the mock zip file content and target extensions
MOCK_ZIP_CONTENT = [
    "file1.txt",
    "file2.jpg",
    "file3.png",
    "subfolder/file4.txt",
]

# Define a temporary directory for testing
TEST_OUTPUT_DIR = "data/test_output/"


@pytest.fixture(name="test_data")
def test_data_fixture(tmpdir):
    url = "https://example.com/test.zip"
    save_path = os.path.join(tmpdir, "test.zip")
    return url, save_path


@pytest.fixture(name="create_mock_zip")
def create_mock_zip_fixture(tmpdir):
    zip_file_path = os.path.join(str(tmpdir), "test.zip")

    with zipfile.ZipFile(zip_file_path, "w") as zipf:
        for file_name in MOCK_ZIP_CONTENT:
            zipf.writestr(file_name, "mock content")

    yield zip_file_path


@pytest.fixture(name="cleanup_test_output")
def cleanup_test_output_fixture():
    yield
    if os.path.exists(TEST_OUTPUT_DIR):
        for root, dirs, files in os.walk(TEST_OUTPUT_DIR, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(TEST_OUTPUT_DIR)


def test_download_zip_file(test_data):
    url, save_path = test_data

    # Fake the requests.get function response
    response_content = b"Mocked content"
    with patch("requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.iter_content.return_value = [response_content]

        download_zip_file(url, save_path)

    assert os.path.exists(save_path)
    with open(save_path, "rb") as f:
        assert f.read() == response_content


def test_extract_files_by_extension(
    create_mock_zip, cleanup_test_output
):  # pylint: disable=unused-argument
    zip_file_path = create_mock_zip
    target_extensions = (".txt", ".png")
    output_dir = TEST_OUTPUT_DIR

    extract_files_by_extension(zip_file_path, target_extensions, output_dir)

    extracted_files = os.listdir(output_dir)

    assert "file1.txt" in extracted_files
    assert "file3.png" in extracted_files
    assert "file2.jpg" not in extracted_files
    assert "subfolder/file4.txt" not in extracted_files
