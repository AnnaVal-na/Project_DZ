import logging
import os

# Создание папки для логов, если она не существует
if not os.path.exists('logs'):
    os.makedirs('logs')

# Создание логера
logger = logging.getLogger(__name__)  # Исправлено: заменён name на __name__
logger.setLevel(logging.DEBUG)

# Создание file_handler
file_handler = logging.FileHandler('logs/masks.log', mode='w')
file_handler.setLevel(logging.DEBUG)

# Создание formatter
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Добавление handler к логеру
logger.addHandler(file_handler)


# Примеры функций с логированием
def example_function_success() -> None:
    logger.info("Функция выполнена успешно.")


def example_function_error() -> None:
    try:
        # Здесь может произойти ошибка
        raise ValueError("Произошла ошибка!")
    except Exception as e:
        logger.error("Ошибка в функции: %s", e)
        logger.exception("Исключение было вызвано.")


# Вызовы функций для примера

example_function_success()
example_function_error()


def get_mask_card_number(card_number: str) -> str:
    try:
        # Проверяем, что номер карты не пустой
        if not card_number:
            logger.error("Попытка передать пустой номер карты.")
            raise ValueError("Card number cannot be empty")

        # Проверяем, что в номере карты только цифры
        if not card_number.isdigit():
            logger.error("Номер карты содержит недопустимые символы.")
            raise ValueError("Card number must contain only digits")

        # Проверяем, что длина номера карты равна 16
        if len(card_number) != 16:
            logger.error("Неверная длина номера карты: %s", card_number)
            raise ValueError("Card number must be 16 digits long")

        # Маскируем номер карты
        masked_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        logger.info("Номер карты успешно замаскирован: %s", masked_number)
        return masked_number

    except ValueError as ve:
        logger.exception("Произошла ошибка при маскировании номера карты: %s", ve)
        raise

    except Exception as e:
        logger.exception("Необработанная ошибка при маскировании номера карты: %s", e)
        raise


def get_mask_account(account_number: str) -> str:
    """
    Вторая функция принимает строку с номером счета.
    Маскирует номер счета в формате XXXX.

    :param account_number: Строка, содержащая номер счета.
    :return: Замаскированный номер счета.
    """
    try:
        if len(account_number) < 4:
            logger.error("Недостаточная длина номера счета: %s", account_number)
            raise ValueError("Номер счета должен содержать как минимум 4 цифры.")

        # Берем последние 4 цифры номера счета
        masked_account = "XXXX" + account_number[-4:]
        logger.info("Номер счета успешно замаскирован: %s", masked_account)
        return masked_account

    except ValueError as ve:
        logger.exception("Произошла ошибка при маскировании номера счета: %s", ve)
        raise
    except Exception as e:
        logger.exception("Необработанная ошибка при маскировании номера счета: %s", e)
        raise
