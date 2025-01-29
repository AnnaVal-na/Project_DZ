def get_mask_card_number(card_number: str) -> str:
    """
    Первая функция принимает строку с номером карты.
    Маскирует номер карты в формате XXXX XX** **** XXXX.
    :param card_number: Строка, содержащая номер карты.
    :return: Замаскированный номер карты.
    """
    if len(card_number) != 16:
        raise ValueError("Номер карты должен содержать ровно 16 цифр.")

    # Разбиваем номер карты на части
    part1 = card_number[:4]
    part2 = card_number[4:6]
    part3 = "****"
    part4 = card_number[12:]

    return f"{part1} {part2}** {part3} {part4}"


def get_mask_account(account_number: str) -> str:
    """
    Вторая функция принимает строку с номером счета.
    Маскирует номер счета в формате **XXXX.

    :param account_number: Строка, содержащая номер счета.
    :return: Замаскированный номер счета.
    """
    if len(account_number) < 4:
        raise ValueError("Номер счета должен содержать как минимум 4 цифры.")

    # Берем последние 4 цифры номера счета
    last_four = account_number[-4:]

    return f"**{last_four}"
