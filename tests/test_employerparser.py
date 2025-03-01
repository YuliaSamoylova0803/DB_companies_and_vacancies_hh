import unittest
from src.employerparser import EmployerParser

class TestFilteredByTheNumberOfVacancies(unittest.TestCase):
    def test_no_open_vacancies(self):
        """Тест для случая, когда нет работодателей с открытыми вакансиями."""
        employers = [
            {"name": "Company A", "open_vacancies": 0},
            {"name": "Company B", "open_vacancies": 0},
        ]

        expected_result = []

        your_instance = EmployerParser()
        result = your_instance.filtered_by_the_number_of_vacancies(employers)
        self.assertEqual(result, expected_result)

    def test_empty_input(self):
        """Тест для пустого списка работодателей."""
        employers = []
        expected_result = []

        your_instance = EmployerParser()
        result = your_instance.filtered_by_the_number_of_vacancies(employers)
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()
