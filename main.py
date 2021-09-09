from pprint import pprint

from simulation.core.subject import Subject, Condition
from simulation.core.pathology import ConcretePathology

s1 = Subject()
s1.condition = Condition.EXPOSED
s1.pathology = ConcretePathology(s1)

s = [Subject() for _ in range(8)]

pprint(s1)
pprint(s)
print()
s1.agglomerate(s)

pprint(s1)
pprint(s)
