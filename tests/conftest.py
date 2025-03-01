from typing import Dict, List, Tuple, Union

import pytest

from src.processing import sort_by_date

# 1. Фикстуры для 4-х тестов функции get_mask_card_number

# Фикстура для тестирования функции маскировки номера карты


@pytest.fixture
def valid_card_number() -> str:
    """Фикстура для корректного номера карты"""
    return "1234567890123456"


@pytest.fixture
def invalid_card_number_length() -> str:
    """Фикстура для некорректной длины номера карты"""
    return "12345678901234"  # 14 цифр вместо 16


@pytest.fixture
def empty_card_number() -> str:
    """Фикстура для пустого номера карты"""
    return ""


@pytest.fixture
def invalid_characters_card_number() -> str:
    """Фикстура для номера карты с недопустимыми символами"""
    return "1234abcd5678efgh"


# Фикстура для тестирования функции сортировки по дате
@pytest.fixture
def sample_data_for_sorting() -> List[Dict[str, Union[str, int]]]:
    """Фикстура для списка словарей с разными датами и статусами"""
    return [
        {"id": 1, "date": "2023-10-05T14:48:00", "state": "EXECUTED"},
        {"id": 2, "date": "2023-10-03T10:30:00", "state": "PENDING"},
        {"id": 3, "date": "2023-10-07T09:15:00", "state": "EXECUTED"},
        {"id": 4, "date": "2023-10-05T14:48:00", "state": "CANCELED"},
        {"id": 5, "date": "2023-10-05T14:48:00", "state": "EXECUTED"},  # Дублирующаяся дата
    ]


@pytest.fixture
def sample_data_with_invalid_dates() -> List[Dict[str, Union[str, int]]]:
    """Фикстура для списка словарей с некорректными форматами дат"""
    return [
        {"id": 1, "date": "2023-10-05T14:48:00", "state": "EXECUTED"},
        {"id": 2, "date": "invalid_date", "state": "PENDING"},
        {"id": 3, "date": "2023-10-07T09:15:00", "state": "EXECUTED"},
        {"id": 4, "date": "", "state": "CANCELED"},
        {"id": 5, "state": "EXECUTED"},  # Отсутствует ключ 'date'
    ]


# 2. # Фикстура для параметризованных тестов к функции filter_by_state

@pytest.fixture
def parametrized_test_data() -> List[Tuple[List[Dict[str, str | int]], str, List[Dict[str, str | int]]]]:
    """Фикстура для параметризованных тестов"""
    return [
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
    ]


# 3.Фикстуры тестов функции get_date
# Фикстура для корректного преобразования даты
@pytest.fixture
def valid_iso_date() -> str:
    """Фикстура для корректной ISO-даты"""
    return "2023-10-05T14:48:00"


@pytest.fixture
def expected_formatted_date() -> str:
    """Фикстура для ожидаемого формата даты"""
    return "05.10.2023"


# Фикстура для параметризованных тестов с различными форматами дат
@pytest.fixture
def parametrized_date_data() -> List[Tuple[str, str]]:
    """Фикстура для различных форматов дат"""
    return [
        ("2023-01-01T00:00:00", "01.01.2023"),  # Начало года
        ("2023-12-31T23:59:59", "31.12.2023"),  # Конец года
        ("2023-03-01T12:00:00", "01.03.2023"),  # Первый день месяца
        ("2023-03-31T12:00:00", "31.03.2023"),  # Последний день месяца
        ("2020-02-29T00:00:00", "29.02.2020"),  # Високосный год
        ("2023-11-05T14:48:00", "05.11.2023")   # Обычная дата
    ]


# Фикстура для некорректных входных данных
@pytest.fixture
def invalid_date_inputs() -> List[str]:
    """Фикстура для некорректных форматов дат"""
    return [
        "invalid_date",  # Некорректная строка
        "",              # Пустая строка
        "2023-10-05"     # Неполная дата
    ]


# 4. Фикстуры для тестов функции get_mask_account


# Фикстура для корректных данных маскирования счета
@pytest.fixture
def valid_account_numbers() -> List[Tuple[str, str]]:
    """Фикстура для корректных номеров счетов"""
    return [
        ("123456789", "6789"),
        ("987654321", "4321"),
        ("00001234", "1234")
    ]


# Фикстура для различных форматов и длин номеров счетов
@pytest.fixture
def various_account_formats_and_lengths() -> List[Tuple[str, str]]:
    """Фикстура для различных форматов и длин номеров счетов"""
    return [
        ("1234", "1234"),  # Минимальная длина
        ("00001", "0001"),  # С нулями в начале
        ("1234567890123456", "3456")  # Длинный номер
    ]


# Фикстура для некорректных (коротких) номеров счетов
@pytest.fixture
def short_account_numbers() -> List[str]:
    """Фикстура для коротких номеров счетов"""
    return [
        "123",  # Недостаточная длина
        "12",   # Очень короткий номер
        ""      # Пустой номер
    ]


