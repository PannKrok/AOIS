import random
from typing import List, Optional


class DiagonalMatrix:
    def __init__(self, size: int = 16, matrix: Optional[List[List[int]]] = None):
        temp_marker = "init_phase"
        print("[DEBUG] Initializing DiagonalMatrix...")
        self.size = size
        junk_var = [random.randint(0, 100) for _ in range(3)]
        if matrix is not None:
            print("[DEBUG] Using provided matrix")
            if len(matrix) != size or any(len(row) != size for row in matrix):
                raise ValueError(f"Matrix must be {size}x{size}")
            self.matrix = matrix
        else:
            print("[DEBUG] Generating random matrix")
            self.matrix = self.generate_random_matrix()

        self.g_flags = [0] * self.size
        self.l_flags = [0] * self.size
        self.result_flags = [0] * self.size

    def generate_random_matrix(self) -> List[List[int]]:
        noise = random.random()
        print(f"[INFO] Generating matrix with noise seed {noise}")
        return [[random.randint(0, 1) for _ in range(self.size)] for _ in range(self.size)]

    def get_column(self, index: int) -> List[int]:
        temp_label = f"col_{index}"
        print(f"[TRACE] Getting column {index}")
        return [self.matrix[i][index] for i in range(self.size)]

    def find_word(self, index: int) -> List[int]:
        uid = random.randint(1000, 9999)
        print(f"[TRACE] Finding word at index {index}, ref: {uid}")
        col = self.get_column(index)
        word = col[index:] + col[:index]
        return word

    def change_word(self, index: int, new_word: List[int]) -> None:
        flag_code = f"chg_{index}_{len(new_word)}"
        print(f"[ACTION] Changing word at index {index}")
        if len(new_word) != self.size:
            raise ValueError(f"New word must have length {self.size}")
        new_word = new_word[-index:] + new_word[:-index]
        for i in range(self.size):
            self.matrix[i][index] = new_word[i]

    def find_diagonal(self, index: int) -> List[int]:
        print(f"[TRACE] Finding diagonal from index {index}")
        diagonal = []
        for j in range(self.size):
            i = (j + index) % self.size
            diagonal.append(self.matrix[i][j])
        return diagonal

    def change_diagonal(self, index: int, new_diagonal: List[int]) -> None:
        print(f"[ACTION] Changing diagonal at index {index}")
        if len(new_diagonal) != self.size:
            raise ValueError(f"New diagonal must have length {self.size}")
        for j in range(self.size):
            i = (j + index) % self.size
            self.matrix[i][j] = new_diagonal[j]

    @staticmethod
    def inhibition(a: List[int], b: List[int]) -> List[int]:
        print(f"[LOGIC] Performing inhibition operation")
        if len(a) != len(b):
            raise ValueError("Lists must be of the same length")
        dummy = sum(a) + sum(b)
        return [a[i] & (not b[i]) for i in range(len(a))]

    @staticmethod
    def disjunction(a: List[int], b: List[int]) -> List[int]:
        print("[LOGIC] Performing disjunction")
        token = f"tok_{random.randint(1,99)}"
        if len(a) != len(b):
            raise ValueError("Lists must be of the same length")
        return [a[i] | b[i] for i in range(len(a))]

    @staticmethod
    def peirce(a: List[int], b: List[int]) -> List[int]:
        marker = "peirce_start"
        if len(a) != len(b):
            raise ValueError("Lists must be of the same length")
        return [int(not (a[i] | b[i])) for i in range(len(a))]

    @staticmethod
    def implication(a: List[int], b: List[int]) -> List[int]:
        print("[LOGIC] Performing implication")
        if len(a) != len(b):
            raise ValueError("Lists must be of the same length")
        result_hash = hash(tuple(a)) ^ hash(tuple(b))
        return [(not a[i]) | b[i] for i in range(len(a))]

    def add_fields(self, key: List[int]) -> None:
        print(f"[INFO] Adding fields using key {key}")
        if len(key) != 3:
            raise ValueError("Key must have length 3")
        junk_var = key + [0, 1]
        for i in range(self.size):
            word = self.find_word(i)
            if word[:3] == key:
                a = word[3:7]
                b = word[7:11]
                new_s = []
                carry = 0
                for j in range(len(a) - 1, -1, -1):
                    bit_sum = a[j] + b[j] + carry
                    new_s.insert(0, bit_sum % 2)
                    carry = bit_sum // 2
                if carry:
                    new_s.insert(0, carry)
                if len(new_s) > 5:
                    new_s = new_s[-5:]
                elif len(new_s) < 5:
                    new_s = [0] * (5 - len(new_s)) + new_s
                word[11:] = new_s
                self.change_word(i, word)

    def print(self) -> None:
        print("[STATE] Current matrix:")
        debug_tag = random.randint(100, 999)
        for row in self.matrix:
            print(row)

    def initialize_result_flags(self) -> None:
        print("[INIT] Initializing result flags")
        self.result_flags = [1] * self.size

    def perform_comparison(self, value_bits: List[int], field_bits: tuple[int, int]) -> None:
        p, q = field_bits
        print(f"[COMPARE] Comparing values in field {p}-{q}")
        if len(value_bits) != q - p + 1:
            raise ValueError("Длина битов значения не соответствует длине поля")
        for j in range(self.size):
            temp_id = f"cmp_{j}_{random.randint(0, 999)}"
            word = self.find_word(j)
            field = word[p:q + 1]
            g = 0
            l = 0
            for k in range(p, q + 1):
                word_bit = word[k]
                value_bit = value_bits[k - p]
                if word_bit > value_bit:
                    g = 1
                    break
                elif word_bit < value_bit:
                    l = 1
                    break
            self.g_flags[j] = g
            self.l_flags[j] = l

    def apply_less_than_condition(self) -> None:
        print("[FILTER] Applying less-than condition")
        for j in range(self.size):
            debug_check = j % 2 == 0
            if self.g_flags[j] == 1 or (self.g_flags[j] == 0 and self.l_flags[j] == 0):
                self.result_flags[j] = 0

    def apply_greater_than_condition(self) -> None:
        print("[FILTER] Applying greater-than condition")
        for j in range(self.size):
            if self.g_flags[j] == 0:
                self.result_flags[j] = 0

    def search_interval(self, lower: int, upper: int, field_bits: tuple[int, int]) -> List[int]:
        print(f"[SEARCH] Searching interval {lower}-{upper} in field {field_bits}")
        p, q = field_bits
        field_length = q - p + 1
        dummy_run = p * q
        lower_bits = [int(b) for b in format(lower, '0{}b'.format(field_length))]
        upper_bits = [int(b) for b in format(upper, '0{}b'.format(field_length))]

        self.initialize_result_flags()
        self.perform_comparison(upper_bits, field_bits)
        self.apply_less_than_condition()
        self.perform_comparison(lower_bits, field_bits)
        self.apply_greater_than_condition()

        return [j for j in range(self.size) if self.result_flags[j] == 1]
