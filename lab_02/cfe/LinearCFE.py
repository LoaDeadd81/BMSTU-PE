from statistics import mean


class LinearCFE:
    def __init__(self, factor_num: int):
        self.factor_num = factor_num
        self.N = 2 ** factor_num
        self.b_num = factor_num + 1
        self.b = []

        self.create_alias()
        self.create_plan_matrix()

    def create_alias(self):
        self.alias = [f'x{i + 1}' for i in range(self.factor_num)]

    def create_plan_matrix(self):
        self.matrix = [[1 for _ in range(self.factor_num + 1)] for _ in range(self.N)]

        period = self.N // 2
        mlt = 1

        for j in range(1, self.factor_num + 1):
            for i in range(self.N):
                if i % period == 0:
                    mlt *= -1

                self.matrix[i][j] *= mlt

            period //= 2

    def get_matrix(self) -> list[list[int]]:
        return self.matrix

    def count_b(self, y: list[float]):
        self.b = [mean(y)]

        for j in range(1, self.b_num):
            self.b.append(sum([self.matrix[i][j] * y[i] for i in range(self.N)]) / self.N)

    def count_y(self) -> list[float]:
        res = []

        for i in range(self.N):
            y = sum([self.matrix[i][j] * self.b[j] for j in range(self.b_num)])
            res.append(y)

        return res

    def get_norm_str(self) -> str:
        res = f"{round(self.b[0], 2)}"

        for i in range(1, self.factor_num + 1):
            if self.b[i] > 0:
                res += f" + {round(self.b[i], 2)}*{self.alias[i - 1]}"
            else:
                res += f" - {round(abs(self.b[i]), 2)}*{self.alias[i - 1]}"
        return res

    def get_y(self, data: list[float]) -> float:
        return self.b[0] + sum([data[j - 1] * self.b[j] for j in range(1, self.b_num)])
