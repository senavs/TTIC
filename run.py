import os

PREVENTIONS = [
    '',
    '-i',
    '-i -m',
    '-i -m -v'
]

for prevention in PREVENTIONS:

    for _ in range(3):
        os.system(f'python3 -m simulation {prevention}')
