import pytest
from src.widget import get_date


def test_get_date_correct_conversion() -> None:
    input_date = "2023-10-05T14:48:00"
    expected_output = "05.10.2023"
    assert get_date(input_date) == expected_output, f"Ошибка при преобразовании даты {input_date}"


@pytest.mark.parametrize("input_date, expected_output", [
    ("2023-01-01T00:00:00", "01.01.2023"),  # Начало года
    ("2023-12-31T23:59:59", "31.12.2023"),  # Конец года
    ("2023-03-01T12:00:00", "01.03.2023"),  # Первый день месяца
    ("2023-03-31T12:00:00", "31.03.2023"),  # Последний день месяца
    ("2020-02-29T00:00:00", "29.02.2020"),  # Високосный год
    ("2023-11-05T14:48:00", "05.11.2023"),  # Обычная дата
])
def test_get_date_various_formats(input_date: str, expected_output: str) -> None:
    result = get_date(input_date)
    assert result == expected_output, f"Ошибка при обработке даты {input_date}"


def test_get_date_invalid_input() -> None:
    # Проверка обработки None
    with pytest.raises(TypeError):
        get_date(None)

    # Корректные тестовые кейсы для ошибок
    invalid_cases = [
        "invalid_date",  # Полностью невалидный формат
        "2023-13-01T00:00:00",  # Несуществующий месяц
        "2023-02-30T00:00:00",  # Несуществующий день
        "2023T14:00:00",  # Неполная дата
        ""  # Пустая строка
    ]

    for case in invalid_cases:
        with pytest.raises(ValueError, match="Invalid isoformat string"):
            get_date(case)
