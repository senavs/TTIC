import argparse

from simulation.settings import SIMULATION_UUID
from simulation.automatos.progress import Progress
from simulation.core.prevention import SocialIsolation, Mask, Vaccine
from simulation.core.subject import Subject

PREVENTIONS = {
    'isolation': SocialIsolation,
    'mask': Mask,
    'vaccine': Vaccine
}

parser = argparse.ArgumentParser(description='Spread disease simulation')
parser.add_argument('--isolation', '-i', dest='isolation', action='store_true')
parser.add_argument('--mask', '-m', dest='mask', action='store_true')
parser.add_argument('--vaccine', '-v', dest='vaccine', action='store_true')

args = parser.parse_args()

if __name__ == '__main__':
    preventions_names = []
    selected_preventions = []

    for flag, value in args.__dict__.items():
        if not value:
            continue
        preventions_names.append(flag)
        selected_preventions.append(PREVENTIONS[flag])

    Subject.set_preventions(selected_preventions)

    print(f'{SIMULATION_UUID: <38} {", ".join(preventions_names if preventions_names else ["null"])}')

    p = Progress()
    p.progress()
