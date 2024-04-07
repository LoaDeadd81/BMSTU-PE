from abc import ABC, abstractmethod


class Element(ABC):
    def __init__(self):
        self.next_time = float('inf')

    @abstractmethod
    def process(self) -> bool:
        pass

    def get_next_time(self) -> float:
        return round(self.next_time, 5)

    def __lt__(self, other):
        return self.next_time < other.next_time
