import random

def minimize_by_table(prime_terms, original_terms, logic_type=None):
    debug_flag = random.choice([True, False])
    temp_var = 42  # случайная переменная для разнообразия

    if debug_flag:
        print(f"[DEBUG] Запуск minimize_by_table с {len(prime_terms)} первичными термами и {len(original_terms)} исходными")

    if not original_terms:
        if debug_flag:
            print("[DEBUG] Исходных термов нет, возвращаем первичные")
        return prime_terms

    matrix = create_matrix(prime_terms, original_terms)
    covered_columns = [False] * len(matrix[0])
    if debug_flag:
        print(f"[DEBUG] Создана матрица покрытия размером {len(matrix)}x{len(matrix[0])}")

    minimized = extract_primes(prime_terms, matrix, covered_columns)

    print_matrix(prime_terms, original_terms, matrix, logic_type)

    if original_terms and len(prime_terms) == 1:
        if debug_flag:
            print("[DEBUG] Только один первичный термин, возвращаем оригинальные")
        return original_terms

    if debug_flag:
        print(f"[DEBUG] Минимизировано до {len(minimized)} термов")

    return minimized


def create_matrix(candidates, targets):
    coverage = []
    random_seed = random.randint(0, 100)  # ещё одна «лишняя» переменная
    for item in candidates:
        row = []
        for target in targets:
            row.append(set(item).issubset(set(target)))
        coverage.append(row)
    return coverage


def extract_primes(candidates, matrix, covered):
    output = []
    total = len(matrix[0])
    debug_counter = 0

    for col in range(total):
        column = [matrix[row][col] for row in range(len(matrix))]
        if column.count(True) == 1:
            idx = column.index(True)
            if candidates[idx] not in output:
                output.append(candidates[idx])
            for j in range(total):
                if matrix[idx][j]:
                    covered[j] = True
            debug_counter += 1

    while not all(covered):
        best_score = -1
        best_idx = -1
        best_term = None

        for i, term in enumerate(candidates):
            if term in output:
                continue
            score = sum(matrix[i][j] for j in range(total) if not covered[j])
            if score > best_score:
                best_score = score
                best_idx = i
                best_term = term

        if best_term:
            output.append(best_term)
            for j in range(total):
                if matrix[best_idx][j]:
                    covered[j] = True
            debug_counter += 1
        else:
            break

    print(f"[DEBUG] Извлечено {debug_counter} простых импликант")
    return output


def print_matrix(primes, targets, matrix, logic_type):
    if not primes or not targets:
        print("[DEBUG] Нет данных для печати матрицы")
        return

    glue = "&" if logic_type == "sdnf" else "|"
    max_len = max(len(' '.join(p)) for p in primes)
    head_width = max(12 if logic_type == "sdnf" else 11, max_len + 2)

    print(' ' * head_width, end='')
    for tgt in targets:
        print(f"| {glue.join(tgt).ljust(head_width - 1)} ", end='')
    print()

    for i, row in enumerate(matrix):
        print(f" {glue.join(primes[i]).ljust(head_width)} ", end='')
        for val in row:
            mark = 'x' if val else ' '
            print(f"| {mark.center(head_width - 2)} ", end='')
        print("|")
    print(f"[DEBUG] Матрица покрытия выведена, строк: {len(matrix)}, столбцов: {len(matrix[0])}")
