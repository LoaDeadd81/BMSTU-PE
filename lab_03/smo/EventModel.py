import heapq

from lab_03.smo.Element import Element


class EventList:
    def __init__(self):
        self.events = list()

    # def push(self, element: Element):
    #     heapq.heappush(self.events, element)
    #
    # def pop(self) -> Element:
    #     return heapq.heappop(self.events)

    def add(self, element: Element):
        self.events.append(element)

    def min(self) -> Element:
        return min(self.events)


def run(elist: EventList, mtime: float) -> float:
    ctime = 0

    while ctime < mtime:
        event = elist.min()
        # print(f"run poped ({type(event)}): {event.get_next_time()}")

        ctime = event.get_next_time()
        # print(f"run ctime: {ctime}")

        event.process()
        # elist.push(event)
        # print(f"run pushed ({type(event)}): {event.get_next_time()}")

    return ctime
