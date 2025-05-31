import pytest
from main import main


def test_menu_conversion(monkeypatch, capsys):
    inputs = iter(["1", "5", ""])  # "1" – выбор пункта, "5" – ввод числа, "" – выход
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(StopIteration):  # main() — бесконечный цикл, выходим вручную
        main()

    output = capsys.readouterr().out
    assert "Прямой" in output
    assert "Обратный" in output
    assert "Дополнительный" in output
