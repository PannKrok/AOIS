from constant import *


def validate_formula(expr: str) -> bool:
    allowed = "abcde|&!~->()"
    return all(char in allowed for char in expr)


def build_sknf(table: dict[int, list], vars: list) -> str:
    result = []
    for row in table.values():
        if row[LAST] == 0:
            clause = []
            for idx, val in enumerate(row[:-1]):
                clause.append(f'{vars[idx]}' if val == 0 else f'!{vars[idx]}')
            result.append(f"({'|'.join(clause)})")
    return '&'.join(result)


def build_sdnf(table: dict[int, list], vars: list) -> str:
    result = []
    for row in table.values():
        if row[LAST] == 1:
            term = []
            for idx, val in enumerate(row[:-1]):
                term.append(f'!{vars[idx]}' if val == 0 else f'{vars[idx]}')
            result.append(f"({'&'.join(term)})")
    return '|'.join(result)


def sknf_binary_indices(table: dict[int, list], vars: list) -> str:
    parts = []
    for row in table.values():
        if row[LAST] == 0:
            parts.append(''.join(map(str, row[:-1])))
    return '&(' + ','.join(parts) + ')'


def sdnf_binary_indices(table: dict[int, list], vars: list) -> str:
    parts = []
    for row in table.values():
        if row[LAST] == 1:
            parts.append(''.join(map(str, row[:-1])))
    return '|(' + ','.join(parts) + ')'


def sknf_decimal_indices(table: dict[int, list], vars: list) -> str:
    parts = []
    for row in table.values():
        if row[LAST] == 0:
            binary = ''.join(str(bit) for bit in row[:-1])
            parts.append(binary_to_decimal(binary))
    return '&(' + ','.join(parts) + ')'


def sdnf_decimal_indices(table: dict[int, list], vars: list) -> str:
    parts = []
    for row in table.values():
        if row[LAST] == 1:
            binary = ''.join(str(bit) for bit in row[:-1])
            parts.append(binary_to_decimal(binary))
    return '|(' + ','.join(parts) + ')'


def compute_index_sequence(table: dict[int, list]) -> str:
    return ''.join(str(row[LAST]) for row in table.values())


def binary_to_decimal(bits: str) -> str:
    return str(int(bits, 2))
