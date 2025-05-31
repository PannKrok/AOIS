from BinaryArithmetics import BinaryArithmetic
from BinaryConverter import BinaryConverter
from CONST import BINARY_ZERO, ONE_ADDITION

class BinaryMultiplier:
    def __init__(self, conv: BinaryConverter, adder: BinaryArithmetic):
        self.conv = conv
        self.adder = adder

    def multiply(self, multiplicand: str, multiplier: str) -> str:
        result = BINARY_ZERO[:]
        same_sign = multiplicand[0] == multiplier[0]

        if multiplier[0] == '1':
            multiplier = '0' + multiplier[1:]

        while multiplier != ''.join(BINARY_ZERO):
            a_val = self.conv.to_decimal(multiplicand)
            r_val = self.conv.to_decimal("".join(result))

            addend_a = self.conv.to_complement_code(a_val)
            addend_r = self.conv.to_complement_code(r_val)

            result = self.adder.sum_complement(addend_a, addend_r)
            decrement = self.adder.sum_complement(
                self.conv.to_complement_code(
                    self.conv.to_decimal(multiplier)
                ),
                ''.join(ONE_ADDITION)
            )
            multiplier = decrement

        if all(bit == '0' for bit in result):
            return ''.join(BINARY_ZERO)

        sign_bit = '0' if same_sign else '1'
        return sign_bit + result[1:]