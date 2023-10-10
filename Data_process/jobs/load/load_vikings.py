from Data_process.helper.helper import get_config, db_load
from Data_process.logger import LOGGER


def main_load_vikings():
    CONFIG = get_config()
    file_path = CONFIG['scraper']['vikings']['filePath']
    table_name = CONFIG['scraper']['vikings']['tableName']

    db_load(file_path, table_name)


if __name__ == "__main__":
    LOGGER.info("Starting process")
    main_load_vikings()

