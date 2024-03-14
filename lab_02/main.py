import sys

from PyQt5.QtWidgets import QApplication

from ui.LabWindow import LabWindow


def main_ui():
    app = QApplication([])
    application = LabWindow()
    application.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main_ui()
