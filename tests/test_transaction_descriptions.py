import pytest
from typing import List, Dict, Generator


# Функция для тестирования
def transaction_descriptions(transactions: List[Dict[str, str]]) -> Generator[str, None, None]:
    for transaction in transactions:
        yield transaction.get('description', 'Описание отсутствует')


# Фикстура для создания данных для тестов
@pytest.fixture
def sample_transactions() -> List[Dict[str, str]]:
    return [
        {'description': 'Перевод организации'},
        {'description': 'Перевод со счета на счет'},
        {'description': 'Перевод с карты на карту'},
        {'description': 'Перевод организации'}
    ]


# Тесты с параметризацией для различных кейсов
@pytest.mark.parametrize("transactions, expected", [
    # Проверка стандартного списка транзакций
    ([{'description': 'Перевод организации'},
      {'description': 'Перевод со счета на счет'},
      {'description': 'Перевод с карты на карту'},
      {'description': 'Перевод организации'}],
     ['Перевод организации',
      'Перевод со счета на счет',
      'Перевод с карты на карту',
      'Перевод организации']),

    # Проверка пустого списка
    ([], []),

    # Проверка, когда описание отсутствует
    ([{'not_description': 'Нет описания'}],
     ['Описание отсутствует'])
])
def test_transaction_descriptions(transactions: List[Dict[str, str]], expected: List[str]) -> None:
    # Создаем генератор из функции
    descriptions = transaction_descriptions(transactions)

    # Проверяем, что все ожидаемые значения совпадают с реальными
    for exp in expected:
        assert next(descriptions) == exp

    # Проверяем, что генератор исчерпан
    with pytest.raises(StopIteration):
        next(descriptions)


# Пример использования фикстуры в тесте
def test_transaction_descriptions_with_fixture(sample_transactions: List[Dict[str, str]]) -> None:
    descriptions = transaction_descriptions(sample_transactions)
    expected = [
        'Перевод организации',
        'Перевод со счета на счет',
        'Перевод с карты на карту',
        'Перевод организации'
    ]

    for exp in expected:
        assert next(descriptions) == exp

    with pytest.raises(StopIteration):
        next(descriptions)
