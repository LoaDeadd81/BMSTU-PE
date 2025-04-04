from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox

from lab_02.cfe.LinearCFE import LinearCFE
from lab_02.cfe.Normalizer import Normalizer
from lab_02.cfe.PartLinearCFE import PartLinearCFE
from lab_02.smo.LabModel import SMOParam, runLab1Model
from lab_02.ui.MainWindow import Ui_MainWindow

FACTOR_NUM = 4
REPEAT_NUM = 20


class LabWindow(QMainWindow):
    def __init__(self):
        super(LabWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.linearCFE = LinearCFE(FACTOR_NUM)
        self.partLinearCFE = PartLinearCFE(FACTOR_NUM)

        self.ui.countPB.clicked.connect(self.count)
        self.ui.checkLinPB.clicked.connect(self.lin_check)
        self.ui.checkPartLinPB.clicked.connect(self.part_lin_check)

    def count(self):
        try:
            matrix = self.partLinearCFE.get_matrix()
            y = self.get_y(matrix)

            self.linearCFE.count_b(y)
            self.partLinearCFE.count_b(y)

            y_linear = self.linearCFE.count_y()
            y_part_linear = self.partLinearCFE.count_y()

            delta_linear = [abs(y[i] - y_linear[i]) for i in range(len(y))]
            delta_part_linear = [abs(y[i] - y_part_linear[i]) for i in range(len(y))]

            self.ui.expMtrTW.clearContents()
            self.ui.expMtrTW.setRowCount(len(matrix))
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    self.ui.expMtrTW.setItem(len(matrix) - i - 1, j, QTableWidgetItem(str(matrix[i][j])))

            offset = len(matrix[0])
            for i in range(len(matrix)):
                self.ui.expMtrTW.setItem(len(matrix) - i - 1, offset, QTableWidgetItem(str(
                    round(y[i], 2)
                )))

            offset += 1
            for i in range(len(matrix)):
                self.ui.expMtrTW.setItem(len(matrix) - i - 1, offset, QTableWidgetItem(str(
                    round(y_linear[i], 2)
                )))
            offset += 1
            for i in range(len(matrix)):
                self.ui.expMtrTW.setItem(len(matrix) - i - 1, offset, QTableWidgetItem(str(
                    round(y_part_linear[i], 2)
                )))

            offset += 1
            for i in range(len(matrix)):
                self.ui.expMtrTW.setItem(len(matrix) - i - 1, offset, QTableWidgetItem(str(
                    round(delta_linear[i], 2)
                )))
            offset += 1
            for i in range(len(matrix)):
                self.ui.expMtrTW.setItem(len(matrix) - i - 1, offset, QTableWidgetItem(str(
                    round(delta_part_linear[i], 2)
                )))

            normalizer = self.get_normalizer()
            self.ui.linNormL.setText(self.linearCFE.get_norm_str())
            self.ui.linDenormL.setText(self.linearCFE.get_nature_str(normalizer))
            check_res = self.linearCFE.check(normalizer)
            if not check_res:
                raise Exception("Линейная не прошла проверку")

            self.ui.partLinNormL.setText(self.partLinearCFE.get_norm_str())
            self.ui.partLinDenormL.setText(self.partLinearCFE.get_nature_str(normalizer))
            check_res = self.partLinearCFE.check(normalizer)
            if not check_res:
                raise Exception("Линейная не прошла проверку")

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

            self.ui.checkResTeorL.setText(str(round(y_teor, 2)))
            self.ui.checkResExpL.setText(str(round(y_exp, 2)))
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

            self.ui.checkResTeorL.setText(str(round(y_teor, 2)))
            self.ui.checkResExpL.setText(str(round(y_exp, 2)))
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

            for _ in range(REPEAT_NUM):
                stats, time = runLab1Model(params[i])
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
        ]
        return Normalizer(data)

    def get_check_data(self) -> list[float]:
        return [self.ui.x1CheckSB.value(),
                self.ui.x2CheckSB.value(),
                self.ui.x3CheckSB.value(),
                self.ui.x4CheckSB.value()]

    def get_check_model_params(self, data: list[float]) -> SMOParam:
        normalizer = self.get_normalizer()
        mtime = self.ui.mTimeSB.value()

        denorm_param = [normalizer.denormalize(i, data[i]) for i in range(len(data))]

        return SMOParam(denorm_param, mtime)

    def get_exp_check_y(self, param: SMOParam) -> float:
        res = 0

        for _ in range(REPEAT_NUM):
            stats, time = runLab1Model(param)
            res += stats.avg_elem_time.avg()

        return res / REPEAT_NUM
