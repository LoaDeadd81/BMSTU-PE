from lab_04.smo.Distributions import Distribution


class Request:
    def __init__(self, distr: Distribution):
        self.distr = distr

    def get_proc_time(self) -> float:
        return self.distr.generate()


class RequestFabric:
    def __init__(self, distr: Distribution):
        self.distr = distr

    def create(self) -> Request:
        return Request(self.distr)
