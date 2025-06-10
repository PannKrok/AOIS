from priority import PRIORITY, OPS

def infix_to_postfix(expression: str) -> str:
    output = []
    stack = []
    pos = 0

    while pos < len(expression):
        char = expression[pos]

        if char.isalpha():
            output.append(char)
            pos += 1
        elif char == '!':
            # Проверяем следующий символ — должен быть переменной или скобкой
            if pos + 1 < len(expression) and (expression[pos + 1].isalpha() or expression[pos + 1] == '('):
                stack.append(char)
            else:
                raise ValueError("Неправильное расположение оператора отрицания '!'")
            pos += 1
        elif char in OPS:
            # Пока на стеке оператор с большим или равным приоритетом — выталкиваем в output
            while stack and stack[-1] != '(' and PRIORITY.get(stack[-1], 0) >= PRIORITY.get(char, 0):
                output.append(stack.pop())
            stack.append(char)
            pos += 1
        elif char == '(':
            stack.append(char)
            pos += 1
        elif char == ')':
            # Вынимаем из стека до '('
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack and stack[-1] == '(':
                stack.pop()
            else:
                raise ValueError("Несогласованные скобки: отсутствует '('")
            # Если после скобки на вершине стека '!' — добавляем его в output (унарный минус)
            if stack and stack[-1] == '!':
                output.append(stack.pop())
            pos += 1
        else:
            raise ValueError(f"Недопустимый символ в выражении: '{char}'")

    # Выталкиваем оставшиеся операторы из стека
    while stack:
        if stack[-1] == '(':
            raise ValueError("Скобка '(' не была закрыта")
        output.append(stack.pop())

    return ''.join(output)


def evaluate_postfix(row: list[int], expr: str, variables: list[str]) -> int:
    postfix_expr = infix_to_postfix(expr)
    calc_stack = []

    for token in postfix_expr:
        if token.isalpha():
            idx = variables.index(token)
            calc_stack.append(row[idx])
        elif token == '!':
            if not calc_stack:
                raise ValueError("Ошибка: недостаточно операндов для оператора НЕ '!'")
            val = calc_stack.pop()
            calc_stack.append(1 - val)
        elif token in OPS:
            if len(calc_stack) < 2:
                raise ValueError(f"Ошибка: недостаточно операндов для оператора '{token}'")
            right_val = calc_stack.pop()
            left_val = calc_stack.pop()

            if token == '&':
                calc_stack.append(left_val & right_val)
            elif token == '|':
                calc_stack.append(left_val | right_val)
            elif token == '>':
                calc_stack.append(int(not left_val or right_val))
            elif token == '~':
                calc_stack.append(int(left_val == right_val))
            else:
                raise ValueError(f"Неизвестный оператор '{token}'")
        else:
            raise ValueError(f"Недопустимый символ в постфиксном выражении: '{token}'")

    if len(calc_stack) != 1:
        raise ValueError("Ошибка вычисления: после обработки остались лишние операнды")

    return calc_stack[0]


def build_truth_table(expression: str) -> tuple[dict[int, list[int]], list[str]]:
    vars_list = sorted({c for c in expression if c.isalpha()})
    n_vars = len(vars_list)
    truth_table = {}

    for num in range(2 ** n_vars):
        bits = [(num >> (n_vars - 1 - i)) & 1 for i in range(n_vars)]
        val = evaluate_postfix(bits, expression, vars_list)
        truth_table[num] = bits + [val]

    print(f"[DEBUG] Построена таблица истинности для {n_vars} переменных с {2**n_vars} строками")
    return truth_table, vars_list
