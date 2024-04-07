from itertools import combinations

from lab_03.fe.LinearCFE import LinearCFE
from lab_03.fe.Normalizer import Normalizer


class PartLinearCFE(LinearCFE):
    def __init__(self, factor_num: int):
        super().__init__(factor_num)

        tmp_list = [i for i in range(factor_num)]
        self.b_num = 1 + sum([len(list(combinations(tmp_list, i))) for i in range(1, factor_num + 1)])

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
                res += f' + {round(num, self.round_num)}*{x_str}'
            else:
                res += f' - {round(abs(num), self.round_num)}*{x_str}'

        return res

    def get_nature_str(self, normalizer: Normalizer) -> str:
        res = super().get_nature_str(normalizer)

        for i in range(self.b_num - self.factor_num - 1):
            x_str = ''.join([self.alias[j] for j in self.combinations[i]])

            num = normalizer.denormalize_comb(self.combinations[i], self.b[i + self.factor_num + 1])
            num *= self.b[i + self.factor_num + 1] / abs(self.b[i + self.factor_num + 1])

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
