from enum import Enum


class Condition(Enum):
    NORMAL: str = 'NORMAL'
    EXPOSED: str = 'EXPOSED'
    INFECTIOUS: str = 'INFECTIOUS'
    HEALED: str = 'HEALED'
    DEAD: str = 'DEAD'


class ConditionColor(Enum):
    NORMAL: list = [255, 255, 255]
    EXPOSED: list = [255, 69, 0]
    INFECTIOUS: list = [139, 0, 0]
    HEALED: list = [0, 255, 0]
    DEAD: list = [0, 0, 0]
