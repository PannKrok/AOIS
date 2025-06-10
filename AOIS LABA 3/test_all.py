# test_main_program.py
from raschet_tablich import *
import builtins
import pytest
from karno import *
from snf import *
from tablica import *
from main import run_program
# Мокаем используемые функции
import sys
from raschet import *

def test_simplify_implicants_dnf():
    terms = [["a1", "a2"], ["a1", "!a2"], ["a2", "a3"], ["!a2", "a3"]]
    expected = [["a1"], ["a3"]]
    result = simplify_implicants(terms, is_dnf=True)
    assert sorted(result) == sorted(expected)

def test_simplify_implicants_no_merge():
    terms = [["a1", "a2"], ["a3", "a4"]]
    result = simplify_implicants(terms, is_dnf=True)
    assert sorted(result) == sorted([["a1", "a2"], ["a3", "a4"]])

def test_get_variable_assignments_dnf():
        term = ["a1", "!a2"]
        expected = {"a1": True, "a2": False}
        result = get_variable_assignments(term, is_dnf=True)
        assert result == expected

def test_get_variable_assignments_cnf():
        term = ["!a1", "a2"]
        expected = {"a1": True, "a2": False}
        result = get_variable_assignments(term, is_dnf=False)
        assert result == expected

def test_apply_assignments_simple():
    terms = [["a1", "!a2"], ["!a1", "a3"]]
    assignments = {"a1": True, "a2": False, "a3": True}
    result = apply_assignments(terms, assignments)
    assert result == [[True, True], [False, True]]

def test_apply_assignments_partial():
    terms = [["a1", "a2"], ["!a3"]]
    assignments = {"a1": False}
    result = apply_assignments(terms, assignments)
    assert result == [[False, "a2"], ['!a3']]


def test_create_matrix_basic():
    candidates = [["a1"], ["a1", "a2"]]
    targets = [["a1", "a2"], ["a1", "!a2"], ["a1"]]
    expected = [
        [True, True, True],
        [True, False, False]
    ]
    result = create_matrix(candidates, targets)
    assert result == expected

def test_extract_primes_unique_coverage():
    candidates = [["a1"], ["a2"]]
    matrix = [
        [True, False],
        [False, True]
    ]
    covered = [False, False]
    result = extract_primes(candidates, matrix, covered)
    assert sorted(result) == sorted(candidates)
    assert all(covered)

def test_extract_primes_with_overlap():
    candidates = [["a1"], ["a1", "a2"], ["a2"]]
    matrix = [
        [True, False, True],
        [True, False, False],
        [False, True, True]
    ]
    covered = [False, False, False]
    result = extract_primes(candidates, matrix, covered)
    # Depending on heuristic, result could include ["a1", "a2"], but should at least cover all columns
    assert any(set(term) == {"a1", "a2"} for term in result) or len(result) >= 2
    assert all(covered)

def test_minimize_by_table_trivial():
    primes = [["a1", "a2"]]
    targets = [["a1", "a2"]]
    result = minimize_by_table(primes, targets, logic_type="sdnf")
    assert result == targets

def test_minimize_by_table_multiple():
    primes = [["a1"], ["a2"], ["a1", "a2"]]
    targets = [["a1", "a2"], ["a1", "!a2"], ["a2"]]
    result = minimize_by_table(primes, targets, logic_type="sdnf")
    assert all(any(set(p).issubset(set(t)) for p in result) for t in targets)

@pytest.mark.parametrize("expr,expected", [
    ("a & b", True),
    ("!(a|b)", True),
    ("", False),
    ("a + b", False),  # '+' is invalid
    ("123", False),
    ("ab", True),
    ("~a & b", True),
])
def test_is_valid(expr, expected):
    assert is_valid(expr) == expected

def test_build_cnf():
    table = {
        0: [0, 0, 0],
        1: [0, 1, 1],
        2: [1, 0, 1],
        3: [1, 1, 0],
    }
    order = ["a", "b"]
    expected = "(a|b)&(!a|!b)"
    result = build_cnf(table, order)
    assert result == expected

def test_print_functions(capfd):
    print_dnf([["a", "!b"], ["!a", "b"]])
    out, _ = capfd.readouterr()
    assert "ДНФ: (a&!b)|(!a&b)" in out

    print_cnf([["a", "b"], ["!a", "!b"]])
    out, _ = capfd.readouterr()
    assert "КНФ: (a|b)&(!a|!b)" in out

    print_minimized_dnf([["a", "b"]])
    out, _ = capfd.readouterr()
    assert "Минимизированная ДНФ: (a&b)" in out

    print_minimized_cnf([["a", "!b"]])
    out, _ = capfd.readouterr()
    assert "Минимизированная КНФ: (a|!b)" in out

