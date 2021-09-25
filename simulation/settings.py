import os
from uuid import uuid4

from pydantic import BaseSettings, Field, validator

SIMULATION_UUID = str(uuid4())


class SimulationBaseSetting(BaseSettings):
    class Config:
        env_file = 'simulation.config'
        env_file_encoding = 'utf-8'


class SubjectSettings(SimulationBaseSetting):
    MIN_AGE: int = Field(1, gt=0)
    MAX_AGE: int = Field(100, le=100)


class PathologySettings(SimulationBaseSetting):
    PROB_INFECTION: float = Field(0.15, ge=0, le=1)
    PROB_DEATH: float = Field(0.03, ge=0, le=1)
    EXPOSED_MAX_DAY: int = Field(7, gt=0)
    INFECTIOUS_MAX_DAY: int = Field(14, gt=0)


class PreventionSettings(SimulationBaseSetting):
    # MASK
    MASK_PROB_INFECTION: float = Field(0.2, ge=0, le=1)
    MASK_PROB_DEATH: float = Field(1, ge=0, le=1)
    MASK_PERC_ACTIVATION: float = Field(0.4, ge=0, le=1)
    # ISOLATION
    ISOLATION_PROB_INFECTION: float = Field(0.5, ge=0, le=1)
    ISOLATION_PROB_DEATH: float = Field(1, ge=0, le=1)
    ISOLATION_PERC_ACTIVATION: float = Field(0.2, ge=0, le=1)
    # VACCINE
    VACCINE_PROB_INFECTION: float = Field(1, ge=0, le=1)
    VACCINE_PROB_DEATH: float = Field(0.05, ge=0, le=1)
    VACCINE_PERC_ACTIVATION: float = Field(0.6, ge=0, le=1)


class BoardSettings(SimulationBaseSetting):
    DIMENSION: int = Field(51, ge=9)
    CELL_SICK_LOCATION: int = 25

    @validator('DIMENSION')
    def validate_dimension(cls, value: int) -> int:
        if value % 2 == 0:
            raise RuntimeError('dimension must be an odd number')
        return value

    @property
    def CELL_SICK_POSITION(self) -> tuple[int, int]:  # noqa
        return self.CELL_SICK_LOCATION, self.CELL_SICK_LOCATION


class ReportSettings(SimulationBaseSetting):
    OUTPUT_BASE_DIR: str = './'
    OUTPUT_BOARD_RESOLUTION: int = Field(800, ge=800, le=1920)
    OUTPUT_BOARD_DPI: int = 96

    @property
    def OUTPUT_BOARD_DIR(self) -> str:  # noqa
        return os.path.join(self.OUTPUT_BASE_DIR, f'results/{SIMULATION_UUID}/board')

    @property
    def OUTPUT_SHEET_DIR(self) -> str:  # noqa
        return os.path.join(self.OUTPUT_BASE_DIR, f'results/{SIMULATION_UUID}/sheet')

    @property
    def OUTPUT_GRAPH_DIR(self) -> str:  # noqa
        return os.path.join(self.OUTPUT_BASE_DIR, f'results/{SIMULATION_UUID}/graph')

    @property
    def OUTPUT_GIF_DIR(self) -> str:  # noqa
        return os.path.join(self.OUTPUT_BASE_DIR, f'results/{SIMULATION_UUID}/gif')

    @property
    def OUTPUT_BOARD_DIMENSION(self) -> tuple[int, int]:  # noqa
        return self.OUTPUT_BOARD_RESOLUTION, self.OUTPUT_BOARD_RESOLUTION


subject_settings = SubjectSettings()
pathology_settings = PathologySettings()
prevention_settings = PreventionSettings()
board_settings = BoardSettings()
report_settings = ReportSettings()

os.makedirs(report_settings.OUTPUT_BOARD_DIR, exist_ok=True)
os.makedirs(report_settings.OUTPUT_SHEET_DIR, exist_ok=True)
os.makedirs(report_settings.OUTPUT_GRAPH_DIR, exist_ok=True)
os.makedirs(report_settings.OUTPUT_GIF_DIR, exist_ok=True)
