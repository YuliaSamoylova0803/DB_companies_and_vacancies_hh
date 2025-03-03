import logging
import unittest

import psycopg2

from src.utils import create_and_fill_tables

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Тестовые данные
TEST_DATA = {
    "company_1": {
        "company_name": "Test Company 1",
        "company_url": "https://testcompany1.com",
        "vacancies": [
            {
                "vacancy_id": "vacancy_1",
                "vacancy_name": "Test Vacancy 1",
                "salary_from": 50000,
                "salary_to": 70000,
                "currency": "RUB",
                "url": "https://testcompany1.com/vacancy_1",
            }
        ],
    },
    "company_2": {
        "company_name": "Test Company 2",
        "company_url": "https://testcompany2.com",
        "vacancies": [
            {
                "vacancy_id": "vacancy_2",
                "vacancy_name": "Test Vacancy 2",
                "salary_from": 60000,
                "salary_to": 80000,
                "currency": "USD",
                "url": "https://testcompany2.com/vacancy_2",
            }
        ],
    },
}

# Параметры подключения к тестовой базе данных
TEST_DB_NAME = "test_database"
TEST_PARAMS = {
    "user": "postgres",
    "password": "10yulia02",
    "host": "localhost",
    "port": "5432",
}


class TestCreateAndFillTables(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Подготовка тестовой базы данных."""
        # Подключение к базе данных postgres для создания тестовой базы
        conn = psycopg2.connect(dbname="postgres", **TEST_PARAMS)
        conn.autocommit = True
        cur = conn.cursor()

        # Удаление базы данных, если она существует
        cur.execute(f"DROP DATABASE IF EXISTS {TEST_DB_NAME};")
        logging.info(f"База данных {TEST_DB_NAME} удалена, если существовала.")

        # Создание новой базы данных
        cur.execute(f"CREATE DATABASE {TEST_DB_NAME};")
        logging.info(f"База данных {TEST_DB_NAME} успешно создана.")

        cur.close()
        conn.close()

    def setUp(self):
        """Подключение к тестовой базе данных перед каждым тестом."""
        self.conn = psycopg2.connect(dbname=TEST_DB_NAME, **TEST_PARAMS)
        self.cur = self.conn.cursor()

    def tearDown(self):
        """Закрытие соединения после каждого теста."""
        self.cur.close()
        self.conn.close()

    def test_tables_creation(self):
        """Проверка создания таблиц companies и vacancies."""
        create_and_fill_tables(TEST_DB_NAME, TEST_PARAMS, TEST_DATA)

        # Проверка существования таблицы companies
        self.cur.execute(
            """
            SELECT EXISTS (
                SELECT FROM pg_tables
                WHERE tablename = 'companies'
            );
            """
        )
        companies_table_exists = self.cur.fetchone()[0]
        self.assertTrue(companies_table_exists, "Таблица companies не создана.")

        # Проверка существования таблицы vacancies
        self.cur.execute(
            """
            SELECT EXISTS (
                SELECT FROM pg_tables
                WHERE tablename = 'vacancies'
            );
            """
        )
        vacancies_table_exists = self.cur.fetchone()[0]
        self.assertTrue(vacancies_table_exists, "Таблица vacancies не создана.")

    def test_data_insertion(self):
        """Проверка заполнения таблиц данными."""
        create_and_fill_tables(TEST_DB_NAME, TEST_PARAMS, TEST_DATA)

        # Проверка данных в таблице companies
        self.cur.execute("SELECT COUNT(*) FROM companies;")
        companies_count = self.cur.fetchone()[0]
        self.assertEqual(companies_count, 2, "Не все компании добавлены в таблицу companies.")

        # Проверка данных в таблице vacancies
        self.cur.execute("SELECT COUNT(*) FROM vacancies;")
        vacancies_count = self.cur.fetchone()[0]
        self.assertEqual(vacancies_count, 2, "Не все вакансии добавлены в таблицу vacancies.")

    def test_data_correctness(self):
        """Проверка корректности данных в таблицах."""
        create_and_fill_tables(TEST_DB_NAME, TEST_PARAMS, TEST_DATA)

        # Проверка данных в таблице companies
        self.cur.execute("SELECT name, website FROM companies WHERE company_id = 'company_1';")
        company_data = self.cur.fetchone()
        self.assertEqual(company_data, ("Test Company 1", "https://testcompany1.com"), "Данные компании некорректны.")

        # Проверка данных в таблице vacancies
        self.cur.execute(
            "SELECT title, salary_from, salary_to, currency, link FROM vacancies WHERE vacancy_id = 'vacancy_1';"
        )
        vacancy_data = self.cur.fetchone()
        expected_vacancy_data = (
            "Test Vacancy 1",
            50000,
            70000,
            "RUB",
            "https://testcompany1.com/vacancy_1",
        )
        self.assertEqual(vacancy_data, expected_vacancy_data, "Данные вакансии некорректны.")

    @classmethod
    def tearDownClass(cls):
        """Удаление тестовой базы данных после всех тестов."""
        # Подключение к базе данных postgres для удаления тестовой базы
        conn = psycopg2.connect(dbname="postgres", **TEST_PARAMS)
        conn.autocommit = True
        cur = conn.cursor()

        # Удаление тестовой базы данных
        cur.execute(f"DROP DATABASE IF EXISTS {TEST_DB_NAME};")
        logging.info(f"База данных {TEST_DB_NAME} успешно удалена.")

        cur.close()
        conn.close()


if __name__ == "__main__":
    unittest.main()
