import random
from itertools import count

from simulation.core.pathology import Pathology, NullPathology
from simulation.settings import SubjectSettings
from simulation.core.condition import Condition

_instance_counter = count(1)


class Subject:

    def __init__(self):
        self.id: int = next(_instance_counter)
        self.age: int = random.randint(SubjectSettings.MIN_AGE, SubjectSettings.MAX_AGE + 1)
        self.condition: Condition = Condition.NORMAL
        self.pathology: Pathology = NullPathology(self)
        self.healthy_lifestyle: float = random.random()

    def agglomerate(self, subjects: list['Subject']):
        for subject in subjects:
            self.pathology.infect(subject)

    def __repr__(self):
        return f'Subject({self.id}, {self.age}, {self.healthy_lifestyle:.2f}, {self.pathology})'
