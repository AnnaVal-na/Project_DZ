import csv
import json
from datetime import datetime
from typing import Any, Dict, List, Optional
import pandas as pd


def load_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из JSON-файла с обработкой ошибок."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            transactions = json.load(file)
            return [{str(k): v for k, v in t.items()} for t in transactions]
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        raise ValueError(f"Ошибка загрузки JSON: {e}")


def load_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из CSV-файла с обработкой ошибок."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [row for row in csv.DictReader(file)]
    except FileNotFoundError as e:
        raise ValueError(f"Файл не найден: {e}")


def load_transactions_from_xlsx(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из XLSX-файла с обработкой ошибок."""
    try:
        df = pd.read_excel(file_path)
        return [{str(k): v for k, v in row.items()} for _, row in df.iterrows()]
    except FileNotFoundError as e:
        raise ValueError(f"Файл не найден: {e}")


def filter_transactions_by_status(transactions: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
    """Регистронезависимая фильтрация транзакций по статусу."""
    target_status = status.upper()
    return [t for t in transactions if str(t.get('status', '')).upper() == target_status]


def sort_transactions(transactions: List[Dict[str, Any]], ascending: bool = True) -> List[Dict[str, Any]]:
    """Безопасная сортировка по дате с обработкой некорректных значений."""
    return sorted(
        transactions,
        key=lambda x: parse_date(x.get('date')) or datetime.min,
        reverse=not ascending
    )


def parse_date(date_str: Optional[Any]) -> Optional[datetime]:
    """Универсальный парсинг дат с поддержкой разных форматов."""
    if isinstance(date_str, str):
        for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%m/%d/%Y"):
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
    return None


def print_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Улучшенный вывод с форматированием и проверкой данных."""
    if not transactions:
        print("\nНет транзакций для отображения.")
        return

    print(f"\nВсего операций: {len(transactions)}")
    for t in transactions:
        date = parse_date(t.get('date')) or "Дата неизвестна"
        print(f"\n{date.strftime('%d.%m.%Y') if isinstance(date, datetime) else date}"
              f" | {t.get('description', 'Без описания')}")
        print(f"Счет: {t.get('account', 'Не указан')}")
        print(f"Сумма: {t.get('amount', 'N/A')} {t.get('currency', '')}")


def get_user_choice(options: List[str]) -> str:
    """Универсальная функция для получения корректного выбора пользователя."""
    while True:
        print("\nВыберите:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        choice = input("Ваш выбор: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return choice
        print("Ошибка ввода. Попробуйте снова.")


def main() -> None:
    print("Программа анализа банковских транзакций\n" + "=" * 40)

    # Выбор источника данных
    file_type = get_user_choice(["JSON", "CSV", "XLSX"])
    file_path = input("\nВведите полный путь к файлу: ").strip()

    try:
        if file_type == '1':
            transactions = load_transactions_from_json(file_path)
        elif file_type == '2':
            transactions = load_transactions_from_csv(file_path)
        else:
            transactions = load_transactions_from_xlsx(file_path)
    except ValueError as e:
        print(f"\nОшибка: {e}")
        return

    # Фильтрация по статусу
    if any('status' in t for t in transactions):
        if input("\nФильтровать по статусу? (y/n): ").lower() == 'y':
            statuses = {str(t.get('status', '')).upper() for t in transactions}
            print("\nДоступные статусы:", *statuses)
            while True:
                desired_status = input("Введите статус: ").upper()
                if desired_status in statuses:
                    transactions = filter_transactions_by_status(transactions, desired_status)
                    break
                print("Некорректный статус. Попробуйте еще раз.")

    # Сортировка
    if input("\nСортировать по дате? (y/n): ").lower() == 'y':
        sort_order = get_user_choice(["По возрастанию", "По убыванию"])
        transactions = sort_transactions(transactions, sort_order == '1')

    print_transactions(transactions)


if __name__ == "__main__":
    main()
