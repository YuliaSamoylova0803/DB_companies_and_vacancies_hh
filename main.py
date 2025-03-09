import logging
from pathlib import Path
from config import config
from setting import BASE_DIR
from src.get_hh_api import get_data, hh_api
from src.utils import create_and_fill_tables
from src.dbmanager import DBManager

# Настройка логирования
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

        # Параметры подключения к базе данных
        dbname = "list_employers02"
        user = "postgres"
        password = "10yulia02"
        host = "localhost"
        port = "5432"

        # Создание экземпляра DBManager
        db_manager = DBManager(dbname=dbname, user=user, password=password, host=host, port=port)

        # Пример использования методов с человекочитаемым выводом
        print("=== Компании и количество вакансий ===")
        companies_vacancies = db_manager.get_companies_and_vacancies_count()
        for company, count in companies_vacancies:
            print(f"Компания: {company}, Количество вакансий: {count}")

        print("\n=== Все вакансии ===")
        all_vacancies = db_manager.get_all_vacancies()
        for vacancy in all_vacancies:
            print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата от: {vacancy[2]}, "
                  f"Зарплата до: {vacancy[3]}, Ссылка: {vacancy[4]}")

        print("\n=== Средняя зарплата ===")
        avg_salary = db_manager.get_avg_salary()
        print(f"Средняя зарплата по всем вакансиям: {avg_salary:.2f}")

        print("\n=== Вакансии с зарплатой выше средней ===")
        higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
        for vacancy in higher_salary_vacancies:
            print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата от: {vacancy[2]}, "
                  f"Зарплата до: {vacancy[3]}, Валюта: {vacancy[4]}, Ссылка: {vacancy[5]}")

        print("\n=== Вакансии с ключевым словом 'смета' ===")
        keyword_vacancies = db_manager.get_vacancies_with_keyword("смета")
        for vacancy in keyword_vacancies:
            print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата от: {vacancy[2]}, "
                  f"Зарплата до: {vacancy[3]}, Валюта: {vacancy[4]}, Ссылка: {vacancy[5]}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()