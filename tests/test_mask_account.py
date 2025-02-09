import pytest
from src.masks import get_mask_account


def test_mask_correctness() -> None:
    # Тестируем правильность маскирования номера счета
    assert get_mask_account("123456789") == "6789"
    assert get_mask_account("987654321") == "4321"
    assert get_mask_account("00001234") == "1234"


def test_various_formats_and_lengths() -> None:
    # Тестируем функцию с различными форматами и длинами номеров счетов
    assert get_mask_account("1234") == "1234"  # Минимальная длина
    assert get_mask_account("00001") == "0001"  # С нулями в начале
    assert get_mask_account("1234567890123456") == "3456"  # Длинный номер


def test_short_account_number() -> None:
    # Тестируем, что функция корректно обрабатывает короткие номера счетов
    with pytest.raises(ValueError, match="Номер счета должен содержать как минимум 4 цифры."):
        get_mask_account("123")
    with pytest.raises(ValueError, match="Номер счета должен содержать как минимум 4 цифры."):
        get_mask_account("12")
    with pytest.raises(ValueError, match="Номер счета должен содержать как минимум 4 цифры."):
        get_mask_account("")
