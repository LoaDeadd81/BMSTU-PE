from lab_03.smo.Distributions import Distribution
from lab_03.smo.Element import Element
from lab_03.smo.Processor import Processor
from lab_03.smo.Request import RequestFabric


class GeneratorStats:
    r_gen: int = 0
    r_den: int = 0


class Generator(Element):
    def __init__(self, name, distr: Distribution, req_fabric: RequestFabric):
        super().__init__()
        self.name = name
        self.distr = distr
        self.fabric = req_fabric

        self.r_list = list()
        self.stats = GeneratorStats()

    def process(self) -> bool:
        t = self.next_time
        self.next_time += self.distr.generate()
        self.stats.r_gen += 1

        req = self.fabric.create()
        for i in self.r_list:
            if i.add_req(t, req):
                return True

        self.stats.r_den += 1
        return False

    def start(self):
        self.next_time = self.distr.generate()

    def add_proc(self, proc: Processor):
        self.r_list.append(proc)

    def get_stats(self) -> GeneratorStats:
        return self.stats
