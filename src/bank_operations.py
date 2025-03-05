from collections import Counter
from typing import Dict, List


def count_operations_by_category(operations: List[Dict[str, str]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по категориям.

    :param operations: Список словарей с данными о банковских операциях.
    :param categories: Список категорий операций.
    :return: Словарь с количеством операций по категориям.
    """
    category_count: Counter = Counter()  # Добавлена аннотация типа

    for operation in operations:
        description = operation.get('description')
        if description in categories:
            category_count[description] += 1

    # Преобразуем Counter в обычный словарь с категориями
    return {category: category_count[category] for category in categories}
