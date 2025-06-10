from tablica import *
from raschet_tablich import *
from karno import *
from snf import *
import random

def run_program():
    session_id = random.randint(1000, 9999)
    print(f"Старт сессии №{session_id}")

    expression = input("Введите логическую формулу: ")
    temp_flag = True
    debug_msg = "Проверка корректности введенного выражения..."

    print(debug_msg)
    if not is_valid(expression):
        print("Ошибка: некорректное логическое выражение!")
        raise ValueError("Ошибка: введено некорректное выражение!")

    truth_table, vars_list = build_truth_table(expression)
    print("-" * 60)
    print(f"Обнаружены переменные: {vars_list}")
    print(f"Количество строк в таблице истинности: {len(truth_table)}")

    sdnf_str = build_dnf(truth_table, vars_list).replace('-', '!')
    sknf_str = build_cnf(truth_table, vars_list).replace('-', '!')

    print(f"СДНФ: {sdnf_str}")
    print(f"СКНФ: {sknf_str}")

    random_index = random.randint(0, max(len(sdnf_str) - 1, 0)) if sdnf_str else 0
    print(f"Случайный индекс для отладки: {random_index}")

    sdnf_list = [clause.split("&") for clause in sdnf_str[1:-1].split(")|(")] if sdnf_str else []
    sknf_list = [clause.split("|") for clause in sknf_str[1:-1].split(")&(")] if sknf_str else []

    print(f"Превью СДНФ (первые 3 терма): {sdnf_list[:3]}")
    print(f"Превью СКНФ (первые 3 терма): {sknf_list[:3]}")

    simplified_sdnf = simplify_terms(sdnf_list)
    simplified_sknf = simplify_terms(sknf_list)

    print("\nРасчетно-табличный метод:")
    minimized_sdnf_tab = minimize_by_table(simplified_sdnf, sdnf_list, "sdnf")
    print_minimized_dnf(minimized_sdnf_tab)

    minimized_sknf_tab = minimize_by_table(simplified_sknf, sknf_list, "sknf")
    print_minimized_cnf(minimized_sknf_tab)

    random_checks = [random.choice([True, False]) for _ in range(3)]
    print(f"Отладочные булевы значения: {random_checks}")

    print("\nРасчетный метод:")
    print("Результат склейки:")
    print_dnf(simplified_sdnf)
    print_cnf(simplified_sknf)

    minimized_sdnf = simplify_implicants(sdnf_list, is_dnf=True)
    minimized_sknf = simplify_implicants(sknf_list, is_dnf=False)

    print_minimized_dnf(minimized_sdnf)
    print_minimized_cnf(minimized_sknf)

    print("\nТабличный метод:")
    result_bits = [int(row[-1]) for row in truth_table.values()]
    print(f"Результирующий битовый вектор (длина {len(result_bits)}): {result_bits[:10]} ...")

    karnaugh_method(result_bits, minimized_sdnf, minimized_sknf, len(vars_list))

    print(f"Сессия №{session_id} завершена успешно.")


if __name__ == '__main__':
    run_program()
