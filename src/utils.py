import json
import logging
import os
from typing import Any, Dict, List

# Проверка и создание директории для логов
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Настройка логирования для модуля utils
logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)

# Создание обработчика для записи логов в файл
file_handler = logging.FileHandler(os.path.join(log_dir, 'utils.log'), mode='w')
file_handler.setLevel(logging.DEBUG)

# Форматирование логов
file_formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Добавление обработчика к логгеру
logger.addHandler(file_handler)


def load_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """Функция для загрузки транзакций из JSON-файла."""
    logger.debug(f"Попытка загрузить транзакции из файла: {file_path}")

    if not os.path.exists(file_path):
        logger.error(f"Файл не найден: {file_path}")
        return []

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if isinstance(data, list):
                logger.info(f"Успешно загружены {len(data)} транзакций из файла: {file_path}")
                return data
            else:
                logger.warning(f"Данные из файла не являются списком: {file_path}")
                return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return []
    except IOError as e:
        logger.error(f"Ошибка ввода-вывода при работе с файлом {file_path}: {e}")
        return []
