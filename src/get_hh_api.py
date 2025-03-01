import requests
import logging


# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

URL = "https://api.hh.ru/vacancies?employer_id="
PARAMS = {"pages": 10, "per_page": 10, "only_with_vacancies": True}
companies = {
    "sokolov": "1038532",
    "teremok": "27879",
    "labirint": "17488",
    "abcp": "561525",
    "simplex": "1250899",
    "writers_way": "2175093",
    "gazprom": "39305",
    "ozon": "2180",
    "fix_price": "196621",
    "mts": "3776"
}


def hh_api():
    """Функция для подключения к api hh.ru"""
    data_list = []
    for company in companies.values():
        try:
            response = requests.get(f"{URL}{company}", params=PARAMS)
            response.raise_for_status()
            data = response.json()
            if "items" in data:
                data_list.extend(data["items"])
        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка при запросе к API: {e}")
    return data_list

def get_data(data):
    """
    Функция для обработки данных из API и подготовки их для вставки в БД.
    Возвращает словарь, где ключ — ID компании, а значение — словарь с данными о компании и списком её вакансий.
    """
    data_list = {}

    for values in data:
        try:
            # Обработка данных о компании
            employer = values.get('employer', {})
            company_id = employer.get('id')
            company_name = employer.get('name')
            company_url = employer.get('alternate_url', '')  # Используем alternate_url, если есть

            # Обработка данных о вакансии
            vacancy_id = values.get('id')
            vacancy_name = values.get('name')
            salary = values.get('salary', {})
            salary_from = int(salary['from']) if salary and salary.get('from') else None
            salary_to = int(salary['to']) if salary and salary.get('to') else None
            currency = salary.get('currency') if salary else None
            url = values.get('alternate_url', '')  # Используем alternate_url, если есть

            # Если компания ещё не добавлена в результат, добавляем её
            if company_id not in data_list:
                data_list[company_id] = {
                    "company_name": company_name,
                    "company_url": company_url,
                    "vacancies": []
                }

            # Добавляем вакансию в список вакансий компании
            data_list[company_id]["vacancies"].append({
                "vacancy_id": vacancy_id,
                "vacancy_name": vacancy_name,
                "salary_from": salary_from,
                "salary_to": salary_to,
                "currency": currency,
                "url": url
            })

        except Exception as e:
            logging.error(f"Ошибка при обработке данных вакансии {values.get('id')}: {e}")

    return data_list

data = hh_api()


if __name__ == "__main__":
    data = hh_api()
    data_employers = get_data(data)
    print(data_employers)



