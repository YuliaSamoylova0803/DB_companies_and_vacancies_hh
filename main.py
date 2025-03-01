import logging
from pathlib import Path

from config import config
from setting import BASE_DIR
from src.get_hh_api import get_data, hh_api
from src.utils import create_and_fill_tables

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
json_filename = Path(BASE_DIR, "data", "employers_data.json").parent
database_path = Path(BASE_DIR, "src", "database.ini").parent


def main():
    try:
        logging.info("Начало выполнения функции main.")
        data = hh_api()
        logging.info("Данные из API успешно получены.")
        data_list = get_data(data)
        logging.info("Данные успешно обработаны.")
        params = config()
        logging.info("Параметры подключения к базе данных загружены.")
        database_name = "list_employers02"
        create_and_fill_tables(database_name, params, data_list)
        logging.info(f"База данных {database_name} успешно создана и заполнена.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
