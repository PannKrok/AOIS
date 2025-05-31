from CONST import *
from math import frexp, ldexp


class BinaryConverter:
    def __init__(self):
        self.bit_width = BIT_SIZE

    def to_bin_string(self, number: int) -> str:
        if number == 0:
            return "0" * (self.bit_width - 1)

        abs_val = abs(number)
        bits = ""
        while abs_val:
            bits = str(abs_val % 2) + bits
            abs_val //= 2

        return bits.zfill(self.bit_width - 1)

    def to_decimal(self, binary: str) -> int:
        if binary[0] == '0':
            return int(binary[1:], 2)
        value = int(binary[1:], 2)
        return -value

    def to_direct_code(self, val: int) -> str:
        prefix = '0' if val >= 0 else '1'
        return prefix + self.to_bin_string(val)

    def to_inverse_code(self, val: int) -> str:
        main = self.to_bin_string(val)
        if val >= 0:
            return '0' + main

        flipped = ''.join(['1' if c == '0' else '0' for c in main])
        return '1' + flipped

    def to_complement_code(self, val: int) -> str:
        if val >= 0:
            return '0' + self.to_bin_string(val)

        inv = list(self.to_inverse_code(val))
        for idx in range(len(inv) - 1, -1, -1):
            if inv[idx] == '0':
                inv[idx] = '1'
                break
            elif inv[idx] == '1':
                inv[idx] = '0'
        return ''.join(inv)

    def float_to_bin32(self, value: float) -> str:
        sign_bit = '0' if value >= 0 else '1'
        value = abs(value)

        if value == 0:
            return '0' * 32
        if value == float('inf'):
            return sign_bit + '1'*8 + '0'*23

        int_part = int(value)
        frac_part = value - int_part

        int_bin = ''
        while int_part:
            int_bin = str(int_part % 2) + int_bin
            int_part //= 2

        frac_bin = ''
        while len(frac_bin) < 23:
            frac_part *= 2
            frac_bin += str(int(frac_part))
            frac_part -= int(frac_part)

        exponent_val = len(int_bin) - 1
        exponent_encoded = exponent_val + 127
        exponent_bin = bin(exponent_encoded)[2:].zfill(8)

        mantissa = (int_bin[1:] + frac_bin)[:23]
        return sign_bit + exponent_bin + mantissa

    def bin32_to_float(self, bitstr: str) -> float:
        s = int(bitstr[0])
        exp = int(bitstr[1:9], 2) - 127
        mantissa_bits = '1' + bitstr[9:]

        mantissa_val = sum(int(bit) * 2**-i for i, bit in enumerate(mantissa_bits))
        result = mantissa_val * (2 ** exp)

        return -result if s == 1 else result



