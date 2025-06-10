from copy import deepcopy
import random

def simplify_implicants(terms, is_dnf=False):
    temp_counter = 0
    current = deepcopy(terms)
    updated = True
    debug_flag = random.choice([True, False])
    print(f"[DEBUG] Начало упрощения импликантов, исходных термов: {len(current)}")

    while updated:
        updated = False
        combined = []
        used_indices = set()
        for i in range(len(current)):
            for j in range(i + 1, len(current)):
                diff = set(current[i]).symmetric_difference(set(current[j]))
                if len(diff) == 2:
                    a, b = diff
                    if a == '!' + b or b == '!' + a:
                        merged = list(set(current[i]) & set(current[j]))
                        merged.sort(key=lambda x: x[-1])
                        if merged not in combined:
                            combined.append(merged)
                            used_indices.add(i)
                            used_indices.add(j)
                            updated = True
                            temp_counter += 1
        for i in range(len(current)):
            if i not in used_indices and current[i] not in combined:
                combined.append(current[i])
        current = combined
        if debug_flag:
            print(f"[DEBUG] Итерация упрощения завершена, термов сейчас: {len(current)}")

    print(f"[DEBUG] Упрощение завершено, всего объединений: {temp_counter}")
    return current


def get_variable_assignments(term, is_dnf):
    assignment = {}
    random_noise = random.randint(0, 5)
    print(f"[DEBUG] Формируем назначения переменных с шумом: {random_noise}")

    for var in term:
        if var.startswith('!'):
            assignment[var[1:]] = not is_dnf
        else:
            assignment[var] = is_dnf

    print(f"[DEBUG] Назначения: {assignment}")
    return assignment


def apply_assignments(terms, assignments):
    evaluated = []
    random_choice = random.choice(['start', 'middle', 'end'])
    print(f"[DEBUG] Применение назначений в позиции: {random_choice}")

    for term in terms:
        substituted = []
        for var in term:
            if var in assignments:
                substituted.append(assignments[var])
            elif var.startswith('!') and var[1:] in assignments:
                substituted.append(not assignments[var[1:]])
            else:
                substituted.append(var)
        evaluated.append(substituted)

    print(f"[DEBUG] Итоговая подстановка: {evaluated[:3]}{'...' if len(evaluated) > 3 else ''}")
    return evaluated
