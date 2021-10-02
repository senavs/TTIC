import os
from abc import ABC, abstractmethod
from collections import namedtuple

import imageio
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from simulation.automatos.board import Board
from simulation.settings import report_settings

FilteredDataframes = namedtuple('FilteredDataframes', ['infected', 'dead', 'infected_per_day', 'dead_per_day', 'dead_by_age'])


class Drawer(ABC):

    def __init_subclass__(cls, width: int = 100, height: int = 100, dpi: int = 96, *args, **kwargs):
        cls.width = width
        cls.height = height
        cls.dpi = dpi
        return cls

    def __init__(self):
        self.figure: Figure = plt.figure(figsize=(self.width / self.dpi, self.height / self.dpi), dpi=self.dpi)
        self.axis: Axes = plt.subplot(1, 1, 1)

    @abstractmethod
    def draw(self, *args, **kwargs):
        raise NotImplemented

    def __enter__(self) -> 'Drawer':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.axis.cla()


class BoardImageDrawer(Drawer, width=800, height=800, dpi=96):

    def draw(self, board: Board, file_name: str):
        func = np.frompyfunc(lambda cell: cell.draw(), 1, 1)

        drawable_board = np.array(func(board.board).tolist(), dtype=np.uint8)

        self.axis.cla()
        self.axis.axis('off')
        self.axis.imshow(drawable_board)
        self._create_grid(drawable_board)

        self.figure.savefig(f'{report_settings.OUTPUT_BOARD_DIR}/{file_name}.png', bbox_inches='tight')

    @staticmethod
    def _create_grid(arr: np.ndarray):
        """"Add grid border in each pixel"""

        pixel, *_ = arr.shape
        plt.hlines(y=np.arange(0, pixel) + 0.5, xmin=np.full(pixel, 0) - 0.5, xmax=np.full(pixel, pixel) - 0.5, color="black", linewidth=0.2)
        plt.vlines(x=np.arange(0, pixel) + 0.5, ymin=np.full(pixel, 0) - 0.5, ymax=np.full(pixel, pixel) - 0.5, color="black", linewidth=0.2)


class GraphDrawer(Drawer, width=800, height=200, dpi=96):

    def draw(self):
        cells, steps, prevt = self._load_dataframes(report_settings.OUTPUT_SHEET_DIR)
        filtered_dataframes = self._create_filtered_dataframes(cells, steps)

        self._draw_infected(filtered_dataframes.infected, prevt)
        self._draw_infected_per_day(filtered_dataframes.infected_per_day, prevt)
        self._draw_dead(filtered_dataframes.dead, prevt)
        self._draw_dead_per_day(filtered_dataframes.dead_per_day, prevt)
        self._draw_dead_by_age(filtered_dataframes.dead_by_age)

    def _draw_infected(self, infected: pd.DataFrame, prevt: pd.DataFrame):
        data = infected.sum(axis=1)

        self.axis.set_title('Infected')
        self.axis.plot(data.values, color='r', label='infected')
        self._create_prevt_lines(prevt)
        self.axis.legend()

        self.figure.savefig(f'{report_settings.OUTPUT_GRAPH_DIR}/infected.png', bbox_inches='tight')

        self.axis.cla()

    def _draw_infected_per_day(self, infected_per_day: pd.DataFrame, prevt: pd.DataFrame):
        data = infected_per_day.sum(axis=1)
        rolling = data.rolling(7).mean()

        self.axis.set_title('Infected per day')
        self.axis.bar(data.index, data.values, color='r', label='infected')
        self.axis.plot(rolling, color='black', label='7 days average long-term', linewidth=2)
        self._create_prevt_lines(prevt)
        self.axis.legend()

        self.figure.savefig(f'{report_settings.OUTPUT_GRAPH_DIR}/infected_per_day.png', bbox_inches='tight')

        self.axis.cla()

    def _draw_dead(self, dead: pd.DataFrame, prevt: pd.DataFrame):
        data = dead.sum(axis=1)

        self.axis.set_title('Dead')
        self.axis.plot(data.values, color='r', label='dead')
        self._create_prevt_lines(prevt)
        self.axis.legend()

        self.figure.savefig(f'{report_settings.OUTPUT_GRAPH_DIR}/dead.png', bbox_inches='tight')

        self.axis.cla()

    def _draw_dead_per_day(self, dead_per_day: pd.DataFrame, prevt: pd.DataFrame):
        data = dead_per_day.sum(axis=1)
        rolling = data.rolling(7).mean()

        self.axis.set_title('Dead per day')
        self.axis.bar(data.index, data.values, color='r', label='dead')
        self.axis.plot(rolling, color='black', label='7 days average long-term', linewidth=2)
        self._create_prevt_lines(prevt)
        self.axis.legend()

        self.figure.savefig(f'{report_settings.OUTPUT_GRAPH_DIR}/dead_per_day.png', bbox_inches='tight')

        self.axis.cla()

    def _draw_dead_by_age(self, dead_by_age: pd.DataFrame):
        self.axis.set_title('Dead by age')
        self.axis.bar(dead_by_age.index, dead_by_age.values, color='black', label='dead')
        self.axis.legend()

        self.figure.savefig(f'{report_settings.OUTPUT_GRAPH_DIR}/dead_by_age.png', bbox_inches='tight')

        self.axis.cla()

    @staticmethod
    def _load_dataframes(reports_path: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        cells = pd.read_csv(os.path.join(reports_path, 'cells.csv'))
        steps = pd.read_csv(os.path.join(reports_path, 'steps.csv'))
        prevt = pd.read_csv(os.path.join(reports_path, 'prevt.csv'))

        return cells, steps, prevt

    @staticmethod
    def _create_filtered_dataframes(cells: pd.DataFrame, steps: pd.DataFrame) -> FilteredDataframes:
        def apply_first_time(col: pd.Series, condition: str):
            col_copy = col.copy()
            col_copy.values[:] = 0

            if condition in col.unique():
                col_copy[np.argmax((col == condition))] = 1
            return col_copy

        infected = steps.applymap(lambda x: x in ('EXPOSED', 'INFECTOUS'))

        dead = steps.applymap(lambda x: x in ('DEAD',))

        infected_per_day = steps.apply(lambda x: apply_first_time(x, 'EXPOSED'))

        dead_per_day = steps.apply(lambda x: apply_first_time(x, 'DEAD'))

        dead_by_age = dead.copy()
        dead_by_age.columns = cells.age.astype(int)
        dead_by_age = dead_by_age.sum(axis=0).groupby('age').sum().sort_index()

        return FilteredDataframes(infected, dead, infected_per_day, dead_per_day, dead_by_age)

    @staticmethod
    def _create_prevt_lines(prevt: pd.DataFrame):
        for column, color in zip(prevt.columns, ['y', 'b', 'g']):
            value = prevt.loc[0, column]
            if not value:
                continue
            plt.axvline(x=prevt.loc[0, column], color=color, label=column, linewidth=3)


class BoardGifDrawer(Drawer):

    def __init__(self):
        # it's not necessary figure or axis
        object.__init__(self)

    def draw(self):
        images = []
        for filename in sorted(os.listdir(report_settings.OUTPUT_BOARD_DIR)):
            images.append(imageio.imread(os.path.join(report_settings.OUTPUT_BOARD_DIR, filename)))
        imageio.mimsave(f'{report_settings.OUTPUT_GIF_DIR}/movie.gif', images)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # it's not necessary to clear figure or axis, but it's not have
        pass
