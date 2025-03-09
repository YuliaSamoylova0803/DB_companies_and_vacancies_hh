import logging
from abc import ABC, abstractmethod
from pprint import pprint
from typing import Optional

import psycopg2

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class DB(ABC):
    """Абстрактный класс для работы с базами данных."""

    pass

    @abstractmethod
    def get_companies_and_vacancies_count(self):
        """Метод получения списка всех компаний и количество вакансий у каждой компании"""
        pass

    @abstractmethod
    def get_all_vacancies(self):
        """Метод получения списка всех вакансий с указанием названий компании, названия вакансии, зарплаты и ссылки"""
        pass

    @abstractmethod
    def get_avg_salary(self):
        """Метод получения средней зарплаты по вакансиям"""
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self):
        """Метод получения списка всех вакансий, у которых зарплата выше средней по всем по всем вакансиям"""
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self):
        """Метод получения списка всех вакансий, в названии которых содержатся переданные в метод слова, н-р python"""
        pass


class DBManager(DB):
    """Класс для подключения к БД PostgreSQL и выполнения запросов."""

    def __init__(self, dbname: str, user: str, password: str, host: str = "localhost", port: str = "5432") -> None:
        """
        Инициализация подключения к базе данных.
        :param dbname: Имя базы данных
        :param user: Имя пользователя
        :param password: Пароль
        :param host: Хост (по умолчанию localhost)
        :param port: Порт (по умолчанию 5432)
        """
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    def __del__(self) -> None:
        """Закрытие соединения с базой данных при удалении объекта."""
        if self.conn:
            self.conn.close()

    def get_companies_and_vacancies_count(self) -> list[tuple[str, int]]:
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        :return: Список кортежей (название компании, количество вакансий)
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT c.name, COUNT(v.vacancy_id)
                    FROM companies c
                    LEFT JOIN vacancies v ON c.company_id = v.company_id
                    GROUP BY c.name;
                """
                )
                return cur.fetchall()
        except Exception as e:
            logging.error(f"Ошибка при получении списка компаний и количества вакансий: {e}")
            return []

    def get_all_vacancies(self) -> list[tuple[str, str, Optional[int], Optional[int], str, str]]:
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.
        :return: Список кортежей (название компании, название вакансии, зарплата от, зарплата до, валюта, ссылка)
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT c.name, v.title, v.salary_from, v.salary_to, v.currency, v.link
                    FROM vacancies v
                    JOIN companies c ON v.company_id = c.company_id;
                """
                )
                return cur.fetchall()
        except Exception as e:
            logging.error(f"Ошибка при получении списка вакансий: {e}")
            return []

    def get_avg_salary(self) -> float:
        """
        Получает среднюю зарплату по вакансиям.
        :return: Средняя зарплата (float)
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT AVG((salary_from + salary_to) / 2)
                    FROM vacancies
                    WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL;
                """
                )
                return cur.fetchone()[0]
        except Exception as e:
            logging.error(f"Ошибка при получении средней зарплаты: {e}")
            return 0

    def get_vacancies_with_higher_salary(self) -> list[tuple[str, str, Optional[int], Optional[int], str, str]]:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :return: Список кортежей (название компании, название вакансии, зарплата от, зарплата до, валюта, ссылка)
        """
        try:
            avg_salary = self.get_avg_salary()
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT c.name, v.title, v.salary_from, v.salary_to, v.currency, v.link
                    FROM vacancies v
                    JOIN companies c ON v.company_id = c.company_id
                    WHERE (v.salary_from + v.salary_to) / 2 > %s;
                """,
                    (avg_salary,),
                )
                return cur.fetchall()
        except Exception as e:
            logging.error(f"Ошибка при получении вакансий с зарплатой выше средней: {e}")
            return []

    def get_vacancies_with_keyword(self, keyword) -> list[tuple[str, str, Optional[int], Optional[int], str, str]]:
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова.
        :param keyword: Ключевое слово для поиска
        :return: Список кортежей (название компании, название вакансии, зарплата от, зарплата до, валюта, ссылка)
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT c.name, v.title, v.salary_from, v.salary_to, v.currency, v.link
                    FROM vacancies v
                    JOIN companies c ON v.company_id = c.company_id
                    WHERE LOWER(v.title) LIKE %s;
                """,
                    (f"%{keyword.lower()}%",),
                )
                return cur.fetchall()
        except Exception as e:
            logging.error(f"Ошибка при поиске вакансий по ключевому слову: {e}")
            return []


if __name__ == "__main__":
    # Параметры подключения к базе данных
    dbname = "list_employers"
    user = "postgres"
    password = "10yulia02"
    host = "localhost"
    port = "5432"

    # Создание экземпляра DBManager
    db_manager = DBManager(dbname, user, password, host, port)

    # Пример использования методов
    print("Компании и количество вакансий:")
    pprint(db_manager.get_companies_and_vacancies_count())

    print("\nВсе вакансии:")
    pprint(db_manager.get_all_vacancies())

    print("\nСредняя зарплата:")
    pprint(db_manager.get_avg_salary())

    print("\nВакансии с зарплатой выше средней:")
    pprint(db_manager.get_vacancies_with_higher_salary())

    print("\nВакансии с ключевым словом 'python':")
    pprint(db_manager.get_vacancies_with_keyword("смета"))
