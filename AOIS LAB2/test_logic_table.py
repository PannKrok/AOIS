import pytest
from logic_table import (
    to_postfix,
    evaluate_expression,
    generate_truth_table,
    precedence_rank,
    binary_add,
)

def test_to_postfix_basic():
    assert to_postfix("a&b") == "ab&"
    assert to_postfix("a|b&c") == "abc&|"
    assert to_postfix("a>(b|c)") == "abc|>"
    assert to_postfix("!(a&b)") == "ab&!"
    assert to_postfix("(a~b)&c") == "ab~c&"

def test_precedence_rank():
    assert precedence_rank(">") > precedence_rank("~")
    assert precedence_rank("~") > precedence_rank("&")
    assert precedence_rank("&") > precedence_rank("!")
    assert precedence_rank("!") == precedence_rank("|")
    assert precedence_rank("(") < precedence_rank("|")
    assert precedence_rank("invalid") == -1



def test_binary_add_basic():
    assert binary_add([0, 0, 1], [0, 0, 1]) == [0, 1, 0]
    assert binary_add([1, 1, 1], [0, 0, 1]) == [1, 0, 0, 0]  # overflow
    assert binary_add([0, 1, 1], [0, 1, 1]) == [1, 1, 0]

def test_evaluate_expression():
    # a = 1, b = 0
    assert evaluate_expression([1, 0], "ab&") == 0
    assert evaluate_expression([1, 0], "ab|") == 1
    assert evaluate_expression([1, 0], "ab>") == 0
    assert evaluate_expression([1, 1], "ab~") == 1
    assert evaluate_expression([0, 1], "ab~") == 0
    assert evaluate_expression([1], "a!") == 0
    assert evaluate_expression([0], "a!") == 1

def test_generate_truth_table_no_print():
    rows, vars = generate_truth_table("a&b", show=False)
    assert vars == ["a", "b"]
    assert len(rows) == 4
    assert rows[3][-1] == 1  # a=1, b=1 => 1
    assert rows[0][-1] == 0  # a=0, b=0 => 0

def test_generate_truth_table_complex_expr():
    expr = "!(a&b)|c"
    rows, vars = generate_truth_table(expr, show=False)
    assert vars == ["a", "b", "c"]
    assert len(rows) == 8
