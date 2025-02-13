import pytest
from typing import List, Tuple
from src.generators import card_number_generator


# Фикстура для тестовых диапазонов генерации номеров карт
@pytest.fixture
def card_number_ranges() -> List[Tuple[int, int]]:
    """Фикстура для различных диапазонов генерации номеров карт"""
    return [
        (1, 3),  # Маленький диапазон
        (100, 102),  # Средний диапазон
        (9999999999999998, 10000000000000000),  # Крайние значения диапазона
    ]


# Фикстура для проверки форматирования номеров карт
@pytest.fixture
def card_format_test_data() -> List[Tuple[int, str]]:
    """Фикстура для проверки форматирования номеров карт"""
    return [
        (1, "0000 0000 0000 0001"),
        (1234567890123456, "1234 5678 9012 3456"),
        (9999999999999999, "9999 9999 9999 9999"),
    ]


# Тест №1: Проверка правильности выдачи номеров карт в заданном диапазоне
def test_card_number_generator_range(card_number_ranges: List[Tuple[int, int]]) -> None:
    for start, end in card_number_ranges:
        expected = [
            f"{num:016d}" for num in range(start, end + 1)
        ]
        result = list(card_number_generator(start, end))
        formatted_expected = [
            f"{num[:4]} {num[4:8]} {num[8:12]} {num[12:]}" for num in expected
        ]
        assert result == formatted_expected, f"Ошибка при генерации номеров карт в диапазоне ({start}, {end})"


# Тест №2: Проверка корректности форматирования номеров карт
@pytest.mark.parametrize("number, expected", [
    (1, "0000 0000 0000 0001"),
    (1234567890123456, "1234 5678 9012 3456"),
    (9999999999999999, "9999 9999 9999 9999"),
])
def test_card_number_generator_format(number: int, expected: str) -> None:
    # Генерируем один номер карты
    result = next(card_number_generator(number, number))
    assert result == expected, f"Ошибка при форматировании номера карты: {number}"


# Тест №3: Проверка обработки крайних значений диапазона и завершения генерации
def test_card_number_generator_edge_cases(card_number_ranges: List[Tuple[int, int]]) -> None:
    for start, end in card_number_ranges:
        result = list(card_number_generator(start, end))
        assert len(result) == (end - start + 1), (
            f"Неверное количество сгенерированных номеров в диапазоне ({start}, {end})"
        )
        if result:
            # Проверяем первый и последний элементы
            first_card = result[0]
            last_card = result[-1]
            assert (
                first_card == f"{start:016d}"[:4]
                + " " + f"{start:016d}"[4:8]
                + " " + f"{start:016d}"[8:12]
                + " " + f"{start:016d}"[12:]
            ), f"Ошибка первого номера в диапазоне ({start}, {end})"
            assert (
                last_card == f"{end:016d}"[:4]
                + " " + f"{end:016d}"[4:8]
                + " " + f"{end:016d}"[8:12]
                + " " + f"{end:016d}"[12:]
            ), f"Ошибка последнего номера в диапазоне ({start}, {end})"
