from abc import ABC, abstractmethod


class DB(ABC):
    """Абстрактный класс для работы с базами данных."""
    pass

    @abstractmethod
    def get_companies_and_vacancies_count(self):
        """Метод получения списка всех компаний и количество вакансий у каждой компании"""
        pass

    @abstractmethod
    def get_all_vacancies(self):
        """Метод получения списка всех вакансий с указанием названий компании, названия вакансии и зарплаты и ссылки на вакансию"""
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
    def get_vacancies_with_keybord(self):
        """Метод получения списка всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        pass


class DBManager(DB):
    """Класс для подключения к БД PostgreSQL"""

    def get_companies_and_vacancies_count(seif):
        """Метод получения списка всех компаний и количество вакансий у каждой компании"""
        pass

    def get_all_vacancies(self):
        """Метод получения списка всех вакансий с указанием названий компании, названия вакансии и зарплаты и ссылки на вакансию"""
        pass

    def get_avg_salary(self):
        """Метод получения средней зарплаты по вакансиям"""
        pass

    def get_vacancies_with_higher_salary(self):
        """Метод получения списка всех вакансий, у которых зарплата выше средней по всем по всем вакансиям"""
        pass

    def get_vacancies_with_keyword(self):
        """Метод получения списка всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        pass

