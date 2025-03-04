import unittest
from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

from src.transactions_from_excel import load_transactions_from_excel


class TestLoadTransactionsFromExcel(unittest.TestCase):

    @patch('openpyxl.load_workbook')
    def test_load_transactions_success(self, mock_load_workbook: Any) -> None:
        # Создаем mock для workbook и sheet
        mock_sheet = MagicMock()
        mock_sheet.iter_rows.return_value = [
            (1, 'Transaction 1', 100),
            (2, 'Transaction 2', 200),
        ]
        mock_sheet.getitem.return_value = ['ID', 'Description', 'Amount']

        mock_workbook = MagicMock()
        mock_workbook.active = mock_sheet
        mock_load_workbook.return_value = mock_workbook

        # Вызываем тестируемую функцию
        transactions: List[Dict[str, Any]] = load_transactions_from_excel('dummy_path.xlsx')

        # Проверяем, что результат соответствует ожидаемому
        expected_transactions: List[Dict[str, Any]] = [
            {'ID': 1, 'Description': 'Transaction 1', 'Amount': 100},
            {'ID': 2, 'Description': 'Transaction 2', 'Amount': 200},
        ]
        self.assertEqual(transactions, expected_transactions)

    @patch('openpyxl.load_workbook')
    def test_load_transactions_file_not_found(self, mock_load_workbook: Any) -> None:
        mock_load_workbook.side_effect = FileNotFoundError

        transactions: List[Dict[str, Any]] = load_transactions_from_excel('dummy_path.xlsx')

        # Проверяем, что возвращаемый результат пустой список
        self.assertEqual(transactions, [])

    @patch('openpyxl.load_workbook')
    def test_load_transactions_empty_sheet(self, mock_load_workbook: Any) -> None:
        mock_sheet = MagicMock()
        mock_sheet.iter_rows.return_value = []
        mock_sheet.getitem.return_value = ['ID', 'Description', 'Amount']

        mock_workbook = MagicMock()
        mock_workbook.active = mock_sheet
        mock_load_workbook.return_value = mock_workbook

        transactions: List[Dict[str, Any]] = load_transactions_from_excel('dummy_path.xlsx')

        # Проверяем, что возвращаемый результат пустой список
        self.assertEqual(transactions, [])

    @patch('openpyxl.load_workbook')
    def test_load_transactions_incorrect_row_length(self, mock_load_workbook: Any) -> None:
        mock_sheet = MagicMock()
        mock_sheet.iter_rows.return_value = [
            (1, 'Transaction 1', 100),
            (2, 'Transaction 2'),  # Некорректная строка
        ]
        mock_sheet.getitem.return_value = ['ID', 'Description', 'Amount']

        mock_workbook = MagicMock()
        mock_workbook.active = mock_sheet
        mock_load_workbook.return_value = mock_workbook

        transactions: List[Dict[str, Any]] = load_transactions_from_excel('dummy_path.xlsx')

        # Проверяем, что возвращаемый результат соответствует ожидаемому
        expected_transactions: List[Dict[str, Any]] = [
            {'ID': 1, 'Description': 'Transaction 1', 'Amount': 100},
        ]
        self.assertEqual(transactions, expected_transactions)


if __name__ == '__main__':
    unittest.main()
