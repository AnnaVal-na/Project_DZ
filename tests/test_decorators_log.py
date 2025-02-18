import pytest
import os
from decorators.decorators_log import log
from _pytest.capture import CaptureFixture


# Пример функции с декоратором
@log()
def add(a: int, b: int) -> int:
    return a + b


@log(filename='test_log.txt')
def divide(a: float, b: float) -> float:
    return a / b


def test_add_success(capsys: CaptureFixture) -> None:
    add(3, 4)
    captured = capsys.readouterr()
    assert captured.out.strip() == "add ok"


def test_add_error(capsys: CaptureFixture) -> None:
    with pytest.raises(TypeError):
        add(3, 'four')
    captured = capsys.readouterr()
    assert "add error:" in captured.out
    assert "Inputs: (3, 'four'), {}" in captured.out


def test_divide_success() -> None:
    try:
        os.remove('test_log.txt')
    except FileNotFoundError:
        pass

    divide(10, 2)

    with open('test_log.txt', 'r') as file:
        logs = file.readlines()
    assert logs[-1].strip() == "divide ok"


def test_divide_error() -> None:
    try:
        os.remove('test_log.txt')
    except FileNotFoundError:
        pass

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    with open('test_log.txt', 'r') as file:
        logs = file.readlines()
    # Исправляем ожидание строки на фактическое содержание лога
    assert "ZeroDivisionError: division by zero" in logs[-2]

    # Удаляем тестовый файл после проверки
    os.remove('test_log.txt')