def test_get_dimensions():
    assert get_dimensions(2) == (2, 2)
    assert get_dimensions(3) == (2, 4)
    assert get_dimensions(4) == (4, 4)
    assert get_dimensions(5) == (2, 2)  # fallback default

def test_reorder_gray():
    seq = [(0,0), (0,1), (1,0), (1,1)]
    gray = reorder_gray(seq)
    # Each consecutive pair differs in exactly one bit
    for i in range(len(gray)-1):
        diff = sum(a != b for a,b in zip(gray[i], gray[i+1]))
        assert diff == 1
    assert set(gray) == set(seq)

def test_compute_index():
    # For inputs (r, c) in binary tuples
    idx = compute_index((0,0), (0,0), 1, 1, 4)
    assert idx == 0
    idx = compute_index((1,0), (1,1), 1, 2, 8)
    assert isinstance(idx, int)
    assert 0 <= idx < 8

def test_analyze_neighbors():
    # Create 4 KarnaughCell objects with same results for neighbors
    cells = [KarnaughCell(1, [0,0]), KarnaughCell(1, [0,1]), KarnaughCell(0, [1,0]), KarnaughCell(1, [1,1])]
    group, updated_cells = analyze_neighbors(0, cells, 2)
    # Group should contain neighbors with same result and not paired yet
    assert group is not None
    # Cells involved in pair should be marked
    assert updated_cells[1].in_pair is True or updated_cells[0].in_pair is True

def test_detect_large_group():
    # Setup a 4-cell block with identical results
    cells = [KarnaughCell(1, [0,0]), KarnaughCell(1, [0,1]), KarnaughCell(1, [1,0]), KarnaughCell(1, [1,1])]
    block, updated_cells = detect_large_group(0, cells, 2)
    assert block is not None
    for i in range(4):
        assert updated_cells[i].in_block is True

def test_build_truth_table():
    table, vars_list = build_truth_table("a&b")
    assert vars_list == ['a','b']
    assert table[0] == [0,0,0]
    assert table[3] == [1,1,1]

def test_karnaugh_cell_init():
    cell1 = KarnaughCell(1, [0, 1])
    assert cell1.result == 1
    assert cell1.inputs == [0, 1]
    assert cell1.in_pair is False
    assert cell1.in_block is False
    assert cell1.mode == "dnf"

    cell0 = KarnaughCell(0, [1, 0])
    assert cell0.mode == "cnf"


def test_mark_cell():
    cell = KarnaughCell(1, [0, 0])
    mark_cell(cell)
    assert cell.in_pair is True


def test_get_dimensions():
    assert get_dimensions(2) == (2, 2)
    assert get_dimensions(3) == (2, 4)
    assert get_dimensions(4) == (4, 4)
    # Любое другое значение — дефолт
    assert get_dimensions(5) == (2, 2)


def test_reorder_gray():
    seq = [(0,0), (0,1), (1,1), (1,0)]
    reordered = reorder_gray(seq)
    # Длина совпадает
    assert len(reordered) == len(seq)
    # Последовательность по Грею — соседние элементы отличаются ровно в одном бите
    for i in range(1, len(reordered)):
        diff = sum(x != y for x,y in zip(reordered[i], reordered[i-1]))
        assert diff == 1


def test_compute_index():
    r = (0, 1)
    c = (1, 0)
    idx = compute_index(r, c, 2, 2, 16)
    assert isinstance(idx, int)
    assert 0 <= idx < 16
    # Проверка верхнего ограничения
    idx2 = compute_index(r, c, 2, 2, 3)
    assert idx2 <= 2


def test_analyze_neighbors_basic():
    # Создаем таблицу из 4 клеток 2x2
    cells = [KarnaughCell(1, [0,0]), KarnaughCell(1, [0,1]), KarnaughCell(0, [1,0]), KarnaughCell(1, [1,1])]
    # Проверяем соседей для клетки с индексом 0
    group, new_cells = analyze_neighbors(0, deepcopy(cells), 2)
    assert group is not None
    # Все элементы группы должны иметь одинаковый результат
    for g in group:
        for inputs in g:
            assert all(isinstance(bit, int) for bit in inputs)

def test_detect_large_group():
    cells = [KarnaughCell(1, [0,0]), KarnaughCell(1, [0,1]), KarnaughCell(1, [1,0]), KarnaughCell(1, [1,1])]
    group, new_cells = detect_large_group(0, deepcopy(cells), 2)
    assert group is not None
    assert all(isinstance(inputs, list) for inputs in group[0])


def test_detect_large_group_no_group():
    cells = [KarnaughCell(1, [0,0]), KarnaughCell(0, [0,1]), KarnaughCell(1, [1,0]), KarnaughCell(0, [1,1])]
    group, _ = detect_large_group(0, deepcopy(cells), 2)
    assert group is None


