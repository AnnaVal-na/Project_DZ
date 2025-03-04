from typing import Any, Dict, List

import pandas as pd

# Чтение CSV файла
csv_file = 'transactions.csv'
df_csv = pd.read_csv(csv_file)

# Вывод первых 5 строк CSV файла
print("Содержимое CSV файла:")
print(df_csv.head())


def load_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Функция для считывания финансовых операций из CSV-файла.

    Аргументы:
        file_path (str): Путь к файлу CSV.

    Возвращает:
        List[Dict[str, Any]]: Список словарей с транзакциями.
    """
    try:
        df = pd.read_csv(file_path)
        # Преобразуем DataFrame в список словарей и приводим ключи к строкам
        transactions: List[Dict[str, Any]] = [
            {str(k): v for k, v in record.items()}
            for record in df.to_dict(orient='records')
        ]
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
        transactions = []
    except Exception as e:
        print(f"Произошла ошибка при чтении файла CSV: {e}")
        transactions = []

    return transactions
