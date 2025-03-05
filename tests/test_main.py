import unittest
from unittest.mock import mock_open, patch
import json
import pandas as pd
from io import StringIO
from datetime import datetime  # Добавлен импорт datetime
from src.main import (
    load_transactions_from_json,
    load_transactions_from_csv,
    load_transactions_from_xlsx,
    filter_transactions_by_status,
    sort_transactions,
    parse_date,
    print_transactions
)


class TestTransactionLoader(unittest.TestCase):
    """Класс для тестирования загрузки и обработки транзакций."""

    def test_load_transactions_from_json(self) -> None:
        """Тестирование загрузки транзакций из JSON-файла."""
        mock_data = json.dumps([
            {"id": 1, "date": "2023-10-01", "description": "Оплата", "status": "EXECUTED"},
            {"id": 2, "date": "2023-10-02", "description": "Перевод", "status": "PENDING"},
        ])
        with patch('builtins.open', mock_open(read_data=mock_data)):
            result = load_transactions_from_json('fake_path.json')
            expected = [
                {"id": 1, "date": "2023-10-01", "description": "Оплата", "status": "EXECUTED"},
                {"id": 2, "date": "2023-10-02", "description": "Перевод", "status": "PENDING"},
            ]
            self.assertEqual(result, expected)

    def test_load_transactions_from_csv(self) -> None:
        """Тестирование загрузки транзакций из CSV-файла."""
        mock_data = "id,date,description,status\n1,2023-10-01,Оплата,EXECUTED\n2,2023-10-02,Перевод,PENDING\n"
        with patch('builtins.open', mock_open(read_data=mock_data)):
            result = load_transactions_from_csv('fake_path.csv')
            expected = [
                {"id": "1", "date": "2023-10-01", "description": "Оплата", "status": "EXECUTED"},
                {"id": "2", "date": "2023-10-02", "description": "Перевод", "status": "PENDING"},
            ]
            self.assertEqual(result, expected)

    def test_load_transactions_from_xlsx(self) -> None:
        """Тестирование загрузки транзакций из XLSX-файла."""
        df = pd.DataFrame({
            "id": [1, 2],
            "date": ["2023-10-01", "2023-10-02"],
            "description": ["Оплата", "Перевод"],
            "status": ["EXECUTED", "PENDING"]
        })
        with patch('pandas.read_excel', return_value=df):
            result = load_transactions_from_xlsx('fake_path.xlsx')
            expected = [
                {"id": 1, "date": "2023-10-01", "description": "Оплата", "status": "EXECUTED"},
                {"id": 2, "date": "2023-10-02", "description": "Перевод", "status": "PENDING"},
            ]
            self.assertEqual(result, expected)

    def test_filter_transactions_by_status(self) -> None:
        """Тестирование фильтрации транзакций по статусу."""
        transactions = [
            {"id": 1, "status": "EXECUTED"},
            {"id": 2, "status": "PENDING"},
            {"id": 3, "status": "EXECUTED"},
        ]
        result = filter_transactions_by_status(transactions, "EXECUTED")
        expected = [
            {"id": 1, "status": "EXECUTED"},
            {"id": 3, "status": "EXECUTED"},
        ]
        self.assertEqual(result, expected)

    def test_sort_transactions(self) -> None:
        """Тестирование сортировки транзакций по дате."""
        transactions = [
            {"id": 1, "date": "2023-10-02"},
            {"id": 2, "date": "2023-10-01"},
        ]
        result = sort_transactions(transactions, ascending=True)
        expected = [
            {"id": 2, "date": "2023-10-01"},
            {"id": 1, "date": "2023-10-02"},
        ]
        self.assertEqual(result, expected)

    def test_parse_date(self) -> None:
        """Тестирование парсинга даты из строки."""
        valid_date = "2023-10-01"
        invalid_date = "01-10-2023"
        self.assertEqual(parse_date(valid_date), datetime(2023, 10, 1))  # Исправлен импорт datetime
        self.assertIsNone(parse_date(invalid_date))
        self.assertIsNone(parse_date(None))

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_transactions(self, mock_stdout: StringIO) -> None:
        """Тестирование вывода информации о транзакциях."""
        transactions = [
            {
                "date": "2023-10-01",
                "description": "Оплата",
                "account": "123456",
                "amount": "100.00",
                "currency": "RUB"
            },
            {
                "date": "2023-10-02",
                "description": "Перевод",
                "account": "654321",
                "amount": "200.00",
                "currency": "USD"
            },
        ]
        print_transactions(transactions)

        expected_output = (
            "Всего банковских операций в выборке: 2\n\n"
            "2023-10-01 Оплата\n"
            "Счет 123456\n"
            "Сумма: 100.00 RUB\n\n"  # Исправлено: убран лишний \n в конце
            "2023-10-02 Перевод\n"
            "Счет 654321\n"
            "Сумма: 200.00 USD\n\n"  # Добавлен недостающий \n
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_transactions_empty(self, mock_stdout: StringIO) -> None:
        """Тестирование вывода при отсутствии транзакций."""
        print_transactions([])
        expected_output = "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)


if __name__ == '__main__':
    unittest.main()
