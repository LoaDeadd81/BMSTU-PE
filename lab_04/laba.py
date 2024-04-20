import sys

from PyQt5.QtWidgets import QApplication

from lab_04.fe.LinearDFE import LinearDFE
from lab_04.fe.LinearOCKP import LinearOCKP
from ui.LabWindow import LabWindow


def main():
    # param = SMOParam([1, 0.1, 5, 0.1,
    #                   1, 0.1, 5, 0.1], 1000)
    # stats, time = runLabModel(param)
    # tm = stats.avg_elem_time.avg()
    # ro = stats.work_time / time

    # data = [1, 2, 3, 4, [1, 2, 3], [1, 2, 4], [2, 3, 4], [1, 3, 4]]
    data = [1, [1, 3, 5], 3, [1, 3, 7], 5, [3, 5, 7], 7, [1, 5, 7]]
    dfe = LinearDFE(data)
    mtr = dfe.get_matrix()

    ockp = LinearOCKP(data)
    mtr = ockp.get_matrix()
    print()


def main_ui():
    app = QApplication([])
    application = LabWindow()
    application.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main_ui()
    # main()
