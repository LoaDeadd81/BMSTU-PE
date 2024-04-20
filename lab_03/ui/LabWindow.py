import multiprocessing as mp
import time as tm

from PyQt5.QtWidgets import QMainWindow, QMessageBox

from lab_03.fe.LinearCFE import LinearCFE
from lab_03.fe.LinearDFE import LinearDFE
from lab_03.fe.Normalizer import Normalizer
from lab_03.fe.PartLinearCFE import PartLinearCFE
from lab_03.smo.LabModel import SMOParam, runLabModel
from lab_03.ui.DFEWindow import DFEWindow
from lab_03.ui.MainWindow import Ui_MainWindow
from lab_03.ui.FEData import PFEData, DFEData
from lab_03.ui.PFEWindow import PFEWindow

FACTOR_NUM = 8
REPEAT_NUM = 10
# DFE_FACTORS = [1, 2, 3, 4, [1, 2, 3], [1, 2, 4], [2, 3, 4], [1, 3, 4]]
DFE_FACTORS = [1, [1, 3, 5], 3, [1, 3, 7], 5, [3, 5, 7], 7, [1, 5, 7]]


class LabWindow(QMainWindow):
    def __init__(self):
        super(LabWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.linearCFE = LinearCFE(FACTOR_NUM)
        self.partLinearCFE = PartLinearCFE(FACTOR_NUM)
        self.linearDFE = LinearDFE(DFE_FACTORS)

        self.pfe_data = None
        self.dfe_data = None

        self.ui.countPFEPB.clicked.connect(self.count_pfe)
        self.ui.showPFEPB.clicked.connect(self.show_pfe)

        self.ui.countDFEPB.clicked.connect(self.count_dfe)
        self.ui.showDFEPB.clicked.connect(self.show_dfe)

        self.ui.checkLinPB.clicked.connect(self.lin_check)
        self.ui.checkPartLinPB.clicked.connect(self.part_lin_check)

        self.ui.checkLinDFEPB.clicked.connect(self.dfe_check)

    def count_pfe(self):
        try:
            matrix = self.partLinearCFE.get_matrix()
            y = self.get_y_mp(matrix)

            self.linearCFE.count_b(y)
            self.partLinearCFE.count_b(y)

            y_linear = self.linearCFE.count_y()
            y_part_linear = self.partLinearCFE.count_y()

            delta_linear = [abs(y[i] - y_linear[i]) for i in range(len(y))]
            delta_part_linear = [abs(y[i] - y_part_linear[i]) for i in range(len(y))]

            self.pfe_data = PFEData()
            self.pfe_data.matrix = matrix
            self.pfe_data.y = y
            self.pfe_data.y_linear = y_linear
            self.pfe_data.y_part_linear = y_part_linear
            self.pfe_data.delta_linear = delta_linear
            self.pfe_data.delta_part_linear = delta_part_linear
            self.pfe_data.labels = self.partLinearCFE.get_alias()

            self.show_pfe_eq()

        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(e.__str__())
            msg.setWindowTitle("Ошибка")
            msg.exec_()


    def show_pfe_eq(self):
        normalizer = self.get_normalizer()
        self.ui.linNormL.setText(self.linearCFE.get_norm_str())
        self.ui.linDenormL.setText(self.linearCFE.get_nature_str(normalizer))
        print(self.linearCFE.check(normalizer))

        self.ui.partLinNormL.setText(self.partLinearCFE.get_norm_str())
        self.ui.partLinDenormL.setText(self.partLinearCFE.get_nature_str(normalizer))
        print(self.partLinearCFE.check(normalizer))

    def show_pfe(self):
        try:
            if self.pfe_data is None:
                raise Exception("Сначала нужно рассчитать ПФЭ")

            pfe_window = PFEWindow(self, self.pfe_data)
            pfe_window.show()
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(e.__str__())
            msg.setWindowTitle("Ошибка")
            msg.exec_()
    def count_dfe(self):
        try:
            matrix = self.linearDFE.get_matrix()
            y = self.get_y(matrix)

            self.linearDFE.count_b(y)

            y_linear = self.linearDFE.count_y()

            delta_linear = [abs(y[i] - y_linear[i]) for i in range(len(y))]

            self.dfe_data = DFEData()
            self.dfe_data.matrix = matrix
            self.dfe_data.y = y
            self.dfe_data.y_linear = y_linear
            self.dfe_data.delta_linear = delta_linear
            self.dfe_data.labels = self.linearDFE.get_alias()

            self.show_dfe_eq()

        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(e.__str__())
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def show_dfe_eq(self):
        normalizer = self.get_normalizer()
        self.ui.linNormDFEL.setText(self.linearDFE.get_norm_str())
        self.ui.linDenormDFEL.setText(self.linearDFE.get_nature_str(normalizer))


    def show_dfe(self):
        try:
            if self.dfe_data is None:
                raise Exception("Сначала нужно рассчитать ДФЭ")

            pfe_window = DFEWindow(self, self.dfe_data)
            pfe_window.show()
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(e.__str__())
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def lin_check(self):
        try:
            data = self.get_check_data()
            param = self.get_check_model_params(data)

            y_teor = self.linearCFE.get_y(data)
            y_exp = self.get_exp_check_y(param)

            self.ui.checkResTeorL.setText('{:.4f}'.format(y_teor))
            self.ui.checkResExpL.setText('{:.4f}'.format(y_exp))
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(e.__str__())
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def part_lin_check(self):
        try:
            data = self.get_check_data()
            param = self.get_check_model_params(data)

            y_teor = self.partLinearCFE.get_y(data)
            y_exp = self.get_exp_check_y(param)

            self.ui.checkResTeorL.setText('{:.4f}'.format(y_teor))
            self.ui.checkResExpL.setText('{:.4f}'.format(y_exp))
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText(e.__str__())
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def dfe_check(self):
        try:
            data = self.get_check_data()
            param = self.get_check_model_params(data)

            y_teor = self.linearDFE.get_y(data)
            y_exp = self.get_exp_check_y(param)

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

    def get_y_mp(self, matrix: list[list[float]]) -> list[float]:
        # start = tm.time()
        # y = []
        # params = self.get_model_params(matrix)
        #
        # # max_pb = len(matrix) * REPEAT_NUM
        # # cur_pb = 0
        # # self.ui.progressBarPFE.setValue(cur_pb)
        #
        # for i in range(len(matrix)):
        #     tmp_y = 0
        #
        #     for j in range(REPEAT_NUM):
        #         stats, time = runLabModel(params[i])
        #         tmp_y += stats.avg_elem_time.avg()
        #
        #         # cur_pb = i * REPEAT_NUM + j
        #         # self.ui.progressBarPFE.setValue(int(cur_pb / max_pb * 90))
        #
        #     y.append(tmp_y / REPEAT_NUM)
        #
        # end = tm.time()
        # print(end - start)
        #
        # return y

        start = tm.time()
        params = self.get_model_params(matrix)
        y = mp.Array('f', [0.0] * len(matrix))

        p_num = 8
        step = 32
        ranges = [[i * step, (i + 1) * step] for i in range(8)]
        processes = [mp.Process(target=count_y, args=(params, ranges[i][0], ranges[i][1], y)) for i in range(p_num)]

        for process in processes:
            process.start()

        for process in processes:
            process.join()

        end = tm.time()
        print(end - start)

        return y[:]

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


def count_y(params: list[SMOParam], l: int, r: int, y: list[float]):
    for i in range(l, r):
        tmp_y = 0

        for _ in range(REPEAT_NUM):
            stats, time = runLabModel(params[i])
            tmp_y += stats.avg_elem_time.avg()

        y[i] = tmp_y / REPEAT_NUM
