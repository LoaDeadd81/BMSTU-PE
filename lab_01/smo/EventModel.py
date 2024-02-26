import heapq

from smo.Element import Element


class EventList:
    def __init__(self):
        self.events = list()

    def push(self, element: Element):
        heapq.heappush(self.events, element)

    def pop(self) -> Element:
        return heapq.heappop(self.events)


def run(elist: EventList, mtime: float) -> float:
    ctime = 0

    while ctime < mtime:
        event = elist.pop()

        ctime = event.next_time

        event.process()
        elist.push(event)

    return ctime
