from itertools import combinations

from lab_02.cfe.LinearCFE import LinearCFE
from lab_02.cfe.Normalizer import Normalizer


class PartLinearCFE(LinearCFE):
    def __init__(self, factor_num: int):
        super().__init__(factor_num)

        self.combinations = None
        tmp_list = [i for i in range(factor_num)]
        self.b_num = 1 + sum([len(list(combinations(tmp_list, i))) for i in range(1, factor_num + 1)])

        self.create_combinations()
        self.expand_plan_matrix()

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
        res = ""

        zeros = normalizer.zeros  # это кароч x^0 с фото
        intervals = normalizer.intervals  # это кароч дельта x с фото
        # тут лежат все возможные перестановки коэффицентов по 1, 2, 3 и тд, сеты с индексами например x1x2x3 = {0,1,2}
        coeff = [{x} for x in range(self.factor_num)] + [set(x) for x in self.combinations]
        # тоже самое листами, чтоб сохранить порядок при выводе
        combinations = [[x] for x in range(self.factor_num)] + [list(x) for x in self.combinations]

        # self.b_nat - натуральные кэфы
        # тут нулевой отдельно обсчитываем, это всё то, что без x на фото
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

        # перебор все комбинаций, т.е. все возможных членов, кроме свободного
        for i in range(len(combinations)):
            x_str = ''.join([self.alias[j] for j in combinations[i]])

            num = 0
            # фиксируем текущий, чтоб с i и j не путаться
            cur_coeff = coeff[i]
            # обход всех возможных кэфов
            for j in range(len(coeff)):
                # в коэфф вроде входят только члены, в которых есть сама переменная
                # ну тип для x1 это x1,x1x2, ..., x1x2x3 и тд
                # чтоб понять смотри на индексы при b на фото
                if cur_coeff.issubset(coeff[j]):
                    print(f'b{coeff[j]}={self.b[j + 1]}')
                    tmp = self.b[j + 1]
                    # b домнажается на все нули из комбинации, кроме нуля cur_coeff
                    for x in (coeff[j] - cur_coeff):
                        print(f'* x{x}={round(zeros[x], 4)} ', end='')
                        tmp *= zeros[x] * -1
                    print()
                    # b делится на все дельты
                    for x in coeff[j]:
                        print(f'/ x{x}={round(intervals[x], 4)} ', end='')
                        tmp /= intervals[x]
                    print()
                    # в кэф 1 взаимодействия входят с +, вторые с -, третьи с + и тд
                    # if (len(coeff[j]) - len(cur_coeff)) % 2 != 0:
                    #     print("----")
                    #     tmp *= -1

                    print(cur_coeff)
                    print(coeff[j])
                    print(f'tmp={tmp}')
                    print()

                    # ну суммируем с итоговым кэфом
                    # то есть цикл по j обсчитывает все числа внутри скобки
                    num += tmp

            print('==== ', str(num))
            print()

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
            # y_nat = sum(
            #     [(normalizer.denormalize(j - 1, self.matrix[i][j]) if j > 0 else self.matrix[i][j]) * self.b_nat[j]
            #      for j in range(self.b_num)]
            # )
            if abs(y_norm - y_nat) > eps:
                return False

        return True
