import pytest
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from pytest import CaptureFixture
from src.main import (
    load_transactions_from_json,
    filter_transactions_by_status,
    sort_transactions,
    parse_date,
    get_user_choice,
    print_transactions
)


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    return [
        {'date': '2023-10-05', 'status': 'EXECUTED', 'amount': 100},
        {'date': '2023-09-01', 'status': 'CANCELED', 'amount': 200},
        {'date': 'invalid_date', 'status': 'PENDING', 'amount': 300},
    ]


def test_load_json_valid_file(tmp_path: Path) -> None:
    """Тест загрузки корректного JSON-файла."""
    file = tmp_path / "test.json"
    file.write_text('[{"date": "2023-10-05", "status": "EXECUTED"}]')
    result = load_transactions_from_json(str(file))
    assert len(result) == 1
    assert result[0]['date'] == '2023-10-05'


def test_filter_status_case_insensitive(sample_transactions: List[Dict[str, Any]]) -> None:
    """Регистронезависимая фильтрация по статусу."""
    result = filter_transactions_by_status(sample_transactions, 'executed')
    assert len(result) == 1
    assert result[0]['status'] == 'EXECUTED'


def test_sort_transactions_with_invalid_dates(sample_transactions: List[Dict[str, Any]]) -> None:
    """Сортировка с некорректными датами помещает их в начало/конец."""
    result = sort_transactions(sample_transactions, ascending=False)
    assert result[0]['date'] == '2023-10-05'
    assert result[-1]['date'] == 'invalid_date'


def test_parse_date_formats() -> None:
    """Парсинг дат из разных форматов."""
    assert parse_date("2023-10-05") == datetime(2023, 10, 5)
    assert parse_date("05.10.2023") == datetime(2023, 10, 5)
    assert parse_date("10/05/2023") == datetime(2023, 10, 5)
    assert parse_date("invalid") is None


@patch('builtins.input', side_effect=['3', '2'])
def test_get_user_choice_retry(inp_mock: MagicMock) -> None:
    """Проверка повторного запроса при неверном вводе."""
    with patch('builtins.print') as mock_print:
        result = get_user_choice(['A', 'B'])
        expected_calls = [
            unittest.mock.call('\nВыберите:'),
            unittest.mock.call('1. A'),
            unittest.mock.call('2. B'),
            unittest.mock.call('Ошибка ввода. Попробуйте снова.'),
            unittest.mock.call('\nВыберите:'),
            unittest.mock.call('1. A'),
            unittest.mock.call('2. B'),
        ]
        mock_print.assert_has_calls(expected_calls, any_order=False)
    assert result == '2'


def test_print_transactions_empty(capsys: CaptureFixture[str]) -> None:
    """Вывод пустого списка транзакций."""
    print_transactions([])
    captured = capsys.readouterr()
    assert "Нет транзакций" in captured.out


def test_print_transactions_invalid_data(
    capsys: CaptureFixture[str],
    sample_transactions: List[Dict[str, Any]]
) -> None:
    """Вывод транзакций с некорректными данными."""
    print_transactions(sample_transactions)
    captured = capsys.readouterr()
    assert "Дата неизвестна" in captured.out
    assert "Сумма: 100" in captured.out
