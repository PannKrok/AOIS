from BinaryArithmetics import BinaryArithmetic
from BinaryConverter import BinaryConverter
from CONST import BINARY_ZERO, BINARY_ONE

class BinaryDivider:
    def __init__(self, conv: BinaryConverter, adder: BinaryArithmetic):
        self.conv = conv
        self.adder = adder

    def divide(self, dividend: str, divisor: str) -> str:
        quotient = "".join(BINARY_ZERO)
        opposite = dividend[0] != divisor[0]

        dividend = '0' + dividend[1:]
        divisor = '1' + divisor[1:]

        dividend_val = self.conv.to_decimal(dividend)
        divisor_val = self.conv.to_decimal(divisor)

        dividend_bin = self.conv.to_complement_code(dividend_val)
        divisor_bin = self.conv.to_complement_code(divisor_val)

        trial_add = self.adder.sum_complement(dividend_bin, divisor_bin)

        if trial_add[0] == '0':
            while dividend[0] != '1':
                dividend = self.adder.sum_complement(
                    dividend,
                    self.conv.to_complement_code(divisor_val)
                )
                if dividend[0] != '1':
                    quotient = self.adder.sum_complement(quotient, ''.join(BINARY_ONE))

        if list(quotient) == BINARY_ZERO:
            return quotient

        return ('1' + quotient[1:]) if opposite else quotient