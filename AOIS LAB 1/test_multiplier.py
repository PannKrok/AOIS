import pytest
from BinaryConverter import BinaryConverter
from BinaryArithmetics import BinaryArithmetic
from BinaryMultiplier import BinaryMultiplier
from CONST import BINARY_ZERO

@pytest.fixture
def multiplier():
    conv = BinaryConverter()
    adder = BinaryArithmetic(conv)
    return BinaryMultiplier(conv, adder)

@pytest.fixture
def converter():
    return BinaryConverter()

def test_multiply_positive(multiplier, converter):
    a = converter.to_direct_code(3)
    b = converter.to_direct_code(4)
    result = multiplier.multiply(a, b)
    assert converter.to_decimal(result) == 12

def test_multiply_negative_result(multiplier, converter):
    a = converter.to_direct_code(-2)
    b = converter.to_direct_code(3)
    result = multiplier.multiply(a, b)
    assert converter.to_decimal(result) == -6

def test_multiply_two_negatives(multiplier, converter):
    a = converter.to_direct_code(-5)
    b = converter.to_direct_code(-4)
    result = multiplier.multiply(a, b)
    assert converter.to_decimal(result) == 20

def test_multiply_by_zero(multiplier, converter):
    a = converter.to_direct_code(0)
    b = converter.to_direct_code(10)
    result = multiplier.multiply(a, b)
    assert result == ''.join(BINARY_ZERO)

def test_multiply_zero_by_negative(multiplier, converter):
    a = converter.to_direct_code(0)
    b = converter.to_direct_code(-3)
    result = multiplier.multiply(a, b)
    assert result == ''.join(BINARY_ZERO)

def test_multiply_by_one(multiplier, converter):
    a = converter.to_direct_code(7)
    b = converter.to_direct_code(1)
    result = multiplier.multiply(a, b)
    assert converter.to_decimal(result) == 7
