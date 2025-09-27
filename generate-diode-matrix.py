N_buttons = 8
N_outputs = 3
ROWS = N_buttons
MAX_ENUM = 1_000_000
ALLOW_DONTCARE = True

def build_default_target():
    target = []
    for i in range(ROWS):
        if i >= (1 << N_outputs):
            raise RuntimeError('N_outputs too small for button range')
        target.append(i)
    return target

def enumerate_solutions(target):
    per_row_options = []
    full_mask = (1 << N_outputs) - 1
    for r in range(ROWS):
        val = target[r]
        if val is None and ALLOW_DONTCARE:
            per_row_options.append(list(range(1 << N_outputs)))
        else:
            per_row_options.append([val & full_mask])
    total = 1
    for opts in per_row_options:
        total *= len(opts)
        if total > MAX_ENUM:
            raise RuntimeError('enumeration too large')
    from itertools import product
    solutions = []
    for choice in product(*per_row_options):
        diode_count = sum(bin(row).count('1') for row in choice)
        solutions.append((diode_count, list(choice)))
    solutions.sort(key=lambda x: (x[0], x[1]))
    return solutions

def fmt_matrix(matrix):
    lines = []
    for r,row in enumerate(matrix):
        bits = format(row, f'0{N_outputs}b')
        lines.append(f'button {r:02d} ({r:0{N_outputs}b}): {bits}')
    return '\n'.join(lines)

if __name__ == '__main__':
    TARGET = build_default_target()
    sols = enumerate_solutions(TARGET)
    print(f'Enumerated {len(sols)} solution(s).')
    if not sols:
        raise SystemExit('no solutions')
    best_count = sols[0][0]
    print(f'Best diode count = {best_count}\n')
    for idx,(count,matrix) in enumerate(sols):
        print(f'Solution {idx+1}: diodes = {count}')
        print(fmt_matrix(matrix))
        print()

