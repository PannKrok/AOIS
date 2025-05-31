import pytest
from BinaryConverter import BinaryConverter
from BinaryArithmetics import BinaryArithmetic
from BinaryDivider import BinaryDivider
from CONST import BIT_SIZE, BINARY_ZERO

@pytest.fixture
def divider():
    conv = BinaryConverter()
    adder = BinaryArithmetic(conv)
    return BinaryDivider(conv, adder)

@pytest.fixture
def converter():
    return BinaryConverter()

def test_divide_positive_result(divider, converter):
    a = converter.to_direct_code(6)
    b = converter.to_direct_code(2)
    result = divider.divide(a, b)
    assert converter.to_decimal(result) == 3

def test_divide_negative_result(divider, converter):
    a = converter.to_direct_code(-8)
    b = converter.to_direct_code(2)
    result = divider.divide(a, b)
    assert converter.to_decimal(result) == -4

def test_divide_negative_by_negative(divider, converter):
    a = converter.to_direct_code(-12)
    b = converter.to_direct_code(-3)
    result = divider.divide(a, b)
    assert converter.to_decimal(result) == 4

def test_divide_by_larger(divider, converter):
    a = converter.to_direct_code(1)
    b = converter.to_direct_code(10)
    result = divider.divide(a, b)
    assert converter.to_decimal(result) == 0

def test_divide_zero_by_any(divider, converter):
    a = converter.to_direct_code(0)
    b = converter.to_direct_code(7)
    result = divider.divide(a, b)
    assert result == ''.join(BINARY_ZERO)

def test_divide_by_one(divider, converter):
    a = converter.to_direct_code(13)
    b = converter.to_direct_code(1)
    result = divider.divide(a, b)
    assert converter.to_decimal(result) == 13
