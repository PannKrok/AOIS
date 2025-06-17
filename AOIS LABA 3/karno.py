from prettytable import PrettyTable
import itertools
from raschet import *
from snf import *
from copy import deepcopy


class KarnaughCell:
    def __init__(self, result, inputs):
        self.result = result
        self.inputs = inputs
        self.in_pair = False
        self.in_block = False
        self.mode = "dnf" if self.result == 1 else "cnf"


def mark_cell(cell):
    cell.in_pair = True


def karnaugh_method(results, mdnf, mcnf, variables_count):
    grid, cells = PrettyTable(), []
    rows, cols = get_dimensions(variables_count)
    row_bits = variables_count // 2
    col_bits = variables_count - row_bits
    row_vals = reorder_gray(itertools.product([0, 1], repeat=row_bits))
    col_vals = reorder_gray(itertools.product([0, 1], repeat=col_bits))

    grid.field_names = [""] + [str(c) for c in col_vals]
    for i, r in enumerate(row_vals):
        line = [str(r)]
        for j, c in enumerate(col_vals):
            idx = compute_index(r, c, row_bits, col_bits, len(results))
            line.append(results[idx])
        grid.add_row(line)

    print(grid)
    print_minimized_dnf(mdnf)
    print_minimized_cnf(mcnf)

    for i in range(len(results)):
        bin_inputs = list(itertools.product([0, 1], repeat=variables_count))[i]
        cells.append(KarnaughCell(int(results[i]), list(bin_inputs)))

    return generate_blocks(cells, variables_count)


def get_dimensions(n):
    return (2, 2) if n == 2 else (2, 4) if n == 3 else (4, 4) if n == 4 else (2, 2)


def reorder_gray(seq):
    combo_list = list(seq)
    gray_list = [combo_list[0]]
    for _ in range(1, len(combo_list)):
        last = gray_list[-1]
        for item in combo_list:
            if item not in gray_list and sum(x != y for x, y in zip(last, item)) == 1:
                gray_list.append(item)
                break
    return gray_list


def compute_index(r, c, row_len, col_len, total):
    bits = list(r) + list(c)
    pos = sum(bit * (1 << i) for i, bit in enumerate(bits[::-1]))
    return min(pos, total - 1)


def analyze_neighbors(idx, table, var_count):
    res_list = [table[idx].inputs]
    rows, cols = get_dimensions(var_count)
    row = idx // cols
    col = idx % cols
    neighbors = []

    right = (col + 1) % cols if var_count >= 3 else col + 1
    if right < cols:
        neighbor_idx = row * cols + right
        if not table[neighbor_idx].in_pair and table[neighbor_idx].result == table[idx].result:
            neighbors.append(neighbor_idx)

    down = (row + 1) % rows if var_count == 4 else row + 1
    if down < rows:
        neighbor_idx = down * cols + col
        if not table[neighbor_idx].in_pair and table[neighbor_idx].result == table[idx].result:
            neighbors.append(neighbor_idx)

    if not neighbors:
        return None, table

    for n in neighbors:
        res_list.append(table[n].inputs)
        table[n].in_pair = True

    return [deepcopy(res_list)], table


def generate_blocks(cell_table, var_count):
    dnf_blocks, cnf_blocks = [], []
    for i in range(len(cell_table)):
        if cell_table[i].in_pair or cell_table[i].in_block:
            continue
        group, cell_table = analyze_neighbors(i, cell_table, var_count)
        if group:
            (dnf_blocks if cell_table[i].mode == "dnf" else cnf_blocks).extend(group)

        big_group, cell_table = detect_large_group(i, cell_table, var_count)
        if big_group:
            (dnf_blocks if cell_table[i].mode == "dnf" else cnf_blocks).extend(big_group)

    dnf_result = minimize_group(dnf_blocks, "sdnf", var_count)
    cnf_result = minimize_group(cnf_blocks, "scnf", var_count)
    return f"МДНФ: {dnf_result}\nМКНФ: {cnf_result}"


def detect_large_group(index, table, var_count):
    rows, cols = get_dimensions(var_count)
    r = index // cols
    c = index % cols
    block = []

    if r + 1 < rows and c + 1 < cols:
        block = [index, index + 1, index + cols, index + cols + 1]
        if all(table[i].result == table[index].result and not table[i].in_pair and not table[i].in_block for i in block):
            for i in block:
                table[i].in_block = True
            return [deepcopy([table[i].inputs for i in block])], table

    if var_count == 3 and c == 0:
        wrap_block = [index, index + 3, index + cols, index + cols + 3]
        if all(i < len(table) for i in wrap_block):  # ⬅ Защита от выхода за границы
            if all(table[i].result == table[index].result and not table[i].in_pair and not table[i].in_block for i in
                   wrap_block):
                for i in wrap_block:
                    table[i].in_block = True
                return [deepcopy([table[i].inputs for i in wrap_block])], table

    return None, table


def minimize_group(groups, mode, var_count):
    if not groups:
        return ""
    result = ""
    used = set()
    for group in groups:
        group_tup = tuple(map(tuple, group))
        if group_tup in used:
            continue
        part = "("
        for i, bits in enumerate(zip(*group)):
            if all(bit == 0 for bit in bits):
                part += f"!a{i+1}&" if mode == "sdnf" else f"a{i+1}|"
            elif all(bit == 1 for bit in bits):
                part += f"a{i+1}&" if mode == "sdnf" else f"!a{i+1}|"
        part = part.strip("&").strip("|") + ")"
        if part != "()":
            result += part + ("|" if mode == "sdnf" else "&")
            used.add(group_tup)
    return result.strip("&").strip("|")


































































ajsdjbasjdbajsbdjhabsjhdbajsbdhjabsj vashgdvahisjncolasbdutycrfvgbhnjoaokpsjidgtsrAEWRDTHUJOKPAL[SDYOATYDRSERDSQAl,[]ashtraeDTSVNJOKASDPASTRDXAS.L,;DA;SKJBVCGASVBHNMKAL;,SDKJKHCXSGVBAJSMK;LDMAJKSJGVCGD