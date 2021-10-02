from operator import mul

import numpy as np
import pandas as pd

from simulation.automatos.board import Board
from simulation.settings import report_settings


class SheetReporter:

    def __init__(self, board: Board):
        self.flatten_board: np.ndarray = board.board.reshape(mul(*board.board.shape))

        self.cells_data = pd.DataFrame(columns=['x', 'y', 'age', 'healthy'])
        self.steps_data = pd.DataFrame(columns=[f'cell_{n:0>5}' for n in range(self.flatten_board.size)])
        self.prevt_data = pd.DataFrame([[0, 0, 0]], columns=['isolation', 'mask', 'vaccine'])

    def report_cells(self):
        for cell in self.flatten_board:
            self.cells_data = self.cells_data.append({
                'x': cell.x,
                'y': cell.y,
                'age': cell.subject.age,
                'healthy': cell.subject.healthy_lifestyle
            }, ignore_index=True)

    def report_steps(self):
        func = np.frompyfunc(lambda cell: cell.subject.condition.value, 1, 1)

        self.steps_data.loc[len(self.steps_data)] = func(self.flatten_board)

    def report_prevt(self, prevt_type: str, started_day: int):
        assert prevt_type in self.prevt_data.columns

        self.prevt_data[prevt_type] = started_day

    def __enter__(self) -> 'SheetReporter':
        self.report_cells()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cells_data.to_csv(f'{report_settings.OUTPUT_SHEET_DIR}/cells.csv', index=False)  # noqa
        self.steps_data.to_csv(f'{report_settings.OUTPUT_SHEET_DIR}/steps.csv', index=False)  # noqa
        self.prevt_data.to_csv(f'{report_settings.OUTPUT_SHEET_DIR}/prevt.csv', index=False)  # noqa
