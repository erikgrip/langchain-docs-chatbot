import os

# pylint: disable=missing-docstring

from unittest.mock import patch

import pytest

from src.data_downloader.data_downloader import download_zip_file


# Create a fixture for the URL and save_path
@pytest.fixture(name="test_data")
def test_data_fixture(tmpdir):
    url = "https://example.com/test.zip"
    save_path = os.path.join(tmpdir, "test.zip")
    return url, save_path


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
