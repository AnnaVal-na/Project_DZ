from typing import Any, Dict, List

import openpyxl
import pandas as pd

# Чтение Excel файла
excel_file = 'transactions_excel.xlsx'
df_excel = pd.read_excel(excel_file)

# Вывод первых 5 строк Excel файла
print("Содержимое Excel файла:")
print(df_excel.head())


def load_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """Функция для считывания финансовых операций из Excel-файла.

    Аргументы:
        file_path (str): Путь к файлу Excel.

    Возвращает:
        List[Dict[str, Any]]: Список словарей с транзакциями.
    """
    transactions = []

    try:
        workbook = openpyxl.load_workbook(file_path, data_only=True)
        sheet = workbook.active  # Используем активный лист

        # Проверяем, что sheet не None
        if sheet is None:
            raise ValueError("Активный лист не найден.")

        # Получаем заголовки из первой строки
        headers = [str(cell.value) for cell in sheet[1]]  # Приведение заголовков к строкам

        # Считываем данные построчно, начиная со 2-й строки
        for row in sheet.iter_rows(min_row=2, values_only=True):
            # Проверяем, что row не None и имеет нужную длину
            if row is None or len(row) != len(headers):
                continue  # Пропускаем некорректные строки
            # Приведение ключей к строковому типу
            transaction = {headers[i]: row[i] for i in range(len(headers))}
            transactions.append(transaction)

    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла Excel: {e}")

    return transactions
