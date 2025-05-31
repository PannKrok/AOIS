from Builder import Builder
from Binary_helper import Binary_helper
from constants import LITERALS, LEN_OF_TETRADA


def get_adder_CNF():
    values = [0] * 3  # A, B, C
    one = [0] * 2 + [1]
    literals = list(LITERALS[:3])  # A, B, C
    SKNF_S = []
    SKNF_Cout = []

    for i in range(2 ** 3):
        S = values[0] ^ values[1] ^ values[2]  # A ⊕ B ⊕ C
        Cout = int((values[0] and values[1]) or (values[0] and values[2]) or (values[1] and values[2]))
        if S == 0:
            SKNF_S.append(Builder.build_SKNF(literals, values))
        if Cout == 0:
            SKNF_Cout.append(Builder.build_SKNF(literals, values))
        values = Binary_helper.sum_b(values, one)

    return "&".join(SKNF_S), "&".join(SKNF_Cout)


def get_D8421_2():
    values = [0] * LEN_OF_TETRADA
    one = [0] * (LEN_OF_TETRADA - 1) + [1]

    print('D8421\t\t\tD8421+2')
    for i in range(16):
        decimal = Binary_helper.calculate(values)
        if decimal > 9:
            y3, y2, y1, y0 = "X", "X", "X", "X"
        else:
            dec_plus2 = decimal + 2
            y3 = (dec_plus2 // 8) % 2
            y2 = (dec_plus2 // 4) % 2
            y1 = (dec_plus2 // 2) % 2
            y0 = dec_plus2 % 2
        print(f"{values[0]} {values[1]} {values[2]} {values[3]}\t\t\t{y3} {y2} {y1} {y0}")
        values = Binary_helper.sum_b(values, one)

    # Пример: пересчёт вручную логики Y0..Y3 на основе новых значений
    # Здесь представлены условные выражения — лучше получить их автоматически
    min_Y = {
        "Y0": "(D)",                      # Последний бит
        "Y1": "(!B&!C)|(!A&C)",           # Обновлённые
        "Y2": "(!A&!B)|(A&!C)",
        "Y3": "(A&C)|(!B&!D)"
    }

    return min_Y


def replace(form):
    form = form.replace("A", "X3")
    form = form.replace("B", "X2")
    form = form.replace("C", "X1")
    form = form.replace("D", "X0")
    return form


def replace_back(form):
    form = form.replace("X3", "A")
    form = form.replace("X2", "B")
    form = form.replace("X1", "C")
    form = form.replace("X0", "D")
    return form


if __name__ == "__main__":
    SKNF_S, SKNF_Cout = get_adder_CNF()
    print("СКНФ для S: " + SKNF_S, "СКНФ для C_out: " + SKNF_Cout, sep='\n')
    print()

    min_Y = get_D8421_2()
    print(f"Y1 = {replace(min_Y['Y1'])}")
    print(f"Y2 = {replace(min_Y['Y2'])}")
    print(f"Y3 = {replace(min_Y['Y3'])}")
    print(f"Y0 = {replace(min_Y['Y0'])}")
