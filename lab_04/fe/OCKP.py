from lab_04.fe.LinearDFE import LinearDFE
from math import sqrt


class OCKP(LinearDFE):

    def __init__(self, data):
        super().__init__(data)
        self.N_0 = self.N
        self.N = self.N_0 + 2 * self.factor_num + 1
        self.alpha = sqrt(self.N_0 / 2 * (sqrt(self.N / self.N_0) - 1))
        self.S = sqrt(self.N_0 / self.N)

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
