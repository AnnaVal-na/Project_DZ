import pytest
from src.processing import sort_by_date
from typing import List, Dict, Any

# Тест для проверки сортировки по датам в порядке убывания и возрастания


def test_sort_by_date_ascending_descending() -> None:
    # Исходные данные
    data = [
        {"id": 1, "date": "2023-10-05T14:48:00"},
        {"id": 2, "date": "2023-10-03T10:30:00"},
        {"id": 3, "date": "2023-10-07T09:15:00"}
    ]

    # Сортировка по убыванию (по умолчанию)
    result_descending = sort_by_date(data)
    expected_descending = [
        {"id": 3, "date": "2023-10-07T09:15:00"},
        {"id": 1, "date": "2023-10-05T14:48:00"},
        {"id": 2, "date": "2023-10-03T10:30:00"}
    ]
    assert result_descending == expected_descending, "Ошибка при сортировке по убыванию"

    # Сортировка по возрастанию
    result_ascending = sort_by_date(data, descending=False)
    expected_ascending = [
        {"id": 2, "date": "2023-10-03T10:30:00"},
        {"id": 1, "date": "2023-10-05T14:48:00"},
        {"id": 3, "date": "2023-10-07T09:15:00"}
    ]
    assert result_ascending == expected_ascending, "Ошибка при сортировке по возрастанию"


# Тест для проверки сортировки при одинаковых датах
def test_sort_by_date_same_dates() -> None:
    # Исходные данные с одинаковыми датами
    data = [
        {"id": 1, "date": "2023-10-05T14:48:00"},
        {"id": 2, "date": "2023-10-05T14:48:00"},
        {"id": 3, "date": "2023-10-05T14:48:00"}
    ]

    # Сортировка по убыванию
    result_descending = sort_by_date(data)
    # Ожидается, что порядок элементов с одинаковыми датами сохранится
    expected_descending = [
        {"id": 1, "date": "2023-10-05T14:48:00"},
        {"id": 2, "date": "2023-10-05T14:48:00"},
        {"id": 3, "date": "2023-10-05T14:48:00"}
    ]
    assert result_descending == expected_descending, "Ошибка при сортировке при одинаковых датах"

    # Сортировка по возрастанию
    result_ascending = sort_by_date(data, descending=False)
    expected_ascending = [
        {"id": 1, "date": "2023-10-05T14:48:00"},
        {"id": 2, "date": "2023-10-05T14:48:00"},
        {"id": 3, "date": "2023-10-05T14:48:00"}
    ]
    assert result_ascending == expected_ascending, "Ошибка при сортировке при одинаковых датах"


# Тест для проверки работы функции с некорректными форматами дат
def test_sort_by_date_invalid_dates() -> None:
    # Исходные данные с некорректными форматами дат
    data: List[Dict[str, Any]] = [
        {"id": 1, "date": "2023-10-05T14:48:00"},
        {"id": 2, "date": "invalid_date"},
        {"id": 3, "date": "2023-10-07T09:15:00"}
    ]
    # Проверяем, что функция вызывает ValueError при некорректных датах
    with pytest.raises(ValueError, match="Invalid isoformat string"):
        sort_by_date(data)

    # Исходные данные с пропущенным ключом 'date'
    data_missing_key: List[Dict[str, Any]] = [
        {"id": 1, "date": "2023-10-05T14:48:00"},
        {"id": 2},  # Пропущен ключ 'date'
        {"id": 3, "date": "2023-10-07T09:15:00"}
    ]
    # Проверяем, что функция вызывает KeyError при отсутствии ключа 'date'
    with pytest.raises(KeyError):
        sort_by_date(data_missing_key)
