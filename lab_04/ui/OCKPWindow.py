from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

from lab_04.ui.EData import OCKPData
from lab_04.ui.PFEGenWindow import Ui_PFEWindowGen


class OCKPWindow(QMainWindow):
    def __init__(self, parent, data: OCKPData):
        super(OCKPWindow, self).__init__(parent)
        self.ui = Ui_PFEWindowGen()
        self.ui.setupUi(self)

        self.ockp_data = data

        self.show_ockp()

    def show_ockp(self):
        round_num = 2

        self.ui.expMtrTW.clearContents()

        self.ui.expMtrTW.setRowCount(len(self.ockp_data.matrix))

        labels = ["x0"] + self.ockp_data.labels + ["y", "y_т", "|y - y_т|"]
        self.ui.expMtrTW.setColumnCount(len(labels))
        self.ui.expMtrTW.setHorizontalHeaderLabels(labels)

        for i in range(len(self.ockp_data.matrix)):
            for j in range(len(self.ockp_data.matrix[0])):
                self.ui.expMtrTW.setItem(len(self.ockp_data.matrix) - i - 1, j,
                                         QTableWidgetItem(str(round(self.ockp_data.matrix[i][j], round_num))))

        offset = len(self.ockp_data.matrix[0])
        for i in range(len(self.ockp_data.matrix)):
            self.ui.expMtrTW.setItem(len(self.ockp_data.matrix) - i - 1, offset, QTableWidgetItem(str(
                round(self.ockp_data.y[i], round_num)
            )))

        offset += 1
        for i in range(len(self.ockp_data.matrix)):
            self.ui.expMtrTW.setItem(len(self.ockp_data.matrix) - i - 1, offset, QTableWidgetItem(str(
                round(self.ockp_data.y_teor[i], round_num)
            )))
        offset += 1
        for i in range(len(self.ockp_data.matrix)):
            self.ui.expMtrTW.setItem(len(self.ockp_data.matrix) - i - 1, offset, QTableWidgetItem(str(
                round(self.ockp_data.delta_y[i], round_num)
            )))

        print(sum(self.ockp_data.delta_y) / len(self.ockp_data.delta_y))
