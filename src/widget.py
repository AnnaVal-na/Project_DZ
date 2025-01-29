from masks import get_mask_card_number, get_mask_account
import datetime


def mask_account_card(info: str) -> str:
    """
    Принимает строку с типом и номером карты или счета и возвращает строку с замаскированным номером.

    :param info: Строка, содержащая тип и номер карты или счета.
    :return: Замаскированный номер карты или счета.
    """
    # Разделяем строку на части, чтобы определить тип и номер
    parts = info.split()

    if not parts:
        raise ValueError("Строка не должна быть пустой.")

    # Определяем, что за тип информации передан
    type_info = parts[0]
    number = parts[-1]  # Предполагаем, что номер всегда идет последним

    if type_info.lower() in ['visa', 'maestro']:
        # Если это карта, используем функцию для маскировки карты

        return get_mask_card_number(number)
    elif type_info.lower() == 'счет':
        # Если это счет, используем функцию для маскировки счета
        return get_mask_account(number)
    else:
        raise ValueError("Неизвестный тип информации. Ожидалось 'Visa', 'Maestro' или 'Счет'.")


def get_date(date_str):
    date_obj = datetime.fromisoformat(date_str)
    # Форматируем дату в нужный формат "ДД.ММ.ГГГГ"
    formatted_date = date_obj.strftime("%d.%m.%Y")
    return formatted_date
