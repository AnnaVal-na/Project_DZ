def get_mask_card_number(card_number: str) -> str:
    # Проверяем, что номер карты не пустой
    if not card_number:
        raise ValueError("Card number cannot be empty")

    # Проверяем, что в номере карты только цифры
    if not card_number.isdigit():
        raise ValueError("Card number must contain only digits")

    # Проверяем, что длина номера карты равна 16
    if len(card_number) != 16:
        raise ValueError("Card number must be 16 digits long")

    # Маскируем номер карты
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """
    Вторая функция принимает строку с номером счета.
    Маскирует номер счета в формате XXXX.

    :param account_number: Строка, содержащая номер счета.
    :return: Замаскированный номер счета.
    """
    if len(account_number) < 4:
        raise ValueError("Номер счета должен содержать как минимум 4 цифры.")

    # Берем последние 4 цифры номера счета
    last_four = account_number[-4:]

    return last_four