# 5. Фикстуры для тестов функции mask_account_card
# Фикстура для корректных данных маскировки карт и счетов


@pytest.fixture
def valid_mask_data() -> List[Tuple[str, str, str]]:
    """Фикстура для корректных входных данных"""
    return [
        ("Visa 4567891234567890", "Visa", "4567891234567890"),
        ("Maestro 5432109876543210", "Maestro", "5432109876543210"),
        ("Счет 98765432101234567890", "Счет", "98765432101234567890")
    ]

# Фикстура для параметризованных тестов с различными форматами данных


@pytest.fixture
def parametrized_mask_data() -> List[Tuple[str, str]]:
    """Фикстура для параметризованных тестов"""
    return [
        ("Visa 1111222233334444", "1111222233334444"),
        ("Maestro 5555666677778888", "5555666677778888"),
        ("Счет 12345678901234567890", "12345678901234567890"),
        ("Visa Classic 9876543210987654", "9876543210987654"),
        ("Maestro Gold 4444333322221111", "4444333322221111"),
        ("Счет Premium 99998888777766665555", "99998888777766665555")
    ]

# Фикстура для некорректных входных данных


@pytest.fixture
def invalid_mask_data() -> List[Tuple[str, str]]:
    """Фикстура для некорректных входных данных"""
    return [
        ("", "Строка не должна быть пустой."),  # Пустая строка
        ("UnknownType 1234567890123456", "Неизвестный тип информации. Ожидалось 'Visa', 'Maestro' или 'Счет'."),
        ("Visa", "Неизвестный тип информации. Ожидалось 'Visa', 'Maestro' или 'Счет'."),  # Отсутствие номера
        ("Visa 1234", "не является допустимым номером карты или счета")  # Неверный формат номера
    ]


# 6. Параметризованный тест для тестов функции sort_by_date

# Тестовые данные для параметризации
test_data = [
    # Тест 1: Сортировка корректных данных по убыванию
    (
        [
            {"id": 1, "date": "2023-10-05T14:48:00"},
            {"id": 2, "date": "2023-10-03T10:30:00"},
            {"id": 3, "date": "2023-10-07T09:15:00"}
        ],
        True,  # descending=True
        [
            {"id": 3, "date": "2023-10-07T09:15:00"},
            {"id": 1, "date": "2023-10-05T14:48:00"},
            {"id": 2, "date": "2023-10-03T10:30:00"}
        ]
    ),
    # Тест 2: Сортировка корректных данных по возрастанию
    (
        [
            {"id": 1, "date": "2023-10-05T14:48:00"},
            {"id": 2, "date": "2023-10-03T10:30:00"},
            {"id": 3, "date": "2023-10-07T09:15:00"}
        ],
        False,  # descending=False
        [
            {"id": 2, "date": "2023-10-03T10:30:00"},
            {"id": 1, "date": "2023-10-05T14:48:00"},
            {"id": 3, "date": "2023-10-07T09:15:00"}
        ]
    ),
    # Тест 3: Сортировка при одинаковых датах (должен сохранять порядок)
    (
        [
            {"id": 1, "date": "2023-10-05T14:48:00"},
            {"id": 2, "date": "2023-10-05T14:48:00"},
            {"id": 3, "date": "2023-10-05T14:48:00"}
        ],
        True,  # descending=True
        [
            {"id": 1, "date": "2023-10-05T14:48:00"},
            {"id": 2, "date": "2023-10-05T14:48:00"},
            {"id": 3, "date": "2023-10-05T14:48:00"}
        ]
    ),
    # Тест 4: Некорректные форматы дат (ожидается ValueError)
    (
        [
            {"id": 1, "date": "2023-10-05T14:48:00"},
            {"id": 2, "date": "invalid_date"},
            {"id": 3, "date": "2023-10-07T09:15:00"}
        ],
        True,  # descending=True
        ValueError  # Ожидаемое исключение
    ),
    # Тест 5: Пропущенный ключ 'date' (ожидается KeyError)
    (
        [
            {"id": 1, "date": "2023-10-05T14:48:00"},
            {"id": 2},  # Пропущен ключ 'date'
            {"id": 3, "date": "2023-10-07T09:15:00"}
        ],
        True,  # descending=True
        KeyError  # Ожидаемое исключение
    )
]


# Параметризованный тест

@pytest.mark.parametrize("data, descending, expected", test_data)
def test_sort_by_date(
    data: List[Dict[str, str]],
    descending: bool,
    expected: Union[List[Dict[str, str]], type]
) -> None:
    if isinstance(expected, list):  # Если ожидается список (корректные данные)
        result = sort_by_date(data, descending=descending)
        assert result == expected, f"Ошибка при сортировке данных: {data}"
    elif expected == ValueError:  # Если ожидается ValueError
        with pytest.raises(ValueError, match="Invalid isoformat string"):
            sort_by_date(data, descending=descending)
    elif expected == KeyError:  # Если ожидается KeyError
        with pytest.raises(KeyError):
            sort_by_date(data, descending=descending)
