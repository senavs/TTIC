from typing import Union

from simulation.core.condition import Condition
from simulation.core.subject import Subject


class Cell:

    def __init__(self, data: Subject):
        self.data = data

    def __bool__(self):
        return self.data.condition in (Condition.EXPOSED, Condition.INFECTIOUS)

    def __eq__(self, other: Union['Cell', Subject, Condition]):
        if isinstance(other, Cell):
            return self.data.condition == other.data.condition
        elif isinstance(other, Subject):
            return self.data.condition == other.condition
        return self.data.condition == other

    def __repr__(self):
        return f'Cell({self.data})'
