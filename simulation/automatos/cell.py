from typing import Union

from simulation.core.condition import Condition, ConditionColor
from simulation.core.subject import Subject


class Cell:

    def __init__(self, x: int, y: int, data: Subject):
        self.x, self.y = x, y
        self.data = data

    def draw(self) -> tuple[int, int, int]:
        return ConditionColor[self.data.condition.value].value

    def __bool__(self):
        return self.data.is_sick()

    def __eq__(self, other: Union['Cell', Subject, Condition]):
        if isinstance(other, Cell):
            return self.data.condition == other.data.condition
        elif isinstance(other, Subject):
            return self.data.condition == other.condition
        return self.data.condition == other

    def __repr__(self):
        return f'Cell({self.x}, {self.y}, {self.data})'
