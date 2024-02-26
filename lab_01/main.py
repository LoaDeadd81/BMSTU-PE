import sys

from PyQt5.QtWidgets import QApplication

from smo.Distributions import Uniform
from smo.EventModel import EventList, run
from smo.Generator import Generator
from smo.Processor import InfQProcessor
from ui.LabWindow import LabWindow


def main():
    l = 50
    ld = 0
    mu = 50
    mud = 0
    mtime = 1000

    gen_distr = Uniform(l, ld)
    proc_distr = Uniform(mu, mud)

    gen = Generator(gen_distr)
    proc = InfQProcessor(proc_distr)

    gen.start()
    gen.add_proc(proc)

    elist = EventList()
    elist.push(gen)
    elist.push(proc)

    ftime = run(elist, mtime)

    q_avg = proc.stats.avg_q_time.avg()
    sys_avg = proc.stats.avg_elem_time.avg()
    ro = proc.stats.work_time / ftime
    print()


def main_ui():
    app = QApplication([])
    application = LabWindow()
    application.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main_ui()