def test_minimize_group_empty():
    result = minimize_group([], "sdnf", 2)
    assert result == ""


def test_minimize_group_simple():
    group = [[[0,0], [0,1]]]
    res = minimize_group(group, "sdnf", 2)
    assert "(" in res and ")" in res
    # В результат должны входить переменные a1 или a2 в каком-то виде
    assert any(v in res for v in ["a1", "a2", "!a1", "!a2"])


def test_generate_blocks_basic():
    # Создаем клетки, чтобы проверить генерацию блоков
    cells = [KarnaughCell(1, [0,0]), KarnaughCell(1, [0,1]), KarnaughCell(0, [1,0]), KarnaughCell(1, [1,1])]
    res = generate_blocks(deepcopy(cells), 2)
    assert "МДНФ:" in res
    assert "МКНФ:" in res


def test_karnaugh_method_basic():
    results = [1, 1, 0, 1]
    mdnf = "(a1&a2)"
    mcnf = "(!a1|!a2)"
    output = karnaugh_method(results, mdnf, mcnf, 2)
    assert "МДНФ:" in output
    assert "МКНФ:" in output
    assert isinstance(output, str)

def test_infix_to_postfix_simple():
    expr = "a&b"
    result = infix_to_postfix(expr)
    # a b &
    assert result == "ab&"

def test_infix_to_postfix_with_not():
    expr = "!a&b"
    result = infix_to_postfix(expr)
    # a! b &
    assert result == "a!b&"

def test_infix_to_postfix_with_parentheses():
    expr = "(a|b)&c"
    result = infix_to_postfix(expr)
    # a b | c &
    assert result == "ab|c&"

def test_infix_to_postfix_complex():
    expr = "!(a&b)|c"
    result = infix_to_postfix(expr)
    # a b & ! c |
    assert result == "ab&!c|"

def test_infix_to_postfix_unbalanced_parentheses():
    expr = "(a&b"
    with pytest.raises(ValueError, match="Скобка"):
        infix_to_postfix(expr)

def test_infix_to_postfix_invalid_not_position():
    expr = "a!"
    with pytest.raises(ValueError, match="Неправильное расположение оператора отрицания"):
        infix_to_postfix(expr)

def test_infix_to_postfix_invalid_char():
    expr = "a&b$"
    with pytest.raises(ValueError, match="Недопустимый символ"):
        infix_to_postfix(expr)


def test_evaluate_postfix_simple():
    expr = "a&b"
    vars_ = ['a', 'b']
    row = [1, 0]
    val = evaluate_postfix(row, expr, vars_)
    assert val == 0

def test_evaluate_postfix_with_not():
    expr = "!a|b"
    vars_ = ['a', 'b']
    row = [1, 0]
    val = evaluate_postfix(row, expr, vars_)
    # !1|0 = 0|0 = 0
    assert val == 0

def test_evaluate_postfix_implication():
    expr = "a>b"
    vars_ = ['a', 'b']
    row = [1, 0]
    val = evaluate_postfix(row, expr, vars_)
    # 1>0 = 0
    assert val == 0
    row = [0, 0]
    val = evaluate_postfix(row, expr, vars_)
    # 0>0 = 1
    assert val == 1

def test_evaluate_postfix_equivalence():
    expr = "a~b"
    vars_ = ['a', 'b']
    row = [1, 1]
    val = evaluate_postfix(row, expr, vars_)
    assert val == 1
    row = [1, 0]
    val = evaluate_postfix(row, expr, vars_)
    assert val == 0

def test_build_truth_table_basic():
    expr = "a&b"
    table, vars_ = build_truth_table(expr)
    assert vars_ == ['a', 'b']
    # 4 rows for 2 variables
    assert len(table) == 4
    # Проверка значений
    expected = {
        0: [0, 0, 0],
        1: [0, 1, 0],
        2: [1, 0, 0],
        3: [1, 1, 1],
    }
    for k, v in expected.items():
        assert table[k] == v

def test_build_truth_table_with_not_and_or():
    expr = "!(a|b)"
    table, vars_ = build_truth_table(expr)
    assert vars_ == ['a', 'b']
    # Проверка первой и последней строки
    assert table[0] == [0, 0, 1]  # !(0|0) = 1
    assert table[3] == [1, 1, 0]  # !(1|1) = 0

def test_build_truth_table_single_var():
    expr = "!a"
    table, vars_ = build_truth_table(expr)
    assert vars_ == ['a']
    assert len(table) == 2
    assert table[0] == [0, 1]  # !0=1
    assert table[1] == [1, 0]  # !1=0

def test_build_truth_table_empty_vars():
    expr = "1"  # No variables
    # При отсутствии переменных, vars_list пустой, но expr содержит недопустимый символ
    with pytest.raises(ValueError):
        build_truth_table(expr)