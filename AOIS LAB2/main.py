from logic_utils import *
from logic_table import *

def launch():
    formula = input("Введите логическую формулу: ")

    if not validate_formula(formula):
        raise Exception("Ошибка: недопустимые символы во входной строке.")

    table, vars_used = generate_truth_table(formula)

    print("=" * 60)

    print(f'СКНФ: {build_sknf(table, vars_used)}')
    print(f'СДНФ: {build_sdnf(table, vars_used)}')

    print("=" * 60)

    print(f'СКНФ (бинарный): {sknf_binary_indices(table, vars_used)}')
    print(f'СКНФ (десятичный): {sknf_decimal_indices(table, vars_used)}')

    print("=" * 60)

    print(f'СДНФ (бинарный): {sdnf_binary_indices(table, vars_used)}')
    print(f'СДНФ (десятичный): {sdnf_decimal_indices(table, vars_used)}')

    print("=" * 60)
    idx = compute_index_sequence(table)
    print(f'Индекс (бинарный): {idx}')
    print(f'Индекс (десятичный): {binary_to_decimal(idx)}')


if __name__ == "__main__":
    launch()
