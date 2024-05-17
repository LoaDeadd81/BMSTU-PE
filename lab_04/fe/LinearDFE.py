from lab_04.fe.LinearCFE import LinearCFE


class LinearDFE(LinearCFE):
    def __init__(self, data):
        self.dfe_data = data.copy()

        dct = {}
        combo_num = 0
        for i in range(len(data)):
            if isinstance(data[i], list):
                combo_num += 1
            else:
                dct[data[i]] = data[i] - combo_num

        super().__init__(len(data) - combo_num)

        for i in range(len(data)):
            if isinstance(data[i], list):
                for j in range(len(data[i])):
                    self.dfe_data[i][j] = dct[data[i][j]]

        self.expand_dfe_matrix()

        new_fn = len(data)
        self.factor_num = new_fn
        self.N = 2 ** (new_fn - combo_num)
        self.b_num = new_fn + 1

        super().create_alias()

    def expand_dfe_matrix(self):
        for i in range(len(self.matrix)):
            row = [1]
            mtr_j = 1
            for f_comb in self.dfe_data:
                res = 1

                if isinstance(f_comb, list):
                    for comb_val in f_comb:
                        res *= self.matrix[i][comb_val]
                else:
                    res *= self.matrix[i][mtr_j]
                    mtr_j += 1

                row.append(res)

            self.matrix[i] = row
