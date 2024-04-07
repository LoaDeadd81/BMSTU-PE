from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

from lab_03.ui.FEData import PFEData
from lab_03.ui.PFEGenWindow import Ui_PFEWindowGen


class PFEWindow(QMainWindow):
    def __init__(self, parent, data: PFEData):
        super(PFEWindow, self).__init__(parent)
        self.ui = Ui_PFEWindowGen()
        self.ui.setupUi(self)

        self.pfe_data = data

        self.show_pfe()

    def show_pfe(self):
        self.ui.expMtrTW.clearContents()

        self.ui.expMtrTW.setRowCount(len(self.pfe_data.matrix))

        labels = ["x0"] + self.pfe_data.labels + ["y", "y_л", "y_чл", "|y - y_л|", "|y - y_чл|"]
        self.ui.expMtrTW.setColumnCount(len(labels))
        self.ui.expMtrTW.setHorizontalHeaderLabels(labels)

        for i in range(len(self.pfe_data.matrix)):
            for j in range(len(self.pfe_data.matrix[0])):
                self.ui.expMtrTW.setItem(len(self.pfe_data.matrix) - i - 1, j,
                                         QTableWidgetItem(str(self.pfe_data.matrix[i][j])))

        offset = len(self.pfe_data.matrix[0])
        for i in range(len(self.pfe_data.matrix)):
            self.ui.expMtrTW.setItem(len(self.pfe_data.matrix) - i - 1, offset, QTableWidgetItem(str(
                round(self.pfe_data.y[i], 2)
            )))

        offset += 1
        for i in range(len(self.pfe_data.matrix)):
            self.ui.expMtrTW.setItem(len(self.pfe_data.matrix) - i - 1, offset, QTableWidgetItem(str(
                round(self.pfe_data.y_linear[i], 2)
            )))
        offset += 1
        for i in range(len(self.pfe_data.matrix)):
            self.ui.expMtrTW.setItem(len(self.pfe_data.matrix) - i - 1, offset, QTableWidgetItem(str(
                round(self.pfe_data.y_part_linear[i], 2)
            )))

        offset += 1
        for i in range(len(self.pfe_data.matrix)):
            self.ui.expMtrTW.setItem(len(self.pfe_data.matrix) - i - 1, offset, QTableWidgetItem(str(
                round(self.pfe_data.delta_linear[i], 2)
            )))
        offset += 1
        for i in range(len(self.pfe_data.matrix)):
            self.ui.expMtrTW.setItem(len(self.pfe_data.matrix) - i - 1, offset, QTableWidgetItem(str(
                round(self.pfe_data.delta_part_linear[i], 2)
            )))