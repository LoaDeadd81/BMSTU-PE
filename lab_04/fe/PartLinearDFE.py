from itertools import combinations

from lab_04.fe.LinearDFE import LinearDFE
from lab_04.fe.Normalizer import Normalizer


class PartLinearDFE(LinearDFE):
    def __init__(self, data):
        super().__init__(data)

        tmp_list = [i for i in range(self.factor_num)]
        self.b_num = 1 + sum([len(list(combinations(tmp_list, i))) for i in range(1, self.factor_num + 1)])

        self.create_combinations()
        self.expand_plan_matrix()

    def get_alias(self) -> list[str]:
        return (self.alias +
                [''.join([self.alias[j] for j in self.combinations[i]])
                 for i in range(self.b_num - self.factor_num - 1)])

    def create_combinations(self):
        tmp = [i for i in range(self.factor_num)]

        self.combinations = []
        for i in range(2, self.factor_num + 1):
            self.combinations.extend(combinations(tmp, i))

    def expand_plan_matrix(self):
        for i in range(self.N):
            for j in range(len(self.combinations)):
                tmp = 1

                for k in range(len(self.combinations[j])):
                    tmp *= self.matrix[i][self.combinations[j][k] + 1]

                self.matrix[i].append(tmp)

    def get_norm_str(self) -> str:
        res = super().get_norm_str()

        for i in range(self.b_num - self.factor_num - 1):
            x_str = ''.join([self.alias[j] for j in self.combinations[i]])
            num = self.b[i + self.factor_num + 1]
            if num > 0:
                res += ' + ' + self.format_num.format(num) + x_str
            else:
                res += ' - ' + self.format_num.format(abs(num)) + x_str

        return res

    def get_nature_str(self, normalizer: Normalizer) -> str:
        res = ""

        zeros = normalizer.zeros
        intervals = normalizer.intervals
        coeff = [{x} for x in range(self.factor_num)] + [set(x) for x in self.combinations]
        combinations = [[x] for x in range(self.factor_num)] + [list(x) for x in self.combinations]

        self.b_nat = [0] * (self.b_num)
        self.b_nat[0] = self.b[0]
        for i in range(len(combinations)):
            tmp = self.b[i + 1]
            for x in combinations[i]:
                tmp *= zeros[x] / intervals[x] * -1
            # if len(combinations[i]) % 2 != 0:
            #     tmp *= -1
            self.b_nat[0] += tmp

        res += f'{round(self.b_nat[0], self.round_num)}'

        for i in range(len(combinations)):
            x_str = ''.join([self.alias[j] for j in combinations[i]])

            num = 0
            cur_coeff = coeff[i]
            for j in range(len(coeff)):
                if cur_coeff.issubset(coeff[j]):
                    tmp = self.b[j + 1]
                    for x in (coeff[j] - cur_coeff):
                        tmp *= zeros[x] * -1
                    for x in coeff[j]:
                        tmp /= intervals[x]

                    num += tmp

            self.b_nat[i + 1] = num
            if num > 0:
                res += f' + {round(num, self.round_num)}*{x_str}'
            else:
                res += f' - {round(abs(num), self.round_num)}*{x_str}'

        return res

    def get_y(self, data: list[float]) -> float:
        if len(self.b) == 0:
            raise Exception("Сначала нужно рассчитать коэффициенты")

        for i in range(len(self.combinations)):
            tmp = 1

            for j in range(len(self.combinations[i])):
                tmp *= data[self.combinations[i][j]]

            data.append(tmp)

        return self.b[0] + sum([data[j - 1] * self.b[j] for j in range(1, self.b_num)])

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
                return False

        return True
