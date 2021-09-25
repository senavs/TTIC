import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description='Spread disease simulation')
parser.add_argument('--isolation', '-i', dest='isolation', action='store_true')
parser.add_argument('--mask', '-m', dest='mask', action='store_true')
parser.add_argument('--vaccine', '-v', dest='vaccine', action='store_true')

args = parser.parse_args()

if __name__ == '__main__':
    from simulation.settings import SIMULATION_UUID
    from simulation.automatos.progress import Progress
    from simulation.core.prevention import PreventionEnum

    PREVENTIONS = {
        'isolation': PreventionEnum.isolation,
        'mask': PreventionEnum.mask,
        'vaccine': PreventionEnum.vaccine,
    }

    preventions_names = []
    selected_preventions = []

    for flag, value in args.__dict__.items():
        if not value:
            continue
        preventions_names.append(flag)
        selected_preventions.append(PREVENTIONS[flag])

    preventions = ", ".join(preventions_names if preventions_names else ["null"])
    print(f'{datetime.now().isoformat()} {SIMULATION_UUID} - start. preventions: {preventions}')

    p = Progress(*selected_preventions)
    p.progress()

    print(f'{datetime.now().isoformat()} {SIMULATION_UUID} - done. {p.current_time} days')
