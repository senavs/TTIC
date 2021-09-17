from abc import ABC, abstractmethod
from functools import reduce
from operator import mul
from typing import TYPE_CHECKING, Type

from simulation.settings import PreventionSettings, SubjectSettings

if TYPE_CHECKING:
    from simulation.core.subject import Subject


class PreventionGroup:

    def __init__(self, subject: 'Subject', *preventions: Type['Prevention']):
        self.preventions = [prevention(subject) for prevention in preventions]
        self.subject = subject

    def get_prob_infection(self) -> float:
        if not self.preventions:
            return 1
        return reduce(mul, (prevention.prob_infection if prevention.is_activated else 1
                            for prevention in self.preventions))

    def get_prob_death(self) -> float:
        if not self.preventions:
            return 1
        return reduce(mul, (prevention.prob_death if prevention.is_activated else 1
                            for prevention in self.preventions))

    def evolve(self):
        for prevention in self.preventions:
            prevention.evolve()


class Prevention(ABC):
    is_activated = False

    def __init__(self, subject: 'Subject', prob_infection: float = None, prob_death: float = None):
        self.prevented_days = 0

        self.prob_infection = prob_infection
        self.prob_death = prob_death
        self.subject = subject

    @classmethod
    def activate(cls):
        cls.is_activated = True

    @classmethod
    def deactivate(cls):
        cls.is_activated = False

    def increase(self):
        self.prevented_days += 1

    @abstractmethod
    def evolve(self):
        pass


class SocialIsolation(Prevention):

    def __init__(self, subject: 'Subject'):
        super().__init__(
            subject,
            PreventionSettings.ISOLATION_PROB_INFECTION,
            PreventionSettings.ISOLATION_PROB_DEATH
        )

    def evolve(self):
        self.increase()


class Mask(Prevention):

    def __init__(self, subject: 'Subject'):
        super().__init__(
            subject,
            PreventionSettings.MASK_PROB_INFECTION,
            PreventionSettings.MASK_PROB_DEATH
        )

    def evolve(self):
        self.increase()


class Vaccine(Prevention):

    def __init__(self, subject: 'Subject'):
        super().__init__(
            subject,
            PreventionSettings.VACCINE_PROB_INFECTION,
            PreventionSettings.VACCINE_PROB_DEATH
        )

    def evolve(self):
        self.increase()
        # if not self.is_activated:
        #     return
        #
        # if -self.prevented_days % SubjectSettings.MAX_AGE >= self.subject.age:
        #     pass
