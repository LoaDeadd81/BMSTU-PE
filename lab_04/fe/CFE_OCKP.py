from math import sqrt
from statistics import mean

from lab_04.fe.Normalizer import Normalizer
from lab_04.fe.PartLinearCFE import PartLinearCFE


class CFE_OCKP(PartLinearCFE):

    def __init__(self, factor_num: int):
        super().__init__(factor_num)

        self.N_0 = self.N
        self.N = self.N_0 + 2 * self.factor_num + 1
        self.alpha = sqrt(self.N_0 / 2 * (sqrt(self.N / self.N_0) - 1))
        self.S = sqrt(self.N_0 / self.N)

        self.expand_OCKP_plan_matrix()
        super().create_combinations()
        self.combinations += [(x, x) for x in range(self.factor_num)]
        super().expand_plan_matrix()
        self.sqr_index = len(self.matrix[0]) - self.factor_num
        self.minus_s()

        self.expand_alias()

        self.b_num = len(self.matrix[0])

    def expand_OCKP_plan_matrix(self):
        for i in range(self.factor_num):
            self.matrix.append([1] + [0] * self.factor_num)
            self.matrix[-1][i + 1] = self.alpha
            self.matrix.append([1] + [0] * self.factor_num)
            self.matrix[-1][i + 1] = -self.alpha
        self.matrix.append([1] + [0] * self.factor_num)

    def minus_s(self):
        for i in range(len(self.matrix)):
            for j in range(self.sqr_index, len(self.matrix[0])):
                self.matrix[i][j] -= self.S

    def expand_alias(self):
        super().create_alias()

        self.alias += [''.join([self.alias[j] for j in self.combinations[i]]) for i in
                       range(self.b_num - self.factor_num - 1)]

        for i in range(self.factor_num):
            self.alias.append(f'({self.alias[i]})^2')

    def count_b(self, y: list[float]):
        self.b = [mean(y)]
        self.b_similar = [self.b[0]]

        for j in range(1, self.b_num):
            numer = 0
            denom = 0
            for i in range(self.N):
                numer += self.matrix[i][j] * y[i]
                denom += self.matrix[i][j] * self.matrix[i][j]
            self.b.append(numer / denom)
            self.b_similar.append(numer / denom)

        self.b_similar[0] -= sum([self.b[i] for i in range(self.sqr_index, self.b_num)]) * self.S

    def get_y(self, data: list[float]) -> float:
        if len(self.b) == 0:
            raise Exception("Сначала нужно рассчитать коэффициенты")

        for i in range(len(self.combinations)):
            tmp = 1

            for j in range(len(self.combinations[i])):
                tmp *= data[self.combinations[i][j]]

            if i >= len(self.combinations) - self.factor_num:
                tmp -= self.S
            data.append(tmp)

        return self.b[0] + sum([data[j - 1] * self.b[j] for j in range(1, self.b_num)])

    def get_norm_str(self) -> str:
        if len(self.b) == 0:
            raise Exception("Сначала нужно рассчитать коэффициенты")

        res = f"{round(self.b[0], self.round_num)}"

        for i in range(1, self.b_num):
            num = self.b[i]
            x_str = self.alias[i - 1]

            if i >= self.sqr_index:
                x_str = f'({x_str} - {self.format_num.format(self.S)})'

            if self.b[i] > 0:
                res += ' + ' + self.format_num.format(num) + '*' + x_str
            else:
                res += ' - ' + self.format_num.format(abs(num)) + '*' + x_str
        return res

    def get_norm_similar_str(self) -> str:
        if len(self.b_similar) == 0:
            raise Exception("Сначала нужно рассчитать коэффициенты")

        res = f"{round(self.b_similar[0], self.round_num)}"

        for i in range(1, self.b_num):
            num = self.b_similar[i]
            x_str = self.alias[i - 1]

            if self.b_similar[i] > 0:
                res += ' + ' + self.format_num.format(num) + '*' + x_str
            else:
                res += ' - ' + self.format_num.format(abs(num)) + '*' + x_str
        return res

    def get_nature_str(self, normalizer: Normalizer) -> str:
        res = ""

        self.b_nat = [0] * (self.b_num)
        zeros = normalizer.zeros
        intervals = normalizer.intervals
        coeff = [{x} for x in range(self.factor_num)] + [set(x) for x in self.combinations]
        combinations = [[x] for x in range(self.factor_num)] + [list(x) for x in self.combinations]

        self.b_nat[0] = self.b_similar[0]
        for i in range(len(combinations)):
            # if combinations[i] == [0, 0]:
            #     print()
            tmp = self.b[i + 1]
            for x in combinations[i]:
                tmp *= zeros[x] / intervals[x] * -1
            self.b_nat[0] += tmp

        res += f'{round(self.b_nat[0], self.round_num)}'

        for i in range(len(combinations) - self.factor_num):
            x_str = self.alias[i]

            num = 0
            cur_coeff = coeff[i]
            for j in range(len(coeff)):
                if cur_coeff.issubset(coeff[j]):
                    tmp = self.b[j + 1]
                    for x in (coeff[j] - cur_coeff):
                        tmp *= zeros[x] * -1
                    for x in coeff[j]:
                        tmp /= intervals[x]
                    if len(combinations[j]) == 2 and combinations[j][0] == combinations[j][1]:
                        index = combinations[j][0]
                        tmp *= 2 * zeros[index] / intervals[index]
                        tmp *= -1

                    num += tmp

            self.b_nat[i + 1] = num
            if num > 0:
                res += f' + {round(num, self.round_num)}*{x_str}'
            else:
                res += f' - {round(abs(num), self.round_num)}*{x_str}'

        for i in range(len(combinations) - self.factor_num, len(combinations)):
            x_str = self.alias[i]

            index = combinations[i][0]
            num = self.b[i + 1] / pow(intervals[index], 2)
            self.b_nat[i + 1] = num

            if num > 0:
                res += f' + {round(num, self.round_num)}*{x_str}'
            else:
                res += f' - {round(abs(num), self.round_num)}*{x_str}'

        return res

    def check(self, normalizer: Normalizer) -> bool:
        eps = 1e-4

        combinations = [[x] for x in range(self.factor_num)] + [list(x) for x in self.combinations]

        for i in range(self.N):
            y_norm = sum([self.matrix[i][j] * self.b[j] for j in range(self.b_num)])
            y_nat = self.matrix[i][0] * self.b_nat[0]
            for j in range(1, self.b_num):
                x_val = 1
                for x in combinations[j - 1]:
                    x_val *= normalizer.denormalize(x, self.matrix[i][x + 1])
                y_nat += x_val * self.b_nat[j]

            if abs(y_norm - y_nat) > eps:
                print(i)
                print(y_norm, y_nat)
                return False

        return True

    def get_alias(self) -> list[str]:
        return self.alias

    def get_alpha(self) -> float:
        return self.alpha

    def get_S(self) -> float:
        return self.S
