from typing import Any, Dict, List


def get_data_vacancies() -> str:
    """Получение данных из таблицы vacancies."""
    return "SELECT * FROM vacancies"


def get_data_companies() -> str:
    """Получение данных из таблицы companies."""
    return "SELECT * FROM companies"


def get_data_join_tables() -> str:
    """Объединение таблиц."""
    return """LEFT JOIN companies AS c ON c.company_id = v.company_id"""


def get_all_vacancies(name: str) -> str:
    """
    Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.

    :param name: Название компании.
    :return: SQL-запрос.
    """
    return f"""
        SELECT c.name, v.title, v.salary_to, v.salary_from, v.link
        FROM vacancies AS v
        LEFT JOIN companies AS c ON c.company_id = v.company_id
        WHERE c.name = '{name}'
    """


def get_avg_salary() -> str:
    """Получение средней зарплаты по вакансиям."""
    return """
        SELECT AVG((salary_to + salary_from) / 2) AS middle_salary
        FROM vacancies 
        WHERE salary_to IS NOT NULL AND salary_from IS NOT NULL;
    """


def get_vacancies_with_higher_salary() -> str:
    """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
    return """
        SELECT c.name, v.title, v.salary_from, v.salary_to, v.currency, v.link
        FROM vacancies v
        JOIN companies c ON v.company_id = c.company_id
        WHERE (v.salary_from + v.salary_to) / 2 > (
            SELECT AVG((salary_to + salary_from) / 2)
            FROM vacancies 
            WHERE salary_to IS NOT NULL AND salary_from IS NOT NULL
        );
    """


def get_vacancies_with_keyword(keyword: str) -> str:
    """
    Получает список всех вакансий, в названии которых содержатся переданные в метод слова.

    :param keyword: Ключевое слово для поиска в названии вакансии.
    :return: SQL-запрос.
    """
    return f"""
        SELECT c.name, v.title, v.salary_from, v.salary_to, v.currency, v.link
        FROM vacancies v
        JOIN companies c ON v.company_id = c.company_id
        WHERE LOWER(v.title) LIKE '%{keyword.lower()}%';
    """
