import logging
from pathlib import Path

import psycopg2

from setting import BASE_DIR
from src.get_hh_api import get_data, hh_api

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

json_filename = Path(BASE_DIR, "data", "employers_data.json").parent
database_path = Path(BASE_DIR, "src", "database.ini").parent


data = hh_api()
data_list = get_data(data)


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def create_and_fill_tables(database_name: str, params: dict, data_list: dict) -> None:
    """
    Создаёт базу данных, таблицы companies и vacancies, если они не существуют,
    и заполняет их данными из data_list.
    """
    try:
        # Подключение к базе данных
        conn = psycopg2.connect(dbname=database_name, **params)
        conn.autocommit = True
        cur = conn.cursor()

        # Создание таблицы companies
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS companies (
                company_id VARCHAR(20) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                website VARCHAR(255)
            );
            """
        )
        logging.info("Таблица companies создана или уже существует.")

        # Создание таблицы vacancies
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id VARCHAR(20) PRIMARY KEY,
                company_id VARCHAR(20) REFERENCES companies(company_id),
                title VARCHAR(255) NOT NULL,
                salary_from INT,
                salary_to INT,
                currency VARCHAR(10),
                link VARCHAR(255) NOT NULL
            );
            """
        )
        logging.info("Таблица vacancies создана или уже существует.")

        # Заполнение таблицы companies
        for company_id, company_data in data_list.items():
            cur.execute(
                """
                INSERT INTO companies (company_id, name, website)
                VALUES (%s, %s, %s)
                ON CONFLICT (company_id) DO NOTHING;
                """,
                (company_id, company_data["company_name"], company_data["company_url"]),
            )
            logging.info(f"Данные компании {company_data['company_name']} добавлены.")

            # Заполнение таблицы vacancies
            for vacancy in company_data["vacancies"]:
                cur.execute(
                    """
                    INSERT INTO vacancies (vacancy_id, company_id, title, salary_from, salary_to, currency, link)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (vacancy_id) DO NOTHING;
                    """,
                    (
                        vacancy["vacancy_id"],
                        company_id,
                        vacancy["vacancy_name"],
                        vacancy["salary_from"],
                        vacancy["salary_to"],
                        vacancy["currency"],
                        vacancy["url"],
                    ),
                )
                logging.info(f"Вакансия {vacancy['vacancy_name']} добавлена.")

        conn.commit()
        logging.info("Данные успешно добавлены в таблицы companies и vacancies.")

    except psycopg2.Error as e:
        logging.error(f"Ошибка при создании базы данных или таблиц: {e}")
    finally:
        if conn:
            conn.close()
