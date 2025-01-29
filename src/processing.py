def filter_by_state(data, state='EXECUTED'):
    """
    Фильтрует список словарей по указанному значению ключа 'state'.

    :param data: список словарей, где каждый словарь содержит ключ 'state'
    :param state: значение состояния для фильтрации (по умолчанию 'EXECUTED')
    :return: новый список словарей, отфильтрованный по указанному состоянию
    """
    return [item for item in data if item.get('state') == state]


def sort_by_date(data, descending=True):
    """
    Сортирует список словарей по ключу 'date'.

    :param data: список словарей, где каждый словарь содержит ключ 'date'
    :param descending: порядок сортировки: True для убывания, False для возрастания
    :return: новый список словарей, отсортированный по дате
    """
    return sorted(data, key=lambda x: datetime.fromisoformat(x['date']), reverse=descending)