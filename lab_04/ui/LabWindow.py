from PyQt5.QtWidgets import QMainWindow, QMessageBox

from lab_04.fe.Normalizer import Normalizer
from lab_04.fe.LinearOCKP import LinearOCKP
from lab_04.smo.LabModel import SMOParam, runLabModel
from lab_04.ui.EData import OCKPData
from lab_04.ui.MainWindow import Ui_MainWindow
from lab_04.ui.OCKPWindow import OCKPWindow

FACTOR_NUM = 8
REPEAT_NUM = 20
# DFE_FACTORS = [1, 2, 3, 4, [1, 2, 3], [1, 2, 4], [2, 3, 4], [1, 3, 4]]
# DFE_FACTORS = [1, [1, 3, 5], 3, [1, 3, 7], 5, [3, 5, 7], 7, [1, 5, 7]]
DFE_FACTORS = [1, 2, 3, 4, 5, 6, [1, 2, 3, 4], [3, 4, 5, 6]]


class LabWindow(QMainWindow):
    def __init__(self):
        super(LabWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ockp = LinearOCKP(DFE_FACTORS)

        self.pfe_data = None
        self.dfe_data = None
        self.ockp_data = None

        self.ui.countPB.clicked.connect(self.count_ockp)
        self.ui.showPB.clicked.connect(self.show_ockp)

        self.ui.checkPB.clicked.connect(self.check)

    def count_ockp(self):
        try:
            matrix = self.ockp.get_matrix()
            y = self.get_y(matrix)

            self.ockp.count_b(y)

            y_linear = self.ockp.count_y()

            delta_linear = [abs(y[i] - y_linear[i]) for i in range(len(y))]

            self.ockp_data = OCKPData()
            self.ockp_data.matrix = matrix
            self.ockp_data.y = y
            self.ockp_data.y_teor = y_linear
            self.ockp_data.delta_y = delta_linear
            self.ockp_data.labels = self.ockp.get_alias()

            self.ui.alphaL.setText(str(round(self.ockp.get_alpha(), 4)))
            self.ui.SL.setText(str(round(self.ockp.get_S(), 4)))
            self.show_ockp_eq()

        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(e.__str__())
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def show_ockp_eq(self):
        normalizer = self.get_normalizer()
        self.ui.NormL.setText(self.ockp.get_norm_str())
        self.ui.NormSimL.setText(self.ockp.get_norm_similar_str())
        self.ui.NatL.setText(self.ockp.get_nature_str(normalizer))
        print(self.ockp.check(normalizer))

    def show_ockp(self):
        try:
            if self.ockp_data is None:
                raise Exception("Сначала нужно рассчитать")

            ockp_window = OCKPWindow(self, self.ockp_data)
            ockp_window.show()
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(e.__str__())
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def check(self):
        try:
            data = self.get_check_data()
            param = self.get_check_model_params(data)

            y_teor = self.ockp.get_y(data)
            y_exp = 0
            for i in range(REPEAT_NUM):
                y_exp += self.get_exp_check_y(param)
            y_exp /= REPEAT_NUM

            self.ui.checkResTeorL.setText('{:.4f}'.format(y_teor))
            self.ui.checkResExpL.setText('{:.4f}'.format(y_exp))
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(e.__str__())
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def get_y(self, matrix: list[list[float]]) -> list[float]:
        y = []
        params = self.get_model_params(matrix)

        for i in range(len(matrix)):
            tmp_y = 0

            for j in range(REPEAT_NUM):
                stats, time = runLabModel(params[i])
                tmp_y += stats.avg_elem_time.avg()

            y.append(tmp_y / REPEAT_NUM)

        return y

    def get_model_params(self, matrix: list[list[float]]) -> list[SMOParam]:
        res = []
        normalizer = self.get_normalizer()
        mtime = self.ui.mTimeSB.value()

        for i in range(len(matrix)):
            denorm_param = [normalizer.denormalize(j - 1, matrix[i][j]) for j in range(1, FACTOR_NUM + 1)]
            res.append(SMOParam(denorm_param, mtime))

        return res

    def get_normalizer(self) -> Normalizer:
        data = [
            [self.ui.x1MinSB.value(), self.ui.x1MaxSB.value()],
            [self.ui.x2MinSB.value(), self.ui.x2MaxSB.value()],
            [self.ui.x3MinSB.value(), self.ui.x3MaxSB.value()],
            [self.ui.x4MinSB.value(), self.ui.x4MaxSB.value()],
            [self.ui.x5MinSB.value(), self.ui.x5MaxSB.value()],
            [self.ui.x6MinSB.value(), self.ui.x6MaxSB.value()],
            [self.ui.x7MinSB.value(), self.ui.x7MaxSB.value()],
            [self.ui.x8MinSB.value(), self.ui.x8MaxSB.value()],
        ]
        return Normalizer(data)

    def get_check_data(self) -> list[float]:
        return [self.ui.x1CheckSB.value(),
                self.ui.x2CheckSB.value(),
                self.ui.x3CheckSB.value(),
                self.ui.x4CheckSB.value(),
                self.ui.x5CheckSB.value(),
                self.ui.x6CheckSB.value(),
                self.ui.x7CheckSB.value(),
                self.ui.x8CheckSB.value()]

    def get_check_model_params(self, data: list[float]) -> SMOParam:
        normalizer = self.get_normalizer()
        mtime = self.ui.mTimeSB.value()

        denorm_param = [normalizer.denormalize(i, data[i]) for i in range(len(data))]

        return SMOParam(denorm_param, mtime)

    def get_exp_check_y(self, param: SMOParam) -> float:
        res = 0

        for _ in range(REPEAT_NUM):
            stats, time = runLabModel(param)
            res += stats.avg_elem_time.avg()

        return res / REPEAT_NUM

