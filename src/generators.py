from typing import Dict, Generator, Iterator, List


# Функция 1: Фильтрация транзакций по валюте
def filter_by_currency(transactions: List[Dict], currency: str) -> Iterator[Dict]:
    return (
        transaction
        for transaction in transactions
        if (
            transaction.get('operationAmount') is not None
            and transaction['operationAmount'].get('currency') is not None
            and transaction['operationAmount']['currency'].get('code') == currency
        )
    )


# Функция 2: Генерация описаний транзакций с использованием yield
def transaction_descriptions(transactions: List[Dict[str, str]]) -> Generator[str, None, None]:
    for transaction in transactions:
        yield transaction.get('description', 'Описание отсутствует')


# Пример использования функции:
transactions = [
    {'description': 'Перевод организации'},
    {'description': 'Перевод со счета на счет'},
    {'description': 'Перевод со счета на счет'},
    {'description': 'Перевод с карты на карту'},
    {'description': 'Перевод организации'}
]

# Создаем генератор
descriptions = transaction_descriptions(transactions)

# Выводим первые 5 описаний транзакций
for _ in range(5):
    print(next(descriptions))


# Функция 3: Генератор номеров карт
def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    for number in range(start, end + 1):
        # Форматируем число в строку с ведущими нулями и добавляем пробелы
        card_number: str = f"{number:016d}"
        formatted_card_number: str = f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"
        yield formatted_card_number
