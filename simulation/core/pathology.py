import random
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from simulation.settings import subject_settings, pathology_settings
from simulation.core.condition import Condition

if TYPE_CHECKING:
    from simulation.core.subject import Subject


class Pathology(ABC):

    def __init__(self, subject: 'Subject'):
        self.infected_days: int = 0
        self.subject = subject

        self.prob_infection: float = pathology_settings.PROB_INFECTION
        self.prob_death: float = pathology_settings.PROB_DEATH
        self.exposed_max_day: float = pathology_settings.EXPOSED_MAX_DAY
        self.infectious_max_day: float = pathology_settings.INFECTIOUS_MAX_DAY

    @abstractmethod
    def infect(self, subject: 'Subject') -> bool:
        pass

    @abstractmethod
    def kill(self) -> bool:
        pass

    @abstractmethod
    def evolve(self):
        pass

    def __repr__(self):
        return f'{self.__class__.__name__}({self.infected_days})'


class NullPathology(Pathology):

    def infect(self, subject: 'Subject') -> bool:
        return False

    def kill(self) -> bool:
        return False

    def evolve(self):
        pass


class ConcretePathology(Pathology):

    def increase_infected_days(self):
        self.infected_days += 1

    def infect(self, subject: 'Subject') -> bool:
        if not self.should_infect(subject):
            return False

        subject.condition = Condition.EXPOSED
        subject.pathology = ConcretePathology(subject)
        return True

    def should_infect(self, subject: 'Subject') -> bool:
        # TODO: it has to consider prevention probs
        if self.subject.condition not in (Condition.EXPOSED, Condition.INFECTIOUS):
            return False
        if subject.condition != Condition.NORMAL:
            return False

        return random.random() <= self.prob_infection * self.subject.preventions.get_prob_infection()

    def kill(self) -> bool:
        if not self.should_kill():
            return False

        self.subject.condition = Condition.DEAD
        return True

    def should_kill(self) -> bool:
        if self.subject.condition not in (Condition.EXPOSED, Condition.INFECTIOUS):
            return False

        prob = (self.prob_death * (self.subject.age / subject_settings.MAX_AGE)) / self.subject.healthy_lifestyle * self.subject.preventions.get_prob_death()
        return random.random() <= prob

    def evolve(self):
        self.increase_infected_days()

        if self.infected_days < self.exposed_max_day:
            return

        if self.subject.condition == Condition.EXPOSED and self.infected_days > self.exposed_max_day:
            self.subject.condition = Condition.INFECTIOUS
        elif self.subject.condition == Condition.INFECTIOUS and (self.infected_days - self.exposed_max_day) > self.infectious_max_day:
            self.subject.condition = Condition.HEALED

        self.kill()
