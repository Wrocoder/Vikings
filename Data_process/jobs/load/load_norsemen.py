from Data_process.helper.helper import get_config, db_load
from Data_process.logger import LOGGER


def main_load_norsemen():
    CONFIG = get_config()
    file_path = CONFIG['scraper']['norsemen']['filePath']
    table_name = CONFIG['scraper']['norsemen']['tableName']

    db_load(file_path, table_name)


if __name__ == "__main__":
    LOGGER.info("Starting process")
    main_load_norsemen()
