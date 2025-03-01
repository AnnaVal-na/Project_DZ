from typing import Dict, List

import pytest

from src.generators import filter_by_currency


# Фикстура для тестовых данных
@pytest.fixture
def sample_transactions() -> List[Dict]:
    return [
        {"id": 1, "operationAmount": {"amount": 100, "currency": {"code": "USD"}}},
        {"id": 2, "operationAmount": {"amount": 200, "currency": {"code": "EUR"}}},
        {"id": 3, "operationAmount": {"amount": 300, "currency": {"code": "USD"}}},
        {"id": 4, "operationAmount": None},  # Пропущен operationAmount
        {"id": 5, "operationAmount": {"amount": 400, "currency": {"code": "GBP"}}}
    ]


# Тест 1: Проверка корректной фильтрации транзакций по заданной валюте
def test_filter_by_currency_correct_filtering(sample_transactions: List[Dict]) -> None:
    currency = "USD"
    filtered_transactions = list(filter_by_currency(sample_transactions, currency))
    expected_result: List[Dict] = [
        {"id": 1, "operationAmount": {"amount": 100, "currency": {"code": "USD"}}},
        {"id": 3, "operationAmount": {"amount": 300, "currency": {"code": "USD"}}}
    ]
    assert filtered_transactions == expected_result, "Ошибка при фильтрации транзакций по валюте"


# Тест 2: Проверка обработки случая, когда транзакции в заданной валюте отсутствуют
def test_filter_by_currency_no_matching_currency(sample_transactions: List[Dict]) -> None:
    currency = "JPY"  # Валюта, которой нет в данных
    filtered_transactions = list(filter_by_currency(sample_transactions, currency))
    expected_result: List[Dict] = []
    assert (
        filtered_transactions == expected_result
    ), "Ошибка: функция должна вернуть пустой список, если нет совпадений"


# Тест 3: Проверка обработки пустого списка или списка без соответствующих валютных операций
def test_filter_by_currency_empty_or_invalid_data() -> None:
    # Случай пустого списка
    empty_transactions: List[Dict] = []
    result_empty = list(filter_by_currency(empty_transactions, "USD"))
    assert result_empty == [], "Ошибка: функция должна корректно обрабатывать пустой список"

    # Случай списка без operationAmount
    invalid_transactions: List[Dict] = [
        {"id": 1, "operationAmount": None},
        {"id": 2, "operationAmount": {"amount": 200, "currency": None}},
        {"id": 3}
    ]
    result_invalid = list(filter_by_currency(invalid_transactions, "USD"))
    assert result_invalid == [], "Ошибка: функция должна корректно обрабатывать список без operationAmount"
