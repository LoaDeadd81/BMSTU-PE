class PFEData:
    def __init__(self):
        self.matrix = None
        self.y = None
        self.y_linear = None
        self.y_part_linear = None
        self.delta_linear = None
        self.delta_part_linear = None
        self.labels = None


class DFEData:
    def __init__(self):
        self.matrix = None
        self.y = None
        self.y_linear = None
        self.delta_linear = None
        self.labels = None


class OCKPData:
    def __init__(self):
        self.matrix = None
        self.y = None
        self.y_teor = None
        self.delta_y = None
        self.labels = None