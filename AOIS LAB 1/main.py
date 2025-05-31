from BinaryConverter import BinaryConverter
from BinaryArithmetics import BinaryArithmetic
from BinaryMultiplier import BinaryMultiplier
from BinaryDivider import BinaryDivider


def print_menu():
    print("1. Преобразование в бинарные коды")
    print("2. Сложение (доп. код)")
    print("3. Вычитание (через доп. код)")
    print("4. Умножение (прямой код)")
    print("5. Деление (прямой код)")
    print("6. Float в IEEE-754 (32-bit)")
    print("7. Сложение float (32-bit)")

def main():
    conv = BinaryConverter()
    adder = BinaryArithmetic(conv)
    multiplier = BinaryMultiplier(conv, adder)
    divider = BinaryDivider(conv, adder)

    while True:
        print_menu()
        choice = input("Выбор: ").strip()

        if choice == "1":
            num = int(input("Введите число: "))
            print("Прямой: ", conv.to_direct_code(num))
            print("Обратный: ", conv.to_inverse_code(num))
            print("Дополнительный: ", conv.to_complement_code(num))

        elif choice == "2":
            a = int(input("A: "))
            b = int(input("B: "))
            a_bin = conv.to_complement_code(a)
            b_bin = conv.to_complement_code(b)
            res = adder.sum_complement(a_bin, b_bin)
            print("Бинарный результат: ", res)
            print("Десятичный: ", conv.to_decimal(res))

        elif choice == "3":
            a = int(input("A: "))
            b = int(input("B: "))
            a_bin = conv.to_complement_code(a)
            b_bin = conv.to_complement_code(-b)
            res = adder.sum_complement(a_bin, b_bin)
            print("Бинарный результат: ", res)
            print("Десятичный: ", conv.to_decimal(res))

        elif choice == "4":
            a = int(input("A: "))
            b = int(input("B: "))
            a_code = conv.to_direct_code(a)
            b_code = conv.to_direct_code(b)
            res = multiplier.multiply(a_code, b_code)
            print("Бинарный результат: ", res)
            print("Десятичный: ", conv.to_decimal(str(res)))

        elif choice == "5":
            a = int(input("A: "))
            b = int(input("B: "))
            a_code = conv.to_direct_code(a)
            b_code = conv.to_direct_code(b)
            res = divider.divide(a_code, b_code)
            print("Бинарный результат: ", res)
            print("Десятичный: ", conv.to_decimal(str(res)))

        elif choice == "6":
            num = float(input("Введите float: "))
            print("32-bit код: ", conv.float_to_bin32(num))

        elif choice == "7":
            f1 = float(input("Float A: "))
            f2 = float(input("Float B: "))
            b1 = conv.float_to_bin32(f1)
            b2 = conv.float_to_bin32(f2)
            res = adder.float_sum_32bit(b1, b2)
            print("Бинарный результат: ", res)
            print("Десятичный: ", conv.bin32_to_float(res))

if __name__ == '__main__':
    main()
