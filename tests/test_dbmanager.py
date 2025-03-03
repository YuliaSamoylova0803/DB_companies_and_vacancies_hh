import logging
import unittest

import psycopg2

from src.dbmanager import DBManager  # Импортируем класс DBManager

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Параметры подключения к тестовой базе данных
TEST_DB_NAME = "test_dbmanager"
TEST_PARAMS = {
    "user": "postgres",
    "password": "10yulia02",
    "host": "localhost",
    "port": "5432",
}


class TestDBManager(unittest.TestCase):
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

        # Подключение к тестовой базе данных для создания таблиц и заполнения данными
        conn = psycopg2.connect(dbname=TEST_DB_NAME, **TEST_PARAMS)
        cur = conn.cursor()

        # Создание таблицы companies
        cur.execute(
            """
            CREATE TABLE companies (
                company_id VARCHAR(20) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                website VARCHAR(255)
            );
            """
        )

        # Создание таблицы vacancies
        cur.execute(
            """
            CREATE TABLE vacancies (
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

        # Заполнение таблицы companies
        cur.execute(
            """
            INSERT INTO companies (company_id, name, website)
            VALUES
                ('company_1', 'Test Company 1', 'https://testcompany1.com'),
                ('company_2', 'Test Company 2', 'https://testcompany2.com');
            """
        )

        # Заполнение таблицы vacancies
        cur.execute(
            """
            INSERT INTO vacancies (vacancy_id, company_id, title, salary_from, salary_to, currency, link)
            VALUES
                ('vacancy_1', 'company_1', 'Test Vacancy 1', 50000, 70000, 'RUB', 'https://testcompany1.com/vacancy_1'),
                ('vacancy_2', 'company_2', 'Test Vacancy 2', 60000, 80000, 'USD', 'https://testcompany2.com/vacancy_2');
            """
        )

        conn.commit()
        cur.close()
        conn.close()

    def setUp(self):
        """Подключение к тестовой базе данных перед каждым тестом."""
        self.db_manager = DBManager(TEST_DB_NAME, **TEST_PARAMS)

    def tearDown(self):
        """Закрытие соединения после каждого теста."""
        del self.db_manager

    def test_get_companies_and_vacancies_count(self):
        """Проверка метода get_companies_and_vacancies_count."""
        result = self.db_manager.get_companies_and_vacancies_count()
        expected = [("Test Company 2", 1), ("Test Company 1", 1)]
        self.assertEqual(result, expected, "Некорректный список компаний и количества вакансий.")

    def test_get_all_vacancies(self):
        """Проверка метода get_all_vacancies."""
        result = self.db_manager.get_all_vacancies()
        expected = [
            ("Test Company 1", "Test Vacancy 1", 50000, 70000, "RUB", "https://testcompany1.com/vacancy_1"),
            ("Test Company 2", "Test Vacancy 2", 60000, 80000, "USD", "https://testcompany2.com/vacancy_2"),
        ]
        self.assertEqual(result, expected, "Некорректный список всех вакансий.")

    def test_get_avg_salary(self):
        """Проверка метода get_avg_salary."""
        result = self.db_manager.get_avg_salary()
        expected = 65000.0  # (50000 + 70000 + 60000 + 80000) / 4
        self.assertEqual(result, expected, "Некорректная средняя зарплата.")

    def test_get_vacancies_with_higher_salary(self):
        """Проверка метода get_vacancies_with_higher_salary."""
        result = self.db_manager.get_vacancies_with_higher_salary()
        expected = [
            ("Test Company 2", "Test Vacancy 2", 60000, 80000, "USD", "https://testcompany2.com/vacancy_2"),
        ]
        self.assertEqual(result, expected, "Некорректный список вакансий с зарплатой выше средней.")

    def test_get_vacancies_with_keyword(self):
        """Проверка метода get_vacancies_with_keyword."""
        result = self.db_manager.get_vacancies_with_keyword("Test")
        expected = [
            ("Test Company 1", "Test Vacancy 1", 50000, 70000, "RUB", "https://testcompany1.com/vacancy_1"),
            ("Test Company 2", "Test Vacancy 2", 60000, 80000, "USD", "https://testcompany2.com/vacancy_2"),
        ]
        self.assertEqual(result, expected, "Некорректный список вакансий по ключевому слову.")

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
