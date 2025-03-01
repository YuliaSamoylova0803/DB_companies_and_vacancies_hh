def get_data_vacancies():
    """Получение данных из таблицы vacancies"""
    return "SELECT * FROM vacancies"


def get_data_companies():
    """Получение данных из таблицы companies"""
    return "SELECT * FROM companies"


def get_data_join_tables():
    """Объединение таблиц"""
    return """LEFT JOIN companies as c ON c.company_id = v.company_id = name"""


def get_all_vacancies(name):
    """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
    return """SELECT c.name, v.title, v.salary_to, v.salary_from, v.link
              FROM vacancies as v
              LEFT JOIN companies as c ON c.company_id = v.company_id = name"""


def get_avg_salary():
    """Получение средней зарплаты по вакансиям"""
    return """SELECT AVG(salary_to + salary_from) / 2 as middle_salary
            FROM vacancies 
            WHERE salary_to IS NOT NULL AND salary_from IS NOT NULL;"""


def get_vacancies_with_higher_salary():
    """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
    return """
                    SELECT c.name, v.title, v.salary_from, v.salary_to, v.currency, v.link
                    FROM vacancies v
                    JOIN companies c ON v.company_id = c.company_id
                    WHERE (v.salary_from + v.salary_to) / 2 > %s;
                """


def get_vacancies_with_keyword(self, keyword):
    """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
    return """
    SELECT c.name, v.title, v.salary_from, v.salary_to, v.currency, v.link
    FROM vacancies v
    JOIN companies c ON v.company_id = c.company_id
    WHERE LOWER(v.title) LIKE '%keyword%';"""
