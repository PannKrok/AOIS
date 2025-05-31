import pytest
from Binary_helper import Binary_helper
from Builder import Builder
from Parser import Parser
from main import *
from Minimizator import Minimizator

def test_sum_b_with_overflow():
    a = [1, 1, 1]
    b = [0, 0, 1]
    assert Binary_helper.sum_b(a, b) == [0, 0, 0]

def test_calculate_basic():
    assert Binary_helper.calculate([1, 0, 1]) == 5
    assert Binary_helper.calculate([0, 0, 0]) == 0
    assert Binary_helper.calculate([1, 1, 1]) == 7

def test_build_SDNF():
    assert Builder.build_SDNF(["a", "b"], [0, 1]) == "(!a&b)"
    assert Builder.build_SDNF(["x", "y", "z"], [1, 0, 1]) == "(x&!y&z)"

def test_build_SKNF():
    assert Builder.build_SKNF(["a", "b"], [0, 1]) == "(a|!b)"
    assert Builder.build_SKNF(["x", "y", "z"], [1, 0, 1]) == "(!x|y|!z)"

def test_delete_tabulation():
    expr = " a & b \t | c "
    clean = Parser.delete_tabulation(expr)
    assert clean == "a&b|c"

def test_delete_brackets():
    expr = "(1)&(0)|(1)"
    cleaned = Parser.delete_brackets(expr)
    assert cleaned == "1&0|1"

def test_work_w_str_generation():
    expr = "a&b"
    letters = ['a', 'b']
    generator = Parser.work_w_str(expr, letters)

    results = list(generator)
    assert results == [
        ("0&0", [0, 0]),
        ("0&1", [0, 1]),
        ("1&0", [1, 0]),
        ("1&1", [1, 1]),
    ]

def test_bcd_plus_two():
    result = get_D8421_2()
    assert isinstance(result, dict)
    assert set(result.keys()) == {"Y0", "Y1", "Y2", "Y3"}
    for expr in result.values():
        assert isinstance(expr, str)
        assert len(expr) > 0

def test_replace_and_back():
    original = "(A&B)|!D"
    replaced = replace(original)
    assert replaced == "(X3&X2)|!X0"
    restored = replace_back(replaced)
    assert restored == original

def test_check_if_neighbours_should_not_merge():
    a = "(!a&b)"
    b = "(a&!b)"
    result = Minimizator.check_if_neighbours(a, b)
    assert result is None

def test_check_form_with_and_or():
    assert Minimizator.check_form(["(a&b)", "(!a&!b)"]) == "&"
    assert Minimizator.check_form(["(a|b)", "(!a|!b)"]) == "|"

def test_check_form_empty():
    assert Minimizator.check_form([]) is None

def test_scleivanie_no_merge():
    form = ["(a&b)", "(c&d)"]
    result = Minimizator.scleivanie(form, "&")
    assert set(result) == set(form)

def test_scleivanie_till_end_FORM_steps():
    form = ["(a&b)", "(!a&b)", "(a&!b)", "(!a&!b)"]
    steps = Minimizator.scleivanie_till_end_FORM(form)
    assert isinstance(steps, list)
    assert all(isinstance(step, set) for step in steps)
    assert steps[0] == set(form)

def test_build_SDNF_all_ones():
    literals = ['a', 'b', 'c']
    bits = [1, 1, 1]
    result = Builder.build_SDNF(literals, bits)
    assert result == "(a&b&c)"

def test_build_SDNF_mixed_bits():
    literals = ['x', 'y']
    bits = [1, 0]
    result = Builder.build_SDNF(literals, bits)
    assert result == "(x&!y)"

def test_build_SDNF_all_zeros():
    literals = ['a', 'b']
    bits = [0, 0]
    result = Builder.build_SDNF(literals, bits)
    assert result == "(!a&!b)"

def test_build_SKNF_all_zeros():
    literals = ['a', 'b', 'c']
    bits = [0, 0, 0]
    result = Builder.build_SKNF(literals, bits)
    assert result == "(a|b|c)"

def test_build_SKNF_mixed_bits():
    literals = ['x', 'y']
    bits = [1, 0]
    result = Builder.build_SKNF(literals, bits)
    assert result == "(!x|y)"

def test_build_SKNF_all_ones():
    literals = ['a', 'b']
    bits = [1, 1]
    result = Builder.build_SKNF(literals, bits)
    assert result == "(!a|!b)"