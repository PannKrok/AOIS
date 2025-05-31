import pytest
from io import StringIO
import sys

import builtins

import main

def run_launch_with_input(user_input):
    # Перехватываем stdout
    captured_out = StringIO()
    sys.stdout = captured_out

    # Патчим input()
    original_input = builtins.input
    builtins.input = lambda _: user_input

    try:
        main.launch()
    except Exception as e:
        # возвращаем ошибку как строку, чтобы проверить
        output = captured_out.getvalue()
        builtins.input = original_input
        sys.stdout = sys.__stdout__
        return output, str(e)
    else:
        output = captured_out.getvalue()
        return output, None
    finally:
        builtins.input = original_input
        sys.stdout = sys.__stdout__


def test_launch_valid_formula():
    output, error = run_launch_with_input("(a&b)|c")
    assert error is None
    assert "СКНФ:" in output
    assert "СДНФ:" in output
    assert "Индекс (бинарный):" in output


def test_launch_invalid_formula():
    output, error = run_launch_with_input("invalid_formula#")
    assert error is not None
    assert "Ошибка: недопустимые символы во входной строке." in error

if __name__ == "__main__":
    pytest.main()
