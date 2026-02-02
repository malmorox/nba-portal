from enum import Enum

class ChartType(str, Enum):
    BARH = "barh"
    LINE = "line"
    DONUT = "donut"