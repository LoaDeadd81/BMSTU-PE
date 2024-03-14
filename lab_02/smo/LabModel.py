from lab_02.smo.Distributions import Uniform
from lab_02.smo.EventModel import EventList, run
from lab_02.smo.Generator import Generator
from lab_02.smo.Processor import InfQProcessor, InfQProcessorStats


class SMOParam:
    lmbd: float
    lmbd_d: float
    mu: float
    mu_d: float
    mtime: float

    def __init__(self, params: list[float], mtime: float):
        self.lmbd = params[0]
        self.lmbd_d = params[1]
        self.mu = params[2]
        self.mu_d = params[3]
        self.mtime = mtime


def runLab1Model(param: SMOParam) -> tuple[InfQProcessorStats, float]:
    gen = Generator(Uniform(param.lmbd, param.lmbd_d))
    proc = InfQProcessor(Uniform(param.mu, param.mu_d))

    gen.add_proc(proc)
    gen.start()

    elist = EventList()
    elist.push(gen)
    elist.push(proc)

    ftime = run(elist, param.mtime)

    return proc.get_stats(), ftime
