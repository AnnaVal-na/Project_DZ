import pytest
from src.bank_operations import count_operations_by_category
from src.widget import get_date


class TestCountOperationsByCategory:
    categories = ['Groceries', 'Utilities', 'Entertainment', 'Rent']

    def test_category_not_in_operations(self) -> None:
        operations = [{'description': 'Groceries'}, {'description': 'Groceries'}]
        expected_result = {
            'Groceries': 2,
            'Utilities': 0,
            'Entertainment': 0,
            'Rent': 0
        }
        result = count_operations_by_category(operations, self.categories)
        assert result == expected_result

    def test_count_operations(self) -> None:
        operations = [
            {'description': 'Groceries'},
            {'description': 'Groceries'},
            {'description': 'Groceries'},
            {'description': 'Utilities'},
            {'description': 'Utilities'},
            {'description': 'Entertainment'}
        ]
        expected_result = {
            'Groceries': 3,
            'Utilities': 2,
            'Entertainment': 1,
            'Rent': 0
        }
        result = count_operations_by_category(operations, self.categories)
        assert result == expected_result

    def test_empty_operations(self) -> None:
        expected_result = {
            'Groceries': 0,
            'Utilities': 0,
            'Entertainment': 0,
            'Rent': 0
        }
        result = count_operations_by_category([], self.categories)
        assert result == expected_result

    def test_no_matching_categories(self) -> None:
        operations = [{'description': 'Food'}, {'description': 'Transport'}]
        expected_result = {
            'Groceries': 0,
            'Utilities': 0,
            'Entertainment': 0,
            'Rent': 0
        }
        result = count_operations_by_category(operations, self.categories)
        assert result == expected_result


def test_get_date_invalid_input() -> None:
    # Проверка обработки None
    with pytest.raises(TypeError):
        get_date(None)  # Теперь соответствует обновленной сигнатуре

    # Проверка невалидных строк
    invalid_cases = [
        "invalid_date",
        "",
        "2023-10-05",  # Неполная дата
        "not_a_date"
    ]

    for case in invalid_cases:
        with pytest.raises(ValueError):
            get_date(case)
