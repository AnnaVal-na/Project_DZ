import unittest
from typing import Any
from unittest.mock import patch

import pandas as pd

from src.transactions_from_csv import load_transactions_from_csv


class TestLoadTransactionsFromCSV(unittest.TestCase):

    @patch('your_module.pd.read_csv')
    def test_load_transactions_success(self, mock_read_csv: Any) -> None:
        # Подготовка данных
        mock_data = {
            'id': [1, 2],
            'amount': [100.0, 200.0],
            'currency': ['USD', 'EUR']
        }
        mock_df = pd.DataFrame(mock_data)
        mock_read_csv.return_value = mock_df

        # Вызов функции
        result = load_transactions_from_csv('fake_path.csv')

        # Проверка результата
        expected_result = [
            {'id': 1, 'amount': 100.0, 'currency': 'USD'},
            {'id': 2, 'amount': 200.0, 'currency': 'EUR'}
        ]
        self.assertEqual(result, expected_result)

    @patch('your_module.pd.read_csv')
    def test_load_transactions_file_not_found(self, mock_read_csv: Any) -> None:
        # Настройка исключения
        mock_read_csv.side_effect = FileNotFoundError

        # Вызов функции
        result = load_transactions_from_csv('fake_path.csv')

        # Проверка результата
        self.assertEqual(result, [])

    @patch('your_module.pd.read_csv')
    def test_load_transactions_other_exception(self, mock_read_csv: Any) -> None:
        # Настройка исключения
        mock_read_csv.side_effect = Exception('Some error')

        # Вызов функции
        result = load_transactions_from_csv('fake_path.csv')

        # Проверка результата
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
