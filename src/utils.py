import json
import os
from typing import Any, Dict, List


def load_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """ Функция, которая принимает на вход путь до JSON-файла
    и возвращает список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает
    пустой список."""
    # Проверяем, существует ли файл
    if not os.path.exists(file_path):
        return []

    # Пытаемся открыть и загрузить данные из JSON-файла
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Проверяем, является ли загруженные данные списком
            if isinstance(data, list):
                return data
            else:
                return []
    except (json.JSONDecodeError, IOError):
        return []
