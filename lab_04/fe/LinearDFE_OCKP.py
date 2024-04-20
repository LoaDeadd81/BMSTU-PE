from lab_04.fe.LinearDFE import LinearDFE
from math import sqrt
from statistics import mean

from lab_04.fe.Normalizer import Normalizer


class LinearDFE_OCKP(LinearDFE):

    def __init__(self, data):
        super().__init__(data)
        self.b_nat = []
        self.N_0 = self.N
        self.N = self.N_0 + 2 * self.factor_num + 1
        self.alpha = sqrt(self.N_0 / 2 * (sqrt(self.N / self.N_0) - 1))
        self.S = sqrt(self.N_0 / self.N)

        self.combinations = [[x, x] for x in range(self.factor_num)]

        self.expand_OCKP_plan_matrix()
        self.expand_alias()

        self.b_num = 1 + 2 * self.factor_num

    def expand_OCKP_plan_matrix(self):
        for i in range(self.factor_num):
            self.matrix.append([1] + [0] * self.factor_num)
            self.matrix[-1][i + 1] = self.alpha
            self.matrix.append([1] + [0] * self.factor_num)
            self.matrix[-1][i + 1] = -self.alpha
        self.matrix.append([1] + [0] * self.factor_num)

        for i in range(len(self.matrix)):
            for x in range(self.factor_num):
                self.matrix[i].append(self.matrix[i][x + 1] * self.matrix[i][x + 1] - self.S)

    def expand_alias(self):
        super().create_alias()

        for i in range(self.factor_num):
            self.alias.append(f'({self.alias[i]})^2')

    def get_alpha(self) -> float:
        return self.alpha

    def get_S(self) -> float:
        return self.S

    def count_b(self, y: list[float]):
        self.b = [mean(y)]
        self.b_similar = [mean(y)]

        for j in range(1, self.b_num):
            # self.b.append(sum([self.matrix[i][j] * y[i] for i in range(self.N)]) / self.N)
            numer = 0
            denom = 0
            for i in range(self.N):
                numer += self.matrix[i][j] * y[i]
                denom += self.matrix[i][j] * self.matrix[i][j]
            self.b.append(numer / denom)
            self.b_similar.append(numer / denom)

        self.b_similar[0] -= sum([self.b[i] for i in range(self.factor_num + 1, self.b_num)]) * self.S

    def get_y(self, data: list[float]) -> float:
        if len(self.b) == 0:
            raise Exception("Сначала нужно рассчитать коэффициенты")

        for i in range(len(self.combinations)):
            tmp = 1

            for j in range(len(self.combinations[i])):
                tmp *= data[self.combinations[i][j]]

            tmp -= self.S
            data.append(tmp)

        return self.b[0] + sum([data[j - 1] * self.b[j] for j in range(1, self.b_num)])

        # return self.b_similar[0] + sum([data[j - 1] * self.b_similar[j] for j in range(1, self.b_num)])

    def get_norm_str(self) -> str:
        if len(self.b) == 0:
            raise Exception("Сначала нужно рассчитать коэффициенты")

        res = f"{round(self.b[0], self.round_num)}"

        for i in range(1, self.b_num):
            num = self.b[i]
            x_str = self.alias[i - 1]
            if i > self.factor_num:
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
        if len(self.b) == 0:
            raise Exception("Сначала нужно рассчитать коэффициенты")

        self.b_nat = [0.0] * (2 * self.factor_num + 1)
        zeros = [0] + normalizer.zeros
        intervals = [1] + normalizer.intervals

        self.b_nat[0] = self.b_similar[0]
        for i in range(1, self.factor_num + 1):
            self.b_nat[0] -= self.b[i] * zeros[i] / intervals[i]
        for i in range(self.factor_num + 1, self.b_num):
            self.b_nat[0] += self.b[i] * pow(zeros[i - self.factor_num], 2) / pow(intervals[i - self.factor_num], 2)
        res = f"{round(self.b_nat[0], self.round_num)}"

        for i in range(1, self.factor_num + 1):
            num = (self.b[i] / intervals[i]) - (self.b[i + self.factor_num] * 2 * zeros[i] / pow(intervals[i], 2))
            self.b_nat[i] = num
            if num > 0:
                res += f" + {round(num, self.round_num)}*{self.alias[i - 1]}"
            else:
                res += f" - {round(abs(num), self.round_num)}*{self.alias[i - 1]}"

        for i in range(self.factor_num + 1, self.b_num):
            num = self.b[i] / pow(intervals[i - self.factor_num], 2)
            self.b_nat[i] = num
            if num > 0:
                res += f" + {round(num, self.round_num)}*{self.alias[i - 1]}"
            else:
                res += f" - {round(abs(num), self.round_num)}*{self.alias[i - 1]}"

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
