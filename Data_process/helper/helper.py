from io import BytesIO

import pandas as pd
import requests
import yaml
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from sqlalchemy import create_engine

pd.options.display.max_colwidth = 500
pd.options.display.max_columns = 10
pd.options.display.max_rows = 200
pd.options.display.width = 2000


def get_config(path='Data_process/config/conf.yaml', location='local'):
    if location == 'local':
        with open(path, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)
    else:
        raise RuntimeError


def get_selenium_driver():
    return webdriver.Chrome()


def get_dom(url, browser):
    browser.get(url)
    dom_html = browser.page_source
    return BeautifulSoup(dom_html, 'lxml')


def csv_load(data, file_name):
    df = pd.DataFrame(data)
    print(df)
    df.to_csv(file_name, index=True)


def get_img(img_url, save_directory, file_name):
    response = requests.get(img_url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image.save(save_directory + file_name + '.jpg')
        return image
    else:
        print("Failed to fetch the image. Status code:", response.status_code)


def db_load(file_path, table_name):
    CONFIG = get_config()
    conn_string = CONFIG['db']['conf']

    df = pd.read_csv(file_path)
    df.rename(columns={'Unnamed: 0': 'id'}, inplace=True)
    db = create_engine(conn_string)
    conn = db.connect()
    df.to_sql(table_name, con=conn, if_exists='replace', index=False)

    # conn.commit()
    conn.close()


def download_image_to_bytes(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        return BytesIO(response.content).read()
    else:
        return None
