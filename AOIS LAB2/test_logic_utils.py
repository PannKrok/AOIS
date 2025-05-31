import pytest
from logic_utils import build_sknf, build_sdnf

def normalize_formula(formula: str) -> set:
    if '&' in formula:
        sep = '&'
    elif '|' in formula:
        sep = '|'
    else:
        return {formula}

    parts = formula.split(sep)
    parts = [p.strip("() ") for p in parts]
    return set(parts)

def test_build_sknf_basic():
    table = {
        0: [0, 0, 1],
        1: [0, 1, 0],
        2: [1, 0, 0],
        3: [1, 1, 1],
    }
    vars = ['a', 'b']
    result = build_sknf(table, vars)
    expected = "(!a|b)&(a|!b)"
    assert normalize_formula(result) == normalize_formula(expected)


