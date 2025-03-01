import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Получаем API_KEY
API_KEY: Optional[str] = os.getenv("API_KEY")  # Явная аннотация типа
print(API_KEY)  # Это выведет ваш API ключ


def get_exchange_rate(api_key: str, base_currency: str, target_currency: str) -> Optional[float]:
    """
    Эта функция делает запрос к API, чтобы получить текущий курс обмена между
    базовой валютой и целевой валютой.
    :param api_key: API-ключ для доступа к сервису
    :param base_currency: Базовая валюта (например, USD или EUR)
    :param target_currency: Целевая валюта (например, RUB)
    :return: Курс обмена или None, если данные недоступны
    """
    url = f"https://api.apilayer.com/exchangerates_data/latest?base={base_currency}&symbols={target_currency}"
    headers = {
        "apikey": api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data: Dict[str, Any] = response.json()  # Аннотируем тип данных JSON
        rate = data['rates'].get(target_currency)  # Получаем курс обмена
        if isinstance(rate, (float, int)):  # Проверяем, является ли курс числом
            return float(rate)  # Возвращаем курс обмена как float
        else:
            return None  # Если курс не найден или не является числом
    else:
        raise Exception("Error fetching exchange rate")


def convert_to_rub(transaction: Dict[str, Any]) -> Optional[float]:
    """
    Эта функция принимает транзакцию в виде словаря (с ключами amount и currency).
    - Если валюта уже в RUB, она просто возвращает сумму.
    - Если валюта USD или EUR, она вызывает get_exchange_rate для получения курса и возвращает сумму в рублях.
    - Если валюта не поддерживается, она выводит сообщение об ошибке.
    :param transaction: Словарь с информацией о транзакции
    :return: Сумма в рублях или None при ошибках
    """
    api_key: Optional[str] = API_KEY  # Теперь используем API_KEY из .env
    if api_key is None:
        print("API key is not set.")
        return None
    amount: Optional[float] = transaction.get('amount')  # Аннотируем тип для amount
    currency: Optional[str] = transaction.get('currency')  # Аннотируем тип для currency
    if amount is None or currency is None:
        print("Transaction must have both amount and currency.")
        return None
    if currency == 'RUB':
        return float(amount)
    elif currency in ['USD', 'EUR']:
        try:
            rate: Optional[float] = get_exchange_rate(api_key, currency, 'RUB')
            if rate is not None:
                return float(amount) * rate
            else:
                return None
        except Exception as e:
            print(f"Error converting currency: {e}")
            return None
    else:
        print("Unsupported currency")
        return None
