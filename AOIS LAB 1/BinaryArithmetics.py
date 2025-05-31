from typing import List
from BinaryConverter import BinaryConverter
from CONST import *

class BinaryArithmetic:
    def __init__(self, converter: BinaryConverter):
        self.conv = converter

    def _sum_bits(self, bin1: list[str], bin2: list[str]) -> list[str]:
        carry = 0
        result = []
        for i in reversed(range(len(bin1))):
            total = int(bin1[i]) + int(bin2[i]) + carry
            result.insert(0, str(total % 2))
            carry = total // 2

        if carry:
            result.insert(0, '1')
        return result

    def sum_direct(self, a: str, b: str) -> str:
        return ''.join(self._sum_bits(list(a), list(b)))

    def sum_inverse(self, a: str, b: str) -> str:
        temp = self._sum_bits(list(a), list(b))

        if len(temp) > BIT_SIZE:
            temp.pop(0)
            temp = self._sum_bits(temp, BINARY_ONE)

        if temp[0] == '1':
            for i in range(1, len(temp)):
                temp[i] = '1' if temp[i] == '0' else '0'

        return ''.join(temp)

    def sum_complement(self, a: str, b: str) -> str:
        res = self._sum_bits(list(a), list(b))

        if len(res) > BIT_SIZE:
            res.pop(0)

        if res[0] == '1':
            for i in range(1, len(res)):
                res[i] = '1' if res[i] == '0' else '0'
            for i in reversed(range(len(res))):
                if res[i] == '0':
                    res[i] = '1'
                    break
                elif res[i] == '1':
                    res[i] = '0'

        return ''.join(res)

    def float_sum_32bit(self, a: str, b: str) -> str:
        assert len(a) == 32 and len(b) == 32, "Both inputs must be 32-bit binary strings"
        if int(a, 2) == 0 and int(b, 2) == 0:
            return "0" * 32

        # Распаковка
        sign_a, sign_b = int(a[0]), int(b[0])
        exp_a, exp_b = int(a[1:9], 2), int(b[1:9], 2)
        mant_a, mant_b = int(a[9:], 2), int(b[9:], 2)

        # Добавление скрытого бита
        mant_a |= 1 << 23
        mant_b |= 1 << 23

        # Применяем знак
        if sign_a: mant_a = -mant_a
        if sign_b: mant_b = -mant_b

        # Выравнивание по экспоненте
        shift = exp_a - exp_b
        if shift > 0:
            mant_b >>= shift
            exp = exp_a
        else:
            mant_a >>= -shift
            exp = exp_b

        # Сложение
        mant_sum = mant_a + mant_b
        result_sign = 0 if mant_sum >= 0 else 1
        mant_sum = abs(mant_sum)

        # Нормализация
        if mant_sum == 0:
            return "0" * 32  # ноль

        while mant_sum >= (1 << 24):
            mant_sum >>= 1
            exp += 1

        while mant_sum < (1 << 23):
            mant_sum <<= 1
            exp -= 1

        # Удаление скрытого бита и упаковка
        mantissa = mant_sum & ((1 << 23) - 1)
        exponent = exp

        # Защита от переполнения и underflow
        if exponent >= 255:
            return str(result_sign) + '1' * 8 + '0' * 23  # inf
        if exponent <= 0:
            return str(result_sign) + '0' * 8 + '0' * 23  # поднорм. или 0

        return f"{result_sign}{format(exponent, '08b')}{format(mantissa, '023b')}"