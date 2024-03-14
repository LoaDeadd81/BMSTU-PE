from abc import ABC, abstractmethod

import numpy.random as nprand


class Distribution(ABC):
    @abstractmethod
    def generate(self) -> float:
        pass


class Uniform(Distribution):

    def __init__(self, mx: float, dx: float):
        # d = dx * sqrt(3)
        d = dx
        self.a = max(1 / mx - d, 0)
        self.b = 1 / mx + d

    def generate(self) -> float:
        return nprand.uniform(self.a, self.b)


class Exponential(Distribution):

    def __init__(self, mx: float, dx: float):
        self._lambda = mx

    def generate(self) -> float:
        return nprand.exponential(1 / self._lambda)
