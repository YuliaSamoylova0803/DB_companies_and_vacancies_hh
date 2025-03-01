from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import requests

from setting import BASE_DIR

json_filename = Path(BASE_DIR, "data", "employers_data.json").parent
database_path = Path(BASE_DIR, "src", "database.ini").parent


class Parser(ABC):
    """Абстрактный класс для работы с API сервиса с работодателями"""

    pass

    @abstractmethod
    def load_employers(self):
        """Метод отправки get-запроса на сайт Head Hunter"""
        pass

    @abstractmethod
    def filtered_by_the_number_of_vacancies(self):
        """Метод получения компаний только с открытыми вакансиями"""
        pass


class EmployerParser(Parser):
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        """Магический метод инициализаций объектов для отправки get-запроса"""
        self._url = "https://api.hh.ru/employers"
        self._headers = {"User-Agent": "HH-User-Agent"}
        self.params = {"text": "", "page": 0, "per_page": 100}
        self.employers = []

    def load_employers(self, keyword) -> Any:
        """Метод отправки get-запроса на сайт Head Hunter"""
        self.params["text"] = keyword
        while self.params.get("page") != 50:
            response = requests.get(self._url, headers=self._headers, params=self.params)
            employers = response.json()["items"]
            self.employers.extend(employers)
            self.params["page"] += 1
        return self.employers

    def filtered_by_the_number_of_vacancies(self, employers: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Метод получения компаний только с открытыми вакансиями"""
        employers_list = []
        for employer in self.employers:
            if employer.get("open_vacancies", 0) > 0:
                employers_list.append(employer)
        return employers_list


if __name__ == "__main__":
    hh_api = EmployerParser()
    print(hh_api)

    # Получение работодателей с hh.ru в формате JSON
    employers = hh_api.load_employers("")
    print(employers)
    print(len(employers))
    search_employers = employers.filtered_by_the_number_of_vacancies(employers)
    print(search_employers)
