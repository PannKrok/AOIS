import pytest
from BinaryArithmetics import BinaryArithmetic
from CONST import BIT_SIZE, BINARY_ONE
from BinaryConverter import BinaryConverter

# Создадим фикстуру для BinaryArithmetic с моковым BinaryConverterpi
@pytest.fixture
def binary_arithmetic():
    converter = BinaryConverter()  # предполагаем, что есть конструктор без аргументов
    return BinaryArithmetic(converter)

def test_sum_bits_basic(binary_arithmetic):
    # Используем публичные методы, _sum_bits приватный, проверим через sum_direct
    a = '0101'
    b = '0011'
    result = binary_arithmetic.sum_direct(a, b)
    assert result == '1000'

def test_sum_direct_length(binary_arithmetic):
    a = '1111'
    b = '0001'
    assert binary_arithmetic.sum_direct(a, b) == '10000'

def test_sum_inverse_no_carry(binary_arithmetic):
    a = '0001' + '0' * (BIT_SIZE - 4)
    b = '0001' + '0' * (BIT_SIZE - 4)
    result = binary_arithmetic.sum_inverse(a, b)
    assert len(result) == BIT_SIZE
    assert result[0] in ('0', '1')  # знак
    # проверим, что результат - бинарная строка нужной длины
    assert set(result).issubset({'0','1'})

def test_sum_inverse_with_carry(binary_arithmetic):
    a = '1' * BIT_SIZE
    b = '1' * BIT_SIZE
    result = binary_arithmetic.sum_inverse(a, b)
    assert len(result) == BIT_SIZE
    assert set(result).issubset({'0','1'})

def test_sum_complement_basic(binary_arithmetic):
    a = '0' * (BIT_SIZE-1) + '1'
    b = '0' * (BIT_SIZE-1) + '1'
    result = binary_arithmetic.sum_complement(a, b)
    assert len(result) == BIT_SIZE
    assert set(result).issubset({'0','1'})

def test_float_sum_32bit_zero(binary_arithmetic):
    a = '0' * 32
    b = '0' * 32
    result = binary_arithmetic.float_sum_32bit(a, b)
    # Проверка на ноль
    assert int(result, 2) == 0


def test_float_sum_32bit_basic_addition(binary_arithmetic):
    # Сложение двух чисел с простыми мантиссами и экспонентами
    a = '0' + '10000000' + '00000000000000000000000'  # 1.0 in IEEE 754 float
    b = '0' + '10000000' + '00000000000000000000000'  # 1.0
    result = binary_arithmetic.float_sum_32bit(a, b)
    # Результат должен быть примерно 2.0 (экспонента увеличится на 1)
    assert result.startswith('0')  # знак +
    assert int(result[1:9], 2) > 128  # экспонента увеличилась

def test_float_sum_32bit_overflow(binary_arithmetic):
    # Пример числа с большой экспонентой, чтобы вызвать переполнение
    a = '0' + '11111110' + '11111111111111111111111'  # большое число
    b = '0' + '11111110' + '11111111111111111111111'
    result = binary_arithmetic.float_sum_32bit(a, b)
    # Ожидаем infinity
    assert result[1:9] == '11111111'


