import unittest
from src.transaction_search import search_transactions


class TestSearchTransactions(unittest.TestCase):
    """Тестирование функционала поиска банковских операций по описанию."""

    def setUp(self) -> None:
        """
        Инициализация тестовых данных.

        Содержит список транзакций с разными вариантами описаний:
        - Точные совпадения
        - Частичные совпадения
        - Спецсимволы
        - Разный регистр
        """
        self.test_transactions = [
            {'description': 'Payment for groceries', 'amount': 100},
            {'description': 'Cafe "Coffee Time" purchase', 'amount': 15},
            {'description': 'Online store AMAZON', 'amount': 200},
            {'description': 'PYTHON course payment', 'amount': 150},
            {'description': 'Monthly rent', 'amount': 1000},
            {'description': 'Café 123* special', 'amount': 30},
        ]

    def test_exact_match(self) -> None:
        """Тестирование поиска по точному совпадению строки."""
        result = search_transactions(self.test_transactions, 'groceries')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['description'], 'Payment for groceries')

    def test_case_insensitivity(self) -> None:
        """Проверка регистронезависимости поиска."""
        result_lower = search_transactions(self.test_transactions, 'amazon')
        result_upper = search_transactions(self.test_transactions, 'AMAZON')
        self.assertEqual(len(result_lower), 1)
        self.assertEqual(result_lower, result_upper)

    def test_partial_match(self) -> None:
        """Поиск по частичному совпадению с учётом различных форм символов."""
        result = search_transactions(self.test_transactions, 'cafe')
        self.assertEqual(len(result), 2)
        descriptions = {t['description'] for t in result}
        self.assertIn('Cafe "Coffee Time" purchase', descriptions)
        self.assertIn('Café 123* special', descriptions)

    def test_no_matches(self) -> None:
        """Тест случая отсутствия совпадений."""
        result = search_transactions(self.test_transactions, 'hotel')
        self.assertEqual(len(result), 0)

    def test_special_characters(self) -> None:
        """Проверка обработки специальных символов в поисковом запросе."""
        result = search_transactions(self.test_transactions, '123*')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['description'], 'Café 123* special')

    def test_empty_transactions_list(self) -> None:
        """Тестирование обработки пустого списка транзакций."""
        result = search_transactions([], 'test')
        self.assertEqual(len(result), 0)

    def test_empty_search_string(self) -> None:
        """Проверка поведения при пустой строке поиска."""
        result = search_transactions(self.test_transactions, '')
        self.assertEqual(len(result), len(self.test_transactions))

    def test_missing_description_key(self) -> None:
        """Тест обработки транзакций с отсутствующим ключом описания."""
        transactions_with_missing = self.test_transactions + [{'amount': 50}]
        result = search_transactions(transactions_with_missing, 'groceries')
        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()
