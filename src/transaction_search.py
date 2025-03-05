import re
import unicodedata
from typing import Dict, List


def normalize_text(text: str) -> str:
    """Нормализует текст, удаляя диакритические знаки."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ).lower()


def search_transactions(transactions: List[Dict], search_string: str) -> List[Dict]:
    """Ищет транзакции по частичному совпадению с учётом Unicode."""
    search_pattern = re.compile(
        re.escape(normalize_text(search_string)),
        re.IGNORECASE
    )

    return [
        transaction
        for transaction in transactions
        if search_pattern.search(normalize_text(transaction.get('description', '')))
    ]
