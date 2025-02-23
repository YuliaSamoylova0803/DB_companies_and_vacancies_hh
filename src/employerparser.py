from abc import ABC, abstractmethod
from typing import Any

import requests

class Parser(ABC):
    """Абстрактный класс для работы с API сервиса с работодателями"""
    pass

    @abstractmethod
    def load_employers(self):
        """Метод отправки get-запроса на сайт Head Hunter"""
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
        while self.params.get("page") != 30:
            response = requests.get(self._url, headers=self._headers, params=self.params)
            vacancies = response.json()["items"]
            self.employers.extend(vacancies)
            self.params["page"] += 1
        return self.employers


if __name__=="__main__":
    hh_api = EmployerParser()
    print(hh_api)

    # Получение работодателей с hh.ru в формате JSON
    hh_employers = hh_api.load_employers("СБЕР")
    print(hh_employers)
    print(len(hh_employers))



