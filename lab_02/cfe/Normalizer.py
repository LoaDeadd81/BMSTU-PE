class Normalizer:
    def __init__(self, data: list[list[float]]):
        self.data = data
        self.zeros = [(data[i][0] + data[i][1]) / 2 for i in range(len(data))]
        self.intervals = [(data[i][1] - data[i][0]) / 2 for i in range(len(data))]

    def normalize(self, i: int, value: float) -> float:
        return (value - self.zeros[i]) / self.intervals[i]

    def denormalize(self, i: int, value: float) -> float:
        return value * self.intervals[i] + self.zeros[i]
