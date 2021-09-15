from enum import Enum


class Condition(Enum):
    NORMAL = 'NORMAL'
    EXPOSED = 'EXPOSED'
    INFECTIOUS = 'INFECTIOUS'
    HEALED = 'HEALED'
    DEAD = 'DEAD'


class ConditionColor(Enum):
    NORMAL = (255, 255, 255)
    EXPOSED = (255, 69, 0)
    INFECTIOUS = (139, 0, 0)
    HEALED = (0, 255, 0)
    DEAD = (0, 0, 0)
