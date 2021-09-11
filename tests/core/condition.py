import unittest

from simulation.core.condition import Condition, ConditionColor


class ConditionCase(unittest.TestCase):

    def setUp(self) -> None:
        self.conditions_names: list = []
        self.conditions_values: list = []

        for attr, value in Condition.__dict__.items():
            if not (attr.isupper() and attr.isalpha()):
                continue
            self.conditions_names.append(attr)
            self.conditions_values.append(value)

    def test_condition_attributes(self):
        self.assertEqual(len(self.conditions_names), 5)
        self.assertIn('NORMAL', self.conditions_names)
        self.assertIn('EXPOSED', self.conditions_names)
        self.assertIn('INFECTIOUS', self.conditions_names)
        self.assertIn('HEALED', self.conditions_names)
        self.assertIn('DEAD', self.conditions_names)

    def test_condition_values(self):
        self.assertEqual(len(self.conditions_names), 5)

        for name, value in zip(self.conditions_names, self.conditions_values):
            self.assertIsInstance(value, Condition)
            self.assertIsInstance(value.value, str)
            self.assertEqual(name, value.value)


class ConditionColorCase(unittest.TestCase):

    def setUp(self) -> None:
        self.conditions_names: list = []
        self.conditions_colors: list = []

        for attr, value in ConditionColor.__dict__.items():
            if not (attr.isupper() and attr.isalpha()):
                continue
            self.conditions_names.append(attr)
            self.conditions_colors.append(value)

    def test_condition_attributes(self):
        self.assertEqual(len(self.conditions_names), 5)
        self.assertIn('NORMAL', self.conditions_names)
        self.assertIn('EXPOSED', self.conditions_names)
        self.assertIn('INFECTIOUS', self.conditions_names)
        self.assertIn('HEALED', self.conditions_names)
        self.assertIn('DEAD', self.conditions_names)

    def test_condition_colors(self):
        self.assertEqual(len(self.conditions_names), 5)

        for condition, colors in zip(self.conditions_names, self.conditions_colors):
            self.assertIsInstance(colors, ConditionColor)
            self.assertIsInstance(colors.value, list)
            self.assertEqual(len(colors.value), 3)
            self.assertGreaterEqual(min(colors.value), 0)
            self.assertLessEqual(max(colors.value), 255)


if __name__ == '__main__':
    unittest.main()
