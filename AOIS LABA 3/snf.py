from typing import Dict, List
from priority import *
import re

def is_valid(expr: str) -> bool:
    permitted = set("abcde|!&()>~")
    expr = expr.replace(" ", "")
    if not expr:
        print("[DEBUG] Пустое выражение")
        return False
    if not all(ch in permitted for ch in expr):
        print("[DEBUG] Найдены запрещённые символы в выражении")
        return False
    has_var = bool(re.search(r"[a-e]", expr))
    print(f"[DEBUG] Проверка наличия переменных в выражении: {has_var}")
    return has_var


def build_cnf(table: Dict[int, List[int]], order: List[str]) -> str:
    parts = []
    debug_counter = 0
    for values in table.values():
        if values[LAST] == 0:
            clause = []
            for idx, bit in enumerate(values[:-1]):
                literal = order[idx] if bit == 0 else f"!{order[idx]}"
                clause.append(literal)
            parts.append(f"({'|'.join(clause)})")
            debug_counter += 1
    print(f"[DEBUG] Построено КНФ из {debug_counter} дизъюнктов")
    return '&'.join(parts)


def build_dnf(table: Dict[int, List[int]], order: List[str]) -> str:
    components = []
    count = 0
    for values in table.values():
        if values[LAST] == 1:
            group = []
            for idx, bit in enumerate(values[:-1]):
                literal = f"!{order[idx]}" if bit == 0 else order[idx]
                group.append(literal)
            components.append(f"({'&'.join(group)})")
            count += 1
    print(f"[DEBUG] Построено ДНФ из {count} конъюнктов")
    return '|'.join(components)


def simplify_terms(groups: List[List[str]]) -> List[List[str]]:
    if len(groups) <= 1:
        print("[DEBUG] Нет или один набор для упрощения, возвращаем как есть")
        return groups
    reduced = []
    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            shared = sorted(set(groups[i]) & set(groups[j]), key=lambda x: x[-1])
            if len(shared) == len(groups[i]) - 1 and shared not in reduced:
                reduced.append(shared)
    print(f"[DEBUG] Упрощено количество групп с {len(groups)} до {len(reduced)}")
    return reduced


def print_dnf(terms: List[List[str]]):
    if not terms:
        print("ДНФ: ")
        return
    expr = '|'.join(f"({'&'.join(term)})" for term in terms)
    print(f"ДНФ: {expr}")


def print_cnf(clauses: List[List[str]]):
    if not clauses:
        print("КНФ: ")
        return
    expr = '&'.join(f"({'|'.join(clause)})" for clause in clauses)
    print(f"КНФ: {expr}")


def print_minimized_dnf(minimized: List[List[str]]):
    if not minimized:
        print("Минимизированная ДНФ: ")
        return
    expr = '|'.join(f"({'&'.join(term)})" for term in minimized)
    print(f"Минимизированная ДНФ: {expr}")


def print_minimized_cnf(minimized: List[List[str]]):
    if not minimized:
        print("Минимизированная КНФ: ")
        return
    expr = '&'.join(f"({'|'.join(clause)})" for clause in minimized)
    print(f"Минимизированная КНФ: {expr}")
