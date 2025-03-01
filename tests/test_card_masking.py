import pytest

from src.masks import get_mask_card_number


def test_card_number_masking() -> None:
    card_number = "1234567890123456"
    expected_masked = "1234 56** **** 3456"
    assert get_mask_card_number(card_number) == expected_masked


def test_invalid_card_number_length() -> None:
    with pytest.raises(ValueError, match="Card number must be 16 digits long"):
        get_mask_card_number("12345678901234")  # 14 цифр


def test_empty_card_number() -> None:
    with pytest.raises(ValueError, match="Card number cannot be empty"):
        get_mask_card_number("")


def test_invalid_characters() -> None:
    with pytest.raises(ValueError, match="Card number must contain only digits"):
        get_mask_card_number("1234abcd5678efgh")
