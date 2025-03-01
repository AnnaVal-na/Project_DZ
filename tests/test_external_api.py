import unittest
from unittest.mock import patch, Mock
from src.external_api import get_exchange_rate, convert_to_rub
from typing import Dict, Any, Optional


class TestCurrencyConversion(unittest.TestCase):

    @patch('requests.get')
    def test_get_exchange_rate_success(self, mock_get: Mock) -> None:
        # Настраиваем mock-объект
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'rates': {
                'RUB': 75.0
            }
        }
        mock_get.return_value = mock_response

        # Выполняем тест
        rate: Optional[float] = get_exchange_rate('dummy_api_key', 'USD', 'RUB')
        self.assertEqual(rate, 75.0)

    @patch('requests.get')
    def test_get_exchange_rate_failure(self, mock_get: Mock) -> None:
        # Настраиваем mock-объект для неудачного запроса
        mock_response = Mock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        # Проверяем, что возникает исключение
        with self.assertRaises(Exception) as context:
            get_exchange_rate('dummy_api_key', 'USD', 'RUB')

        self.assertTrue('Error fetching exchange rate' in str(context.exception))

    def test_convert_to_rub_rub_currency(self) -> None:
        transaction: Dict[str, Any] = {'amount': 100, 'currency': 'RUB'}
        result: Optional[float] = convert_to_rub(transaction)  # Изменено на Optional[float]
        self.assertEqual(result, 100.0)

    @patch('src.external_api.get_exchange_rate')
    def test_convert_to_rub_usd_currency(self, mock_get_exchange_rate: Mock) -> None:
        # Настраиваем mock для get_exchange_rate
        mock_get_exchange_rate.return_value = 75.0
        transaction: Dict[str, Any] = {'amount': 100, 'currency': 'USD'}
        result: Optional[float] = convert_to_rub(transaction)  # Изменено на Optional[float]
        self.assertEqual(result, 7500.0)

    @patch('src.external_api.get_exchange_rate')
    def test_convert_to_rub_eur_currency(self, mock_get_exchange_rate: Mock) -> None:
        # Настраиваем mock для get_exchange_rate
        mock_get_exchange_rate.return_value = 80.0
        transaction: Dict[str, Any] = {'amount': 100, 'currency': 'EUR'}
        result: Optional[float] = convert_to_rub(transaction)  # Изменено на Optional[float]
        self.assertEqual(result, 8000.0)

    def test_convert_to_rub_unsupported_currency(self) -> None:
        transaction: Dict[str, Any] = {'amount': 100, 'currency': 'GBP'}
        result: Optional[float] = convert_to_rub(transaction)  # Изменено на Optional[float]
        self.assertIsNone(result)


if __name__ == '__main__':  # Исправлено на __name__ == '__main__'
    unittest.main()
