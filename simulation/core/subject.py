import random
from itertools import count

from simulation.core.pathology import ConcretePathology, Pathology, NullPathology
from simulation.core.condition import Condition
from simulation.core.prevention import PreventionGroup, SocialIsolation, Mask, Vaccine
from simulation.settings import SubjectSettings


class Subject:

    def __new__(cls):
        if not getattr(cls, '_icounter', None):
            cls._icounter = count(1)
        return object.__new__(cls)

    def __init__(self):
        self.id: int = next(self._icounter)
        self.age: int = random.randint(SubjectSettings.MIN_AGE, SubjectSettings.MAX_AGE + 1)
        self.condition: Condition = Condition.NORMAL
        self.pathology: Pathology = NullPathology(self)
        self.preventions: PreventionGroup = PreventionGroup(self)
        self.healthy_lifestyle: float = random.random()

    def agglomerate(self, subjects: list['Subject']):
        for subject in subjects:
            self.pathology.infect(subject)

    def is_sick(self) -> bool:
        return self.condition in (Condition.EXPOSED, Condition.INFECTIOUS)

    @classmethod
    def create_sick_subject(cls, condition: Condition = Condition.EXPOSED) -> 'Subject':
        subject = Subject()
        subject.condition = condition
        subject.pathology = ConcretePathology(subject)
        return subject

    def __repr__(self):
        return f'Subject({self.id}, {self.age}, {self.healthy_lifestyle:.2f}, {self.pathology})'
