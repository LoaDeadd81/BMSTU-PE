from lab_03.smo.Distributions import Uniform
from lab_03.smo.EventModel import EventList, run
from lab_03.smo.Generator import Generator
from lab_03.smo.Processor import InfQProcessor, InfQProcessorStats
from lab_03.smo.Request import RequestFabric


class SMOParam:
    lmbd: float
    lmbd_d: float
    mu: float
    mu_d: float

    lmbd_2: float
    lmbd_d_2: float
    mu_2: float
    mu_d_2: float

    mtime: float

    def __init__(self, params: list[float], mtime: float):
        self.lmbd = params[0]
        self.lmbd_d = params[1]
        self.mu = params[2]
        self.mu_d = params[3]

        self.lmbd_2 = params[4]
        self.lmbd_d_2 = params[5]
        self.mu_2 = params[6]
        self.mu_d_2 = params[7]

        self.mtime = mtime


def runLabModel(param: SMOParam) -> tuple[InfQProcessorStats, float]:
    elist = EventList()

    proc = InfQProcessor()
    elist.add(proc)

    fabric1 = RequestFabric(Uniform(param.mu, param.mu_d))
    gen1 = Generator("Generator_1", Uniform(param.lmbd, param.lmbd_d), fabric1)
    gen1.add_proc(proc)
    gen1.start()
    elist.add(gen1)

    fabric2 = RequestFabric(Uniform(param.mu_2, param.mu_d_2))
    gen2 = Generator("Generator_2", Uniform(param.lmbd_2, param.lmbd_d_2), fabric2)
    gen2.add_proc(proc)
    gen2.start()
    elist.add(gen2)

    ftime = run(elist, param.mtime)

    return proc.get_stats(), ftime
