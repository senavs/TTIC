import unittest

from simulation.core.condition import Condition
from simulation.core.pathology import ConcretePathology, NullPathology
from simulation.core.subject import Subject
from simulation.settings import SubjectSettings


class SubjectCase(unittest.TestCase):

    def setUp(self) -> None:
        self.subject1 = Subject()
        self.subject2 = Subject()
        self.exposed_subject = Subject.create_sick_subject()
        self.infectious_subject = Subject.create_sick_subject(Condition.INFECTIOUS)

    def test_subject_id(self):
        self.assertIsInstance(self.subject1.id, int)
        self.assertEqual(self.subject2.id - self.subject1.id, 1)
        self.assertGreater(self.subject2.id, self.subject1.id)

    def test_subject_age(self):
        self.assertGreaterEqual(self.subject1.age, SubjectSettings.MIN_AGE)
        self.assertLessEqual(self.subject1.age, SubjectSettings.MAX_AGE)

    def test_subject_condition(self):
        subject = Subject()
        subject.condition = Condition.DEAD

        self.assertEqual(self.subject1.condition, Condition.NORMAL)
        self.assertEqual(self.exposed_subject.condition, Condition.EXPOSED)
        self.assertEqual(self.infectious_subject.condition, Condition.INFECTIOUS)
        self.assertEqual(subject.condition, Condition.DEAD)

    def test_subject_pathology(self):
        self.assertIsInstance(self.subject1.pathology, NullPathology)
        self.assertIsInstance(self.exposed_subject.pathology, ConcretePathology)

    def test_subject_healthy_lifestyle(self):
        self.assertIsInstance(self.subject1.healthy_lifestyle, float)
        self.assertGreaterEqual(self.subject1.healthy_lifestyle, 0)
        self.assertLessEqual(self.subject1.healthy_lifestyle, 1)


if __name__ == '__main__':
    unittest.main()
