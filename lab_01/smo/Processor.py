from abc import abstractmethod
from math import isinf
from queue import Queue

from smo.Distributions import Distribution
from smo.Element import Element


class Avg:
    def __init__(self):
        self.sum = 0
        self.n = 0

    def add(self, val: float):
        self.sum += val
        self.n += 1

    def avg(self) -> float:
        return self.sum / self.n

    def sum(self) -> float:
        return self.sum


class InfQProcessorStats:
    work_time: float = 0

    avg_elem_time: Avg = Avg()
    avg_elem_q: Queue = Queue()

    avg_q_time: Avg = Avg()
    avg_q_q: Queue = Queue()

    proc_num: int = 0
    req_num: int = 0

    def __init__(self):
        self.work_time = 0
        self.avg_elem_time = Avg()
        self.avg_elem_q = Queue()
        self.avg_q_time = Avg()
        self.avg_q_q = Queue()
        self.proc_num = 0
        self.req_num = 0


class Processor(Element):
    @abstractmethod
    def add_req(self, time: float) -> bool:
        pass


class InfQProcessor(Processor):

    def __init__(self, distr: Distribution):
        super().__init__()
        self.distr = distr

        self.q_len = 0
        self.stats = InfQProcessorStats()

    def process(self) -> bool:
        if self.q_len == 0:
            self.next_time = float('inf')
            return False

        self.start_work(self.next_time)
        return True

    def add_req(self, time: float) -> bool:
        self.q_len += 1

        self.stats.req_num += 1
        self.stats.avg_elem_q.put(time)
        self.stats.avg_q_q.put(time)

        if isinf(self.next_time):
            self.start_work(time)

        return True

    def start_work(self, time: float):
        proc_time = self.distr.generate()

        self.stats.avg_q_time.add(time - self.stats.avg_q_q.get())
        self.stats.avg_elem_time.add(time + proc_time - self.stats.avg_elem_q.get())
        self.stats.work_time += proc_time
        self.stats.proc_num += 1

        self.q_len -= 1
        self.next_time = time + proc_time

    def get_stats(self) -> InfQProcessorStats:
        return self.stats
