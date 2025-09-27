N_inputs = 3
N_outputs = 8
ROWS = 1 << N_inputs
MAX_ENUM = 1000000

def build_target_onehot():
    target = [0]*ROWS
    for i in range(ROWS):
        target[i] = 1 << i
    return target

def enumerate_solutions(target, allow_dontcare=False):
    per_row_options = []
    for r in range(ROWS):
        if target[r] is None and allow_dontcare:
            per_row_options.append(list(range(1 << N_outputs)))
        else:
            per_row_options.append([target[r]])
    total = 1
    for opts in per_row_options:
        total *= len(opts)
        if total > MAX_ENUM:
            raise RuntimeError('enumeration too large')
    from itertools import product
    solutions = []
    for choice in product(*per_row_options):
        matrix = list(choice)
        diode_count = sum(bin(row).count('1') for row in matrix)
        solutions.append((diode_count, matrix))
    solutions.sort(key=lambda x: (x[0], x[1]))
    return solutions

def fmt_matrix(matrix):
    lines = []
    for r,row in enumerate(matrix):
        bits = format(row, f'0{N_outputs}b')
        lines.append(f'row {r:02d} ({r:0{N_inputs}b}): {bits}')
    return '\n'.join(lines)

if __name__ == '__main__':
    target = build_target_onehot()
    sols = enumerate_solutions(target, allow_dontcare=False)
    print(f'Found {len(sols)} solution(s).\n')
    for idx,(count,matrix) in enumerate(sols):
        print(f'Solution {idx+1}: diodes = {count}')
        print(fmt_matrix(matrix))
        print()

