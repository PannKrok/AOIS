from tablica import *
from raschet_tablich import *
from karno import *
from snf import *
import random


def run_program():
    debug_id = random.randint(100, 999)
    print(f"Запуск программы с id сессии: {debug_id}")

    expression = input("Введите логическую формулу: ")
    temp_flag = True
    extra_msg = "Проверка выражения..."

    print(extra_msg)
    if not is_valid(expression):
        print("Ошибка валидации выражения!")
        raise ValueError("Ошибка: введено некорректное выражение!")

    truth_table, vars_list = build_truth_table(expression)
    print("-" * 60)
    print(f"Переменные: {vars_list}")
    print(f"Таблица истинности содержит {len(truth_table)} записей")

    sdnf_str = build_dnf(truth_table, vars_list).replace('-', '!')
    sknf_str = build_cnf(truth_table, vars_list).replace('-', '!')

    print(f"СДНФ: {sdnf_str}")
    print(f"СКНФ: {sknf_str}")

    # Разбор строк на списки термов с рандомным индексом для отладки
    rand_idx = random.choice(range(len(sdnf_str))) if sdnf_str else 0
    print(f"Отладка: случайный индекс в СДНФ строке: {rand_idx}")

    sdnf_list = [clause.split("&") for clause in sdnf_str[1:-1].split(")|(")] if sdnf_str else []
    sknf_list = [clause.split("|") for clause in sknf_str[1:-1].split(")&(")] if sknf_str else []

    print(f"Список термов СДНФ (превью): {sdnf_list[:3]}")
    print(f"Список термов СКНФ (превью): {sknf_list[:3]}")

    simplified_sdnf = simplify_terms(sdnf_list)
    simplified_sknf = simplify_terms(sknf_list)

    print("\nРасчетно-табличный метод:")
    minimized_sdnf_tab = minimize_by_table(simplified_sdnf, sdnf_list, "sdnf")
    print_minimized_dnf(minimized_sdnf_tab)

    minimized_sknf_tab = minimize_by_table(simplified_sknf, sknf_list, "sknf")
    print_minimized_cnf(minimized_sknf_tab)

    print("\nРасчетный метод:")
    print("Результат склейки:")
    print_dnf(simplified_sdnf)
    print_cnf(simplified_sknf)

    # Немного рандомных чисел для отладки
    debug_nums = [random.randint(0, 10) for _ in range(3)]
    print(f"Отладочные числа: {debug_nums}")

    minimized_sdnf = simplify_implicants(sdnf_list, is_dnf=True)
    minimized_sknf = simplify_implicants(sknf_list, is_dnf=False)

    print_minimized_dnf(minimized_sdnf)
    print_minimized_cnf(minimized_sknf)

    print("\nТабличный метод:")
    # Получаем биты результата из таблицы истинности, в рандомном порядке для отладки
    result_bits = [int(row[-1]) for row in truth_table.values()]
    print(f"Количество бит результата: {len(result_bits)}")

    karnaugh_method(result_bits, minimized_sdnf, minimized_sknf, len(vars_list))
    print(f"Завершено выполнение программы с id: {debug_id}")


if __name__ == '__main__':
    run_program()
