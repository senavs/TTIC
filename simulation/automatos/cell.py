from typing import Union

from simulation.core.condition import Condition, ConditionColor
from simulation.core.subject import Subject


class Cell:

    def __init__(self, x: int, y: int, subject: Subject):
        self.x, self.y = x, y
        self.subject = subject

    def draw(self) -> tuple[int, int, int]:
        return ConditionColor[self.subject.condition.value].value

    def __bool__(self):
        return self.subject.is_sick()

    def __eq__(self, other: Union['Cell', Subject, Condition]):
        if isinstance(other, Cell):
            return (self.subject.condition == other.subject.condition) and (self.x == other.x and self.y == other.y)
        elif isinstance(other, Subject):
            return self.subject.condition == other.condition
        return self.subject.condition == other

    def __repr__(self):
        return f'Cell({self.x}, {self.y}, {self.subject})'
