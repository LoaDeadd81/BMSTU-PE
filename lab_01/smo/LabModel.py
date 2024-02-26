from smo.Distributions import Uniform, Exponential
from smo.EventModel import EventList, run
from smo.Generator import Generator
from smo.Processor import InfQProcessor, InfQProcessorStats


class SMOParam:
    lmbd: float
    lmbd_d: float
    mu: float
    mu_d: float
    mtime: float

    def __init__(self, lmbd: float, lmbd_d: float, mu: float, mu_d: float, mtime: float):
        self.lmbd = lmbd
        self.lmbd_d = lmbd_d
        self.mu = mu
        self.mu_d = mu_d
        self.mtime = mtime


def runLab1Model(param: SMOParam) -> tuple[InfQProcessorStats, float]:
    gen = Generator(Uniform(param.lmbd, param.lmbd_d))
    proc = InfQProcessor(Uniform(param.mu, param.mu_d))

    # gen = Generator(Exponential(param.lmbd, param.lmbd_d))
    # proc = InfQProcessor(Exponential(param.mu, param.mu_d))

    gen.add_proc(proc)
    gen.start()

    elist = EventList()
    elist.push(gen)
    elist.push(proc)

    ftime = run(elist, param.mtime)

    return proc.get_stats(), ftime
