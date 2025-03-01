from typing import Dict, List, Union

import pytest

from src.processing import filter_by_state

# Тест для проверки правильности фильтрации по статусу state


def test_filter_by_state_correct_filtering() -> None:
    # Исходные данные
    data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "PENDING"},
        {"id": 3, "state": "EXECUTED"},
        {"id": 4, "state": "CANCELED"}
    ]
    # Фильтрация по умолчанию (state='EXECUTED')
    result = filter_by_state(data)
    expected = [{"id": 1, "state": "EXECUTED"}, {"id": 3, "state": "EXECUTED"}]
    assert result == expected, "Ошибка при фильтрации по EXECUTED"


# Тест для проверки работы функции, когда нет элементов с указанным state
def test_filter_by_state_no_matching_state() -> None:
    # Исходные данные без элементов с state='EXECUTED'
    data: List[Dict[str, Union[str, int]]] = [
        {"id": 1, "state": "PENDING"},
        {"id": 2, "state": "CANCELED"}
    ]
    # Фильтрация по EXECUTED
    result = filter_by_state(data)
    expected: List[Dict[str, Union[str, int]]] = []  # Явно указываем тип для expected
    assert result == expected, "Ошибка: функция должна вернуть пустой список, если нет совпадений"


@pytest.mark.parametrize("data, state, expected", [
    # Тест 1: Фильтрация по EXECUTED
    (
        [
            {"id": 1, "state": "EXECUTED"},
            {"id": 2, "state": "PENDING"},
            {"id": 3, "state": "EXECUTED"}
        ],
        "EXECUTED",
        [
            {"id": 1, "state": "EXECUTED"},
            {"id": 3, "state": "EXECUTED"}
        ]
    ),
    # Тест 2: Фильтрация по PENDING
    (
        [
            {"id": 1, "state": "EXECUTED"},
            {"id": 2, "state": "PENDING"},
            {"id": 3, "state": "EXECUTED"}
        ],
        "PENDING",
        [
            {"id": 2, "state": "PENDING"}
        ]
    ),
    # Тест 3: Фильтрация по CANCELED
    (
        [
            {"id": 1, "state": "EXECUTED"},
            {"id": 2, "state": "PENDING"},
            {"id": 3, "state": "CANCELED"}
        ],
        "CANCELED",
        [
            {"id": 3, "state": "CANCELED"}
        ]
    ),
    # Тест 4: Отсутствие совпадений
    (
        [
            {"id": 1, "state": "EXECUTED"},
            {"id": 2, "state": "PENDING"}
        ],
        "COMPLETED",
        []
    )
])
def test_filter_by_state_parametrized(data: List[Dict[str, str]], state: str, expected: List[Dict[str, str]]) -> None:
    result = filter_by_state(data, state)
    assert result == expected, f"Ошибка при фильтрации с state={state}"
