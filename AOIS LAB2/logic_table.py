# logic_core/logic_table.py
from constant import *
import re


def generate_truth_table(expression: str, show: bool = True) -> tuple[dict, list]:
    postfix = to_postfix(expression)
    variables = sorted(set(re.findall(r"[a-e]", postfix)))
    if show:
        print_header(variables)

    rows = {}
    binary = ZERO
    for i in range(2 ** len(variables)):
        row = binary[-len(variables):]
        result = evaluate_expression(row, postfix)
        rows[i] = row + [result]
        if show:
            print('  |  '.join(str(bit) for bit in rows[i]))
        binary = binary_add(binary, ONE)

    return rows, variables


def evaluate_expression(values: list[int], postfix: str) -> int:
    env = dict(zip("abcde", values))
    stack = []
    for symbol in postfix:
        if symbol in env:
            stack.append(env[symbol])
        elif symbol == '!':
            x = stack.pop()
            stack.append(0 if x else 1)
        elif symbol == '&':
            b, a = stack.pop(), stack.pop()
            stack.append(1 if a and b else 0)
        elif symbol == '|':
            b, a = stack.pop(), stack.pop()
            stack.append(1 if a or b else 0)
        elif symbol == '>':
            b, a = stack.pop(), stack.pop()
            stack.append(0 if a == 1 and b == 0 else 1)
        elif symbol == '~':
            b, a = stack.pop(), stack.pop()
            stack.append(1 if a == b else 0)
    return stack[0]


def to_postfix(expr: str) -> str:
    precedence = PRIORITY
    ops = []
    out = []
    for ch in expr:
        if ch in "abcde":
            out.append(ch)
        elif ch == '(': ops.append(ch)
        elif ch == ')':
            while ops and ops[-1] != '(':
                out.append(ops.pop())
            ops.pop()
        else:
            while ops and ops[-1] != '(' and precedence_rank(ops[-1]) >= precedence_rank(ch):
                out.append(ops.pop())
            ops.append(ch)
    while ops:
        out.append(ops.pop())
    return ''.join(out)


def precedence_rank(op: str) -> int:
    for level, ops in PRIORITY.items():
        if op in ops:
            return level
    return -1


def binary_add(a: list[int], b: list[int]) -> list[int]:
    res = []
    carry = 0
    for i in reversed(range(len(a))):
        s = a[i] + b[i] + carry
        res.insert(0, s % 2)
        carry = s // 2
    if carry:
        res.insert(0, 1)
    return res


def print_header(vars: list):
    top = '+' + '+'.join(['-----'] * (len(vars) + 1)) + '+'
    labels = '| ' + ' | '.join(vars) + ' | Res |'
    print(top)
    print(labels)
