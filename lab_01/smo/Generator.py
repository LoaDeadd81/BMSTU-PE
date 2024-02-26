from smo.Distributions import Distribution
from smo.Element import Element
from smo.Processor import Processor


class GeneratorStats:
    r_gen: int = 0
    r_den: int = 0


class Generator(Element):
    def __init__(self, distr: Distribution):
        super().__init__()
        self.distr = distr

        self.r_list = list()
        self.stats = GeneratorStats()

    def process(self) -> bool:
        t = self.next_time
        self.next_time += self.distr.generate()
        self.stats.r_gen += 1

        for i in self.r_list:
            if i.add_req(t):
                return True

        self.stats.r_den += 1
        return False

    def start(self):
        self.next_time = self.distr.generate()

    def add_proc(self, proc: Processor):
        self.r_list.append(proc)

    def get_stats(self) -> GeneratorStats:
        return self.stats
