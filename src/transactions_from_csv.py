from typing import Any, Dict, List
import pandas as pd
import logging

logging.basicConfig(level=logging.ERROR)


def load_transactions_from_csv(file_path: str) -> List[Dict[Any, Any]]:
    """
    Функция для считывания финансовых операций из CSV-файла.

    Аргументы:
        file_path (str): Путь к файлу CSV.

    Возвращает:
        List[Dict[Any, Any]]: Список словарей с транзакциями.
    """
    try:
        df = pd.read_csv(file_path)
        # Преобразуем DataFrame в список словарей
        transactions: List[Dict[Any, Any]] = df.to_dict(orient='records')
    except FileNotFoundError:
        logging.error(f"Файл не найден: {file_path}")
        transactions = []
    except Exception as e:
        logging.error(f"Произошла ошибка при чтении файла CSV: {e}")
        transactions = []

    return transactions
