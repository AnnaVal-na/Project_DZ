import csv
import json
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd


def load_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из JSON-файла.

    :param file_path: Путь к JSON-файлу.
    :return: Список транзакций в виде словарей.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        transactions = json.load(file)
        return [{str(k): v for k, v in transaction.items()} for transaction in transactions]


def load_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из CSV-файла.

    :param file_path: Путь к CSV-файлу.
    :return: Список транзакций в виде словарей.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [{str(k): v for k, v in row.items()} for row in reader]


def load_transactions_from_xlsx(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из XLSX-файла.

    :param file_path: Путь к XLSX-файлу.
    :return: Список транзакций в виде словарей.
    """
    df = pd.read_excel(file_path)
    return [{str(k): v for k, v in row.items()} for _, row in df.iterrows()]


def filter_transactions_by_status(transactions: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданному статусу.

    :param transactions: Список транзакций в виде словарей.
    :param status: Статус для фильтрации (например, 'EXECUTED', 'CANCELED', 'PENDING').
    :return: Список транзакций с заданным статусом.
    """
    return [t for t in transactions if t.get('status') == status]


def sort_transactions(transactions: List[Dict[str, Any]], ascending: bool) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по дате.

    :paramtransactions: Список транзакций в виде словарей.
    :param ascending: Если True, сортирует по возрастанию, если False - по убыванию.
    :return: Отсортированный список транзакций.
    """
    return sorted(transactions, key=lambda x: parse_date(x.get('date')), reverse=not ascending)


def parse_date(date_str: Any) -> Any:
    """
    Преобразует строку даты в объект datetime. Если преобразование невозможно, возвращает None.

    :param date_str: Строка с датой.
    :return: Объект datetime или None, если преобразование невозможно.
    """
    if isinstance(date_str, str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")  # Убедитесь, что формат даты соответствует вашему формату
        except ValueError:
            return None
    return None


def print_transactions(transactions: List[Dict[str, Any]]) -> None:
    """
    Выводит список транзакций на экран.

    :param transactions: Список транзакций в виде словарей.
    """
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    print(f"Всего банковских операций в выборке: {len(transactions)}\n")
    for t in transactions:
        print(f"{t.get('date')} {t.get('description')}")
        print(f"Счет {t.get('account')}")
        print(f"Сумма: {t.get('amount')} {t.get('currency')}\n")


def main() -> None:
    """
    Основная функция программы, которая управляет потоком выполнения и взаимодействием с пользователем.
    """
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ")
    file_path = input("Введите путь к файлу: ")

    transactions = []  # Инициализируем переменную

    if choice == '1':
        transactions = load_transactions_from_json(file_path)
    elif choice == '2':
        transactions = load_transactions_from_csv(file_path)
    elif choice == '3':
        transactions = load_transactions_from_xlsx(file_path)
    else:
        print("Неверный выбор. Завершение программы.")
        return

    # Используем transactions для вывода на экран
    print_transactions(transactions)
    if __name__ == "__main__":
        main()
