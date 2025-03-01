import json
import os
from abc import ABC, abstractmethod
from pathlib import Path

from setting import BASE_DIR

json_filename = Path(BASE_DIR, "data", "employers_data.json").parent
database_path = Path(BASE_DIR, "src", "database.ini").parent


class Parser(ABC):
    """Абстрактный класс, который обязывает реализовать методы для добавления списка работников в файл"""

    pass

    @abstractmethod
    def add_employers_to_file(self, employer):
        """Функция добавляет данные формата json в файл"""
        pass

    def read_data(self):
        """Чтение файла"""
        pass

    def delete_data(self):
        """Удаление файла"""


class EmployerSaverJSON(Parser):
    """Класс для работы с файлами (employers_list из класса EmployerParser) в формате json"""

    def __init__(self, json_filename):
        self.json_filename = json_filename
        self.inf_about_employers = []

    # блок функций для добавления в файлы
    def add_employers_to_file(self, employer):

        with open(self.json_filename, "a", encoding="utf-8") as file:
            json.dump(employer, file, indent=4, ensure_ascii=False)
            file.write("\n")

    def read_data_json(self):
        """Чтение json файла"""
        with open(self.json_filename, "r", encoding="utf-8") as file:
            return json.load(file)

    def delete_data_json(self):
        """Удаление json-файла"""

        open(self.json_filename, "w").close()
        os.remove(self.json_filename)


class EmployerSaverCSV(Parser):
    """Класс для работы с файлами (employers_list из класса EmployerParser) в формате csv"""

    pass
