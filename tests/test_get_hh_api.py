import requests
import unittest
from unittest.mock import patch

from src.get_hh_api import hh_api


class TestHHAPI(unittest.TestCase):
    @patch("requests.get")
    def test_hh_api_failure(self, mock_get):
        """Тест для функции hh_api при ошибке запроса."""
        # Мок ошибки запроса
        mock_get.side_effect = requests.exceptions.RequestException("Ошибка соединения")

        # Вызов тестируемой функции
        result = hh_api()

        # Проверка результата
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()