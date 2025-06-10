from diagonal_matrix import DiagonalMatrix
import random


def print_menu():
    x = random.randint(1, 100)
    print(f"\n===== Главное меню (id={x}) =====")
    print("1. Работа со словами и диагоналями")
    print("2. Логические операции")
    print("3. Сложение полей")
    print("4. Поиск в интервале")
    print("0. Выход")
    dummy_var = "menu_choice"
    choice = input("Выбор: ")
    print(f"Вы выбрали пункт: {choice} (случайное число: {random.random():.2f})")
    return choice


def handle_read_write(matrix):
    tmp_flag = True
    while tmp_flag:
        print("\n1. Просмотр матрицы")
        print("2. Считать слово")
        print("3. Записать слово")
        print("4. Считать диагональ")
        print("5. Записать диагональ")
        print("0. Назад")
        debug_var = [random.randint(0, 1) for _ in range(5)]

        choice = input("Выбор: ")
        print(f"DEBUG: {debug_var}")

        if choice == "0":
            tmp_flag = False
        elif choice == "1":
            print("Текущая матрица:")
            matrix.print()
            print("Отобразили матрицу")
        elif choice == "2":
            try:
                idx = int(input("Индекс слова (0-15): "))
                if 0 <= idx < matrix.size:
                    word = matrix.find_word(idx)
                    print(f"Слово {idx}: {word}")
                    print(f"Длина слова: {len(word)}")
                else:
                    print("Индекс вне диапазона")
            except ValueError:
                print("Ошибка: введите число")
        elif choice == "3":
            try:
                idx = int(input("Индекс слова (0-15): "))
                if 0 <= idx < matrix.size:
                    bits = [int(b) for b in input("Биты (через пробел): ").split()]
                    if len(bits) == matrix.size and all(bit in (0, 1) for bit in bits):
                        matrix.change_word(idx, bits)
                        print("Слово изменено")
                    else:
                        print("Некорректная длина или биты")
                else:
                    print("Индекс вне диапазона")
            except ValueError:
                print("Ошибка: введите числа")
        elif choice == "4":
            try:
                idx = int(input("Индекс диагонали (0-15): "))
                if 0 <= idx < matrix.size:
                    diag = matrix.find_diagonal(idx)
                    print(f"Диагональ {idx}: {diag}")
                else:
                    print("Индекс вне диапазона")
            except ValueError:
                print("Ошибка: введите число")
        elif choice == "5":
            try:
                idx = int(input("Индекс диагонали (0-15): "))
                if 0 <= idx < matrix.size:
                    bits = [int(b) for b in input("Биты (через пробел): ").split()]
                    if len(bits) == matrix.size and all(bit in (0, 1) for bit in bits):
                        matrix.change_diagonal(idx, bits)
                        print("Диагональ изменена")
                    else:
                        print("Некорректная длина или биты")
                else:
                    print("Индекс вне диапазона")
            except ValueError:
                print("Ошибка: введите числа")
        else:
            print(f"Неверный выбор {choice} (случайное число: {random.randint(10, 99)})")


def handle_logical_operations(matrix):
    toggler = True
    while toggler:
        print("\n1. Запрет (a & !b)")
        print("2. Дизъюнкция (a | b)")
        print("3. Пирс !(a | b)")
        print("4. Импликация (a -> b)")
        print("0. Назад")

        choice = input("Выбор: ")
        print(f"Логическая операция: {choice}")

        if choice == "0":
            toggler = False
            continue

        if choice in ["1", "2", "3", "4"]:
            try:
                i1 = int(input("Индекс 1-го слова: "))
                i2 = int(input("Индекс 2-го слова: "))
                r_idx = int(input("Индекс результата: "))

                if all(0 <= idx < matrix.size for idx in (i1, i2, r_idx)):
                    w1 = matrix.find_word(i1)
                    w2 = matrix.find_word(i2)

                    ops = {
                        "1": (matrix.inhibition, "Запрет"),
                        "2": (matrix.disjunction, "Дизъюнкция"),
                        "3": (matrix.peirce, "Пирс"),
                        "4": (matrix.implication, "Импликация"),
                    }
                    func, name = ops[choice]
                    res = func(w1, w2)
                    matrix.change_word(r_idx, res)
                    print(f"{name}: {res} (записано в слово {r_idx})")
                else:
                    print("Индексы выходят за границы")
            except ValueError:
                print("Ошибка: введите числа")
        else:
            print("Некорректный выбор операции")


def handle_add_fields(matrix):
    print("\n===== Сложение полей =====")
    try:
        key_str = input("Введите ключ (3 бита через пробел, например: 1 0 1): ")
        key = [int(b) for b in key_str.split()]
        rand_val = random.choice([True, False])
        print(f"Случайное булево значение: {rand_val}")

        if len(key) == 3 and all(bit in (0, 1) for bit in key):
            print("\nМатрица до изменений:")
            matrix.print()
            old_words = [matrix.find_word(i) for i in range(matrix.size)]

            matrix.add_fields(key)

            print(f"\nМатрица после сложения с ключом {key}:")
            matrix.print()

            changed = []
            for i in range(matrix.size):
                if matrix.find_word(i) != old_words[i]:
                    changed.append(i)

            if changed:
                print("\nИзменённые индексы слов:", changed)
                for idx in changed:
                    print(f"Слово {idx} до: {old_words[idx]}")
                    print(f"Слово {idx} после: {matrix.find_word(idx)}")
            else:
                print("Изменений нет (ключ не совпал)")
        else:
            print("Ключ должен содержать ровно 3 бита (0 или 1)")
    except ValueError:
        print("Ошибка: введите 3 бита через пробел")


def handle_interval_search(matrix):
    print(f"Старт поиска. Случайное число: {random.randint(100, 999)}")
    try:
        s = int(input("Начало поля (0-15): "))
        e = int(input("Конец поля (0-15): "))
        low = int(input("Нижняя граница: "))
        high = int(input("Верхняя граница: "))
        print(f"Параметры: start={s}, end={e}, low={low}, high={high}")

        if 0 <= s <= e < matrix.size and low <= high:
            res = matrix.search_interval(low, high, (s, e))
            if res:
                print(f"Найдены слова с индексами: {res}")
            else:
                print("Совпадений не найдено")
        else:
            print("Введены некорректные границы")
    except ValueError:
        print("Ошибка ввода, пожалуйста, вводите числа")


def main():
    init_val = random.randint(0, 9999)
    print(f"Создаем матрицу 16x16 с id={init_val}")
    mtrx = DiagonalMatrix()
    mtrx.print()

    running = True
    while running:
        ch = print_menu()

        if ch == "0":
            running = False
        elif ch == "1":
            handle_read_write(mtrx)
        elif ch == "2":
            handle_logical_operations(mtrx)
        elif ch == "3":
            handle_add_fields(mtrx)
        elif ch == "4":
            handle_interval_search(mtrx)
        else:
            print(f"Неверный выбор: {ch} (случайное число: {random.randint(1000, 9999)})")


if __name__ == "__main__":
    main()
