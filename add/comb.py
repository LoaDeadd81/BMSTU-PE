from itertools import combinations


def factor_mult(f1: list[int], f2: list[int]) -> list[int]:
    s1 = set(f1)
    s2 = set(f2)

    return list(s1 ^ s2)


def factor_mult_arr(f: list[list[int]]) -> list[int]:
    s = set(f[0])

    for i in range(1, len(f)):
        s ^= set(f[i])

    return list(s)


def main():
    max_i = 2
    # data = [1, [1, 3, 5], 3, [1, 3, 7], 5, [3, 5, 7], 7, [1, 5, 7]]
    data = [1, 2, 3, 4, [1, 2, 3], [1, 2, 4], [2, 3, 4], [1, 3, 4]]
    # data = [1, 2, 3, [1, 2, 3], [1, 2], [1, 3], [2, 3]]
    # data = [1, 2, 3, [1, 2]]
    # data = [1, [1, 3], 3, [1, 5], 5, [3, 5]]

    combo_f = []
    for i in range(len(data)):
        if isinstance(data[i], list):
            combo_f.append(factor_mult([i + 1], data[i]))
    print(combo_f)

    combo_len = len(combo_f)

    combs = []
    tmp = [i for i in range(combo_len)]
    for i in range(2, combo_len + 1):
        combs.extend(combinations(tmp, i))
    # print(combs)

    for combo in combs:
        cur = []
        for i in combo:
            cur.append(combo_f[i])
        combo_f.append(factor_mult_arr(cur))

    print('1 = ', end='')
    for i in combo_f:
        print(i, '=', end=' ')
    print('\n')

    for i in range(len(data)):
        print(f'x{i + 1} =', end=' ')
        for cmb in combo_f:
            b = factor_mult([i + 1], cmb)
            if len(b) > max_i:
                continue
            print(b, '=', end=' ')
        print('\n', end='')


if __name__ == '__main__':
    main()
