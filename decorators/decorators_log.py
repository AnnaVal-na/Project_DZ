import functools
import traceback
from typing import Callable, Any, Optional


def log(filename: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                # Начало выполнения функции
                result = func(*args, **kwargs)

                # Если filename задан, записываем в файл, иначе выводим в консоль
                message = f"{func.__name__} ok"
                if filename:
                    with open(filename, 'a') as file:
                        file.write(message + '\n')
                else:
                    print(message)

                return result
            except Exception as e:
                error_message = f"{func.__name__} error: {str(e)}. Inputs: {args}, {kwargs}"

                # Записываем ошибку в лог
                if filename:
                    with open(filename, 'a') as file:
                        file.write(error_message + '\n')
                else:
                    print(error_message)

                # Выводим трассировку стека для подробностей (по желанию)
                if filename:
                    with open(filename, 'a') as file:
                        file.write(traceback.format_exc() + '\n')
                else:
                    print(traceback.format_exc())

                # Поднимаем исключение дальше, если это требуется
                raise

        return wrapper

    return decorator
