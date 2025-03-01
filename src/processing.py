from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(data: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """
    Функция принимает список словарей и опционально
    значение для ключа state (по умолчанию 'EXECUTED'). Функция
    возвращает новый список словарей, содержащий только те словари,
    у которых ключ state соответствует указанному значению.
    """
    return [item for item in data if item.get('state') == state]


def sort_by_date(data: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """
    Функция принимает список словарей и необязательный
    параметр, задающий порядок сортировки (по умолчанию — убывание).
    Функция должна возвращать новый список, отсортированный по дате
    (date)
    """
    return sorted(data, key=lambda x: datetime.fromisoformat(x['date']), reverse=descending)
