import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

# Импортируем функцию для тестирования
from src.transactions_from_csv import load_transactions_from_csv


class TestLoadTransactionsFromCSV(unittest.TestCase):

    @patch('pandas.read_csv')
    def test_load_transactions_success(self, mock_read_csv: MagicMock) -> None:
        # Настраиваем Mock для возвращения тестового DataFrame
        mock_data = {
            'date': ['2023-01-01', '2023-01-02'],
            'amount': [100, 200],
            'description': ['Transaction 1', 'Transaction 2']
        }
        mock_df = pd.DataFrame(mock_data)
        mock_read_csv.return_value = mock_df

        # Вызываем функцию
        transactions = load_transactions_from_csv('dummy_path.csv')

        # Проверяем, что возвращаемое значение соответствует ожиданиям
        expected_transactions = [
            {'date': '2023-01-01', 'amount': 100, 'description': 'Transaction 1'},
            {'date': '2023-01-02', 'amount': 200, 'description': 'Transaction 2'}
        ]
        self.assertEqual(transactions, expected_transactions)

    @patch('pandas.read_csv')
    def test_load_transactions_file_not_found(self, mock_read_csv: MagicMock) -> None:
        # Настраиваем Mock для вызова FileNotFoundError
        mock_read_csv.side_effect = FileNotFoundError

        # Вызываем функцию
        transactions = load_transactions_from_csv('dummy_path.csv')

        # Проверяем, что возвращаемое значение пусто
        self.assertEqual(transactions, [])

    @patch('pandas.read_csv')
    def test_load_transactions_other_exception(self, mock_read_csv: MagicMock) -> None:
        # Настраиваем Mock для вызова другой ошибки
        mock_read_csv.side_effect = Exception("Some error")

        # Вызываем функцию
        transactions = load_transactions_from_csv('dummy_path.csv')

        # Проверяем, что возвращаемое значение пусто
        self.assertEqual(transactions, [])


if __name__ == '__main__':
    unittest.main()
