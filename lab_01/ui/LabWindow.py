import pyqtgraph as pg
from PyQt5.QtWidgets import QMainWindow

from smo.LabModel import SMOParam, runLab1Model
from smo.Processor import InfQProcessorStats
from ui.MainWindow import Ui_MainWindow


class LabWindow(QMainWindow):
    def __init__(self):
        super(LabWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.modelPB.clicked.connect(self.model)
        self.ui.lambdaGraphPB.clicked.connect(self.lambda_graph)
        self.ui.muGraphPB.clicked.connect(self.mu_graph)
        self.ui.roGraphPB.clicked.connect(self.ro_graph)

    def model(self):
        param = self.get_smo_param()

        proc_stat, ftime = runLab1Model(param)

        self.set_exp_res(param)
        self.set_fact_res(proc_stat, ftime)

    def lambda_graph(self):
        lmbd_l = 1
        lmbd_r = 10
        lmbd_step = 0.1
        lmbd_d = 0.1
        mu = 10
        mu_d = 0.1
        mtime = 100
        cnt = 100
        param = SMOParam(lmbd=0, lmbd_d=lmbd_d, mu=mu, mu_d=mu_d, mtime=mtime)

        x = []
        y = []
        lmbd = lmbd_l
        while lmbd < lmbd_r:
            param.lmbd = lmbd

            res = []
            for i in range(cnt):
                proc_stat, ftime = runLab1Model(param)
                res.append(proc_stat.avg_elem_time.avg())

            print(lmbd / lmbd_r)
            x.append(lmbd)
            y.append(sum(res) / len(res))
            lmbd += lmbd_step

        window = pg.plot(x, y,
                         title=f"Зависимость среднего времени пребывания в системе от интенсивности поступления (µ = {mu})")
        window.setGeometry(100, 100, 800, 600)
        plot_widget = window.getPlotItem()
        labelStyle = {'color': '#FFF', 'font-size': '16pt'}
        plot_widget.getAxis('left').setLabel('Среднеее временя пребывания заявки в системе', **labelStyle)
        plot_widget.getAxis('bottom').setLabel('Интенсивность поступления заявок λ', **labelStyle)


    def mu_graph(self):
        mu_l = 1
        mu_r = 10
        mu_step = 0.1
        mu_d = 0.5
        lmbd = 10
        lmbd_d = 0.1
        mtime = 100
        cnt = 150
        param = SMOParam(lmbd=lmbd, lmbd_d=lmbd_d, mu=0, mu_d=mu_d, mtime=mtime)

        x = []
        y = []
        mu = mu_l
        while mu < mu_r:
            param.mu = mu

            res = []
            for i in range(cnt):
                proc_stat, ftime = runLab1Model(param)
                res.append(proc_stat.avg_elem_time.avg())

            print(mu / mu_r)
            x.append(mu)
            y.append(sum(res) / len(res))
            mu += mu_step

        window = pg.plot(x, y,
                         title=f"Зависимость среднего времени пребывания в системе от интенсивности обслуживания (λ = {lmbd})")
        window.setGeometry(100, 100, 800, 600)
        plot_widget = window.getPlotItem()
        labelStyle = {'color': '#FFF', 'font-size': '16pt'}
        plot_widget.getAxis('left').setLabel('Среднеее временя пребывания заявки в системе', **labelStyle)
        plot_widget.getAxis('bottom').setLabel('Интенсивность обслуживания заявок µ', **labelStyle)

    def ro_graph(self):
        lmbd_step = 0.1
        lmbd_l = lmbd_step
        lmbd_r = 10 + lmbd_step
        lmbd_d = 0.1
        mu = 10
        mu_d = 0.1
        mtime = 100
        cnt = 100
        param = SMOParam(lmbd=0, lmbd_d=lmbd_d, mu=mu, mu_d=mu_d, mtime=mtime)

        x = []
        y = []
        lmbd = lmbd_l
        while lmbd < lmbd_r:
            param.lmbd = lmbd

            res = []
            for i in range(cnt):
                proc_stat, ftime = runLab1Model(param)
                res.append(proc_stat.avg_elem_time.avg())

            print(lmbd / lmbd_r)
            x.append(lmbd / mu)
            y.append(sum(res) / len(res))
            lmbd += lmbd_step

        window = pg.plot(x, y,
                         title=f"Зависимость среднего времени пребывания в системе от загрузки системы ρ (µ = {mu}, λ = ({lmbd_l - lmbd_step}, {lmbd_r - lmbd_step})")
        window.setGeometry(100, 100, 800, 600)
        plot_widget = window.getPlotItem()
        labelStyle = {'color': '#FFF', 'font-size': '16pt'}
        plot_widget.getAxis('left').setLabel('Среднеее временя пребывания заявки в системе', **labelStyle)
        plot_widget.getAxis('bottom').setLabel('Загрузка системы ρ', **labelStyle)

    def get_smo_param(self):
        return SMOParam(lmbd=self.ui.lambdaSP.value(), lmbd_d=self.ui.labdaDeltaSP.value(), mu=self.ui.muSP.value(),
                        mu_d=self.ui.muDeltaSp.value(), mtime=self.ui.mtineSP.value())

    def set_exp_res(self, param: SMOParam):
        ro = param.lmbd / param.mu
        proc_num = param.mtime * min(param.lmbd, param.mu)
        if ro <= 1:
            avg_sys_t = 1 / param.mu
        # elif param.mu < 1:
        #     avg_sys_t = (proc_num + ro - proc_num * ro + 1) / (2 * param.mu)
        else:
            tmp_ro = 1 / ro
            avg_sys_t = (proc_num + tmp_ro - proc_num * tmp_ro + 1) / 2

        self.ui.loadExpL.setText(str(round(ro, 2)))
        self.ui.avgTExpL.setText(str(round(avg_sys_t, 2)))
        self.ui.rExpL.setText(str(round(proc_num, 2)))

    def set_fact_res(self, proc_stat: InfQProcessorStats, ftime: float):
        ro = proc_stat.work_time / ftime
        avg_sys_t = proc_stat.avg_elem_time.avg()
        proc_num = proc_stat.proc_num

        self.ui.loadFactL.setText(str(round(ro, 2)))
        self.ui.avgTFactL.setText(str(round(avg_sys_t, 2)))
        self.ui.rFactL.setText(str(round(proc_num, 2)))
