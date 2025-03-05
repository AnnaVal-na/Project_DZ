import pytest

from src.masks import get_mask_account, get_mask_card_number
from src.widget import mask_account_card

# Тест для проверки правильности распознавания типа и применения маскировки


def test_mask_account_card_recognition() -> None:
    # Тест для карты Visa
    visa_info = "Visa 4567891234567890"
    masked_visa = mask_account_card(visa_info)
    assert masked_visa == get_mask_card_number("4567891234567890"), "Ошибка при маскировке номера Visa"

    # Тест для карты Maestro
    maestro_info = "Maestro 5432109876543210"
    masked_maestro = mask_account_card(maestro_info)
    assert masked_maestro == get_mask_card_number("5432109876543210"), "Ошибка при маскировке номера Maestro"

    # Тест для счета
    account_info = "Счет 98765432101234567890"
    masked_account = mask_account_card(account_info)
    assert masked_account == get_mask_account("98765432101234567890"), "Ошибка при маскировке номера счета"


@pytest.mark.parametrize("info, expected", [
    ("Visa 1111222233334444", get_mask_card_number("1111222233334444")),
    ("Maestro 5555666677778888", get_mask_card_number("5555666677778888")),
    ("Счет 12345678901234567890", get_mask_account("12345678901234567890")),
    ("Visa Classic 9876543210987654", get_mask_card_number("9876543210987654")),
    ("Maestro Gold 4444333322221111", get_mask_card_number("4444333322221111")),
    ("Счет Premium 99998888777766665555", get_mask_account("99998888777766665555"))
])
def test_mask_account_card_parametrized(info: str, expected: str) -> None:
    result = mask_account_card(info)
    assert result == expected, f"Ошибка при обработке: {info}"


def test_mask_account_card_invalid_input() -> None:
    # Пустая строка
    with pytest.raises(ValueError, match="Строка не должна быть пустой."):
        mask_account_card("")

    # Неизвестный тип информации
    with pytest.raises(ValueError, match="Неизвестный тип информации. Ожидалось 'Visa', 'Maestro' или 'Счет'."):
        mask_account_card("UnknownType 1234567890123456")

    # Отсутствие номера в строке
    #     with pytest.raises(ValueError, match="Неизвестный тип информации. Ожидалось 'Visa', 'Maestro' или 'Счет'."):
    #         mask_account_card("Visa")
    #
    #     # Неверный формат номера (слишком короткий)
    #     with pytest.raises(ValueError, match="не является допустимым номером карты или счета"):
    #         mask_account_card("Visa 1234")
