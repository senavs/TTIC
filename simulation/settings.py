import os
from uuid import uuid4

simulation_uuid = uuid4()


class SubjectSettings:
    MIN_AGE: int = 5
    MAX_AGE: int = 90


class PathologySettings:
    PROB_INFECTION: float = 0.15
    PROB_DEATH: float = 0.03
    EXPOSED_MAX_DAY: int = 7
    INFECTIOUS_MAX_DAY: int = 14


class PreventionSettings:
    # MASK
    MASK_PROB_INFECTION: float = 0.2
    MASK_PROB_DEATH: float = 1
    MASK_PERC_ACTIVATION: float = 0.1
    # ISOLATION
    ISOLATION_PROB_INFECTION: float = 0.5
    ISOLATION_PROB_DEATH: float = 1
    ISOLATION_PERC_ACTIVATION: float = 0.2
    # VACCINE
    VACCINE_PROB_INFECTION: float = 1
    VACCINE_PROB_DEATH: float = 0.05
    VACCINE_PERC_ACTIVATION: float = 0.3


class BoardSettings:
    DIMENSION: int = 51
    CELL_SICK_POSITION: tuple[int, int] = (25, 25)


class PrinterSettings:
    OUTPUT_BOARD_RESOLUTION: tuple[int, int] = (800, 800)
    OUTPUT_BOARD_DPI: int = 96
    OUTPUT_BOARD_DIR: str = f'./results/{simulation_uuid}/board/'
    OUTPUT_SHEET_DIR: str = f'./results/{simulation_uuid}/sheet/'


os.makedirs(PrinterSettings.OUTPUT_BOARD_DIR, exist_ok=True)
os.makedirs(PrinterSettings.OUTPUT_SHEET_DIR, exist_ok=True)
