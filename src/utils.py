import logging
import psycopg2
from config import config
from pathlib import Path
from setting import BASE_DIR
from src.get_hh_api import hh_api, get_data

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

json_filename = Path(BASE_DIR, "data", "employers_data.json").parent
database_path = Path(BASE_DIR, "src", "database.ini").parent
#params = config(database_path)

data = hh_api()
data_list = get_data(data)

def create_and_fill_tables(database_name: str, params: dict, data_list):
    """
    Создаёт базу данных, таблицы companies и vacancies, если они не существуют,
    и заполняет их данными из data_list.
    """

    try:
        # Подключение к базе данных по умолчанию (postgres)
        conn = psycopg2.connect(dbname="postgres", **params)
        conn.autocommit = True  # Включаем autocommit для создания базы данных
        cur = conn.cursor()

        # Создание базы данных, если она не существует
        cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
        logging.info(f"База данных c именем {database_name} уже существовала и была удалена.")
        cur.execute(f"CREATE DATABASE {database_name};")
        logging.info(f"База данных {database_name} успешно создана.")

        # Закрываем соединение с базой данных по умолчанию

        conn.close()

        # Подключение к новой базе данных
        conn = psycopg2.connect(dbname=database_name, **params)
        logging.info(f"Повторное подключение для создания таблиц.")

        with conn.cursor() as cur:
            # Создание таблицы companies
            cur.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                    company_id VARCHAR(20) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    website VARCHAR(255)
                );
            """)

            # Создание таблицы vacancies
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    vacancy_id VARCHAR(20) PRIMARY KEY,
                    company_id VARCHAR(20) REFERENCES companies(company_id),
                    title VARCHAR(255) NOT NULL,
                    salary_from INT,
                    salary_to INT,
                    currency VARCHAR(10),
                    link VARCHAR(255) NOT NULL
                );
            """)
            conn.commit()
            logging.info("Таблицы companies и vacancies успешно созданы.")


            # Заполнение таблицы companies
            for company_id, company_data in data_list.items():
                cur.execute("""
                    INSERT INTO companies (company_id, name, website)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (company_id) DO NOTHING;
                """, (company_id, company_data["company_name"], company_data["company_url"]))
                conn.commit()

                # Заполнение таблицы vacancies
                for vacancy in company_data["vacancies"]:
                    cur.execute("""
                        INSERT INTO vacancies (vacancy_id, company_id, title, salary_from, salary_to, currency, link)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (vacancy_id) DO NOTHING;
                    """, (
                        vacancy["vacancy_id"],
                        company_id,
                        vacancy["vacancy_name"],
                        vacancy["salary_from"],
                        vacancy["salary_to"],
                        vacancy["currency"],
                        vacancy["url"]
                    ))
                    conn.commit()

            logging.info("Данные успешно добавлены в таблицы companies и vacancies.")

    except psycopg2.Error as e:
        logging.error(f"Ошибка при создании базы данных или таблиц: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()



if __name__ == "__main__":
    # Параметры подключения к PostgreSQL
    dbname = "test_0103"  # Имя новой базы данных
    user = "postgres"
    password = "10yulia02"
    host = "localhost"
    port = "5432"

    # Создаём базу данных, таблицы и заполняем их данными
    create_and_fill_tables(dbname, params)


