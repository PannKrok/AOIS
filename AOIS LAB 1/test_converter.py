import pytest
from BinaryConverter import BinaryConverter

@pytest.fixture
def converter():
    return BinaryConverter()

def test_to_bin_string_zero(converter):
    assert converter.to_bin_string(0) == '0' * (converter.bit_width - 1)

def test_to_bin_string_positive(converter):
    assert converter.to_bin_string(5).endswith('101')

def test_to_bin_string_padding(converter):
    bin_str = converter.to_bin_string(3)
    assert len(bin_str) == converter.bit_width - 1

def test_to_decimal_positive(converter):
    binary = '0' + converter.to_bin_string(7)
    assert converter.to_decimal(binary) == 7

def test_to_decimal_negative(converter):
    binary = '1' + converter.to_bin_string(7)
    assert converter.to_decimal(binary) == -7

def test_to_direct_code_positive(converter):
    assert converter.to_direct_code(5).startswith('0')

def test_to_direct_code_negative(converter):
    assert converter.to_direct_code(-5).startswith('1')

def test_to_inverse_code_positive(converter):
    assert converter.to_inverse_code(3).startswith('0')

def test_to_inverse_code_negative(converter):
    result = converter.to_inverse_code(-3)
    assert result.startswith('1')
    assert set(result[1:]).issubset({'0', '1'})

def test_to_complement_code_positive(converter):
    assert converter.to_complement_code(4).startswith('0')

def test_to_complement_code_negative(converter):
    result = converter.to_complement_code(-1)
    assert result.startswith('1')
    assert set(result).issubset({'0', '1'})

def test_float_to_bin32_zero(converter):
    assert converter.float_to_bin32(0.0) == '0' * 32

def test_float_to_bin32_inf(converter):
    assert converter.float_to_bin32(float('inf')).startswith('0' + '1'*8)

def test_float_to_bin32_basic(converter):
    result = converter.float_to_bin32(1.5)
    assert result[0] == '0'  # sign bit
    assert len(result) == 32

def test_bin32_to_float_basic(converter):
    float_val = 2.5
    bin_str = converter.float_to_bin32(float_val)
    restored = converter.bin32_to_float(bin_str)
    assert abs(restored - float_val) < 1e-5

def test_bin32_to_float_negative(converter):
    float_val = -3.75
    bin_str = converter.float_to_bin32(float_val)
    restored = converter.bin32_to_float(bin_str)
    assert abs(restored - float_val) < 1e-5
