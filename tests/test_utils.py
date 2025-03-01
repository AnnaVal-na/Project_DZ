import unittest
from unittest.mock import mock_open, patch
from src.utils import load_transactions_from_json
from typing import List, Dict, Any


class TestLoadTransactions(unittest.TestCase):

    @patch("os.path.exists")
    def test_file_not_exists(self, mock_exists: Any) -> None:
        # Настраиваем mock для os.path.exists
        mock_exists.return_value = False

        result: List[Dict[str, Any]] = load_transactions_from_json("dummy_path.json")
        self.assertEqual(result, [])

    @patch("builtins.open", new_callable=mock_open, read_data='[{"amount": 100, "currency": "USD"}]')
    @patch("os.path.exists")
    def test_load_transactions_success(self, mock_exists: Any, mock_file: Any) -> None:
        # Настраиваем mock для os.path.exists
        mock_exists.return_value = True

        result: List[Dict[str, Any]] = load_transactions_from_json("dummy_path.json")
        self.assertEqual(result, [{"amount": 100, "currency": "USD"}])

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_transactions_invalid_json(self, mock_file: Any, mock_exists: Any) -> None:
        # Настраиваем mock для os.path.exists
        mock_exists.return_value = True
        mock_file.side_effect = IOError("File not found")  # Симулируем ошибку открытия файла

        result: List[Dict[str, Any]] = load_transactions_from_json("dummy_path.json")
        self.assertEqual(result, [])

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data='{"amount": 100, "currency": "USD"}')  # Неверный JSON
    def test_load_transactions_not_a_list(self, mock_file: Any, mock_exists: Any) -> None:
        # Настраиваем mock для os.path.exists
        mock_exists.return_value = True

        result: List[Dict[str, Any]] = load_transactions_from_json("dummy_path.json")
        self.assertEqual(result, [])

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data='[{"amount": 100, "currency": "USD"}]')
    def test_load_transactions_success_multiple_entries(self, mock_file: Any, mock_exists: Any) -> None:
        # Настраиваем mock для os.path.exists
        mock_exists.return_value = True

        result: List[Dict[str, Any]] = load_transactions_from_json("dummy_path.json")
        self.assertEqual(result, [{"amount": 100, "currency": "USD"}])


if __name__ == '__main__':
    unittest.main()
