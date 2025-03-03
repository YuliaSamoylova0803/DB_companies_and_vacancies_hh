import pytest


@pytest.fixture
def employers():
    return [
        {"name": "Company A", "open_vacancies": 5},
        {"name": "Company B", "open_vacancies": 0},
        {"name": "Company C", "open_vacancies": 3},
    ]
