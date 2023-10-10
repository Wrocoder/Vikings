import os
from unittest.mock import patch, Mock

import pandas as pd
import pytest
import yaml
from bs4 import BeautifulSoup

from Data_process.helper.helper import get_config, get_selenium_driver, get_dom, csv_load, \
    download_image_to_bytes

TEST_CONFIG_PATH = 'test_config.yaml'
TEST_IMAGE_URL = 'https://testo.com/test.jpg'
TEST_SAVE_DIR = 'testo_images/'
TEST_FILE_NAME = 'test_image.jpg'
TEST_CSV_DATA = [{'name': 'Actor 1', 'biography': 'Bio 1'}, {'name': 'Actor 2', 'biography': 'Bio 2'}]
TEST_CSV_FILE = 'testo.csv'
TEST_DB_FILE = 'testo_db.sqlite'
TEST_TABLE_NAME = 'actors'


@pytest.fixture
def setup_selenium():
    browser = get_selenium_driver()
    yield browser
    browser.quit()


def test_get_config(tmpdir):
    config_data = {'db': {'conf': 'test_db.conf'}}
    with open(os.path.join(tmpdir, TEST_CONFIG_PATH), 'w') as config_file:
        yaml.dump(config_data, config_file, default_flow_style=False)

    config = get_config(os.path.join(tmpdir, TEST_CONFIG_PATH), location='local')
    assert config == config_data


def test_get_dom(setup_selenium):
    browser = setup_selenium
    test_url = 'https://testo.com'

    soup = get_dom(test_url, browser)
    assert isinstance(soup, BeautifulSoup)


def test_csv_load(tmpdir):
    test_csv_path = os.path.join(tmpdir, TEST_CSV_FILE)
    csv_load(TEST_CSV_DATA, test_csv_path)
    assert os.path.exists(test_csv_path)
    df = pd.read_csv(test_csv_path)
    assert df.to_dict(orient='records') == TEST_CSV_DATA


# def test_get_img(tmpdir):
#     test_save_path = os.path.join(tmpdir, TEST_SAVE_DIR)
#     os.makedirs(test_save_path, exist_ok=True)
#     test_image_path = os.path.join(test_save_path, TEST_FILE_NAME + '.jpg')
#
#     image = get_img(TEST_IMAGE_URL, test_save_path, TEST_FILE_NAME)
#     assert os.path.exists(test_image_path)
#
#     assert isinstance(image, Image.Image)


# def test_db_load(tmpdir):
#     test_csv_path = os.path.join(tmpdir, TEST_CSV_FILE)
#     csv_load(TEST_CSV_DATA, test_csv_path)
#
#     test_db_path = os.path.join(tmpdir, TEST_DB_FILE)
#     db_load(test_csv_path, TEST_TABLE_NAME)
#     assert os.path.exists(test_db_path)


@patch('requests.get')
def test_download_image_to_bytes(mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b'Test Image Data'
    mock_requests_get.return_value = mock_response

    image_bytes = download_image_to_bytes(TEST_IMAGE_URL)

    assert isinstance(image_bytes, bytes)
    assert image_bytes == b'Test Image Data'
