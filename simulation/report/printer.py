import os

import numpy as np
import imageio
from matplotlib import pyplot as plt
from matplotlib.axes import SubplotBase
from matplotlib.figure import Figure

from simulation.automatos.board import Board
from simulation.settings import report_settings


class Printer:

    def __init__(self):
        self.figure, self.axis = self.initialize_figure()

    @staticmethod
    def initialize_figure() -> tuple[Figure, SubplotBase]:
        width, height = report_settings.OUTPUT_BOARD_DIMENSION
        dpi = report_settings.OUTPUT_BOARD_DPI

        figure = plt.figure(figsize=(width / dpi, height / dpi), dpi=dpi)
        axis = plt.subplot(1, 1, 1)

        return figure, axis

    def imshow(self, arr: np.ndarray) -> np.ndarray:
        self.axis.cla()  # noqa: clear axis data to decrease figure.savefig time
        self.axis.axis('off')  # noqa
        image = self.axis.imshow(arr)  # noqa

        # add grid border in each pixel
        pixel, *_ = arr.shape
        plt.hlines(y=np.arange(0, pixel) + 0.5, xmin=np.full(pixel, 0) - 0.5, xmax=np.full(pixel, pixel) - 0.5, color="black", linewidth=0.2)
        plt.vlines(x=np.arange(0, pixel) + 0.5, ymin=np.full(pixel, 0) - 0.5, ymax=np.full(pixel, pixel) - 0.5, color="black", linewidth=0.2)

        return image

    def draw(self, board: Board, file_name: str):
        func = np.frompyfunc(lambda cell: cell.draw(), 1, 1)

        draw_board = np.array(func(board.board).tolist(), dtype=np.uint8)
        image = self.imshow(draw_board)

        self.figure.savefig(f'{report_settings.OUTPUT_BOARD_DIR}/{file_name}.png', bbox_inches='tight')

        return image

    @classmethod
    def make_gif(cls):
        images = []
        for filename in sorted(os.listdir(report_settings.OUTPUT_BOARD_DIR)):
            images.append(imageio.imread(os.path.join(report_settings.OUTPUT_BOARD_DIR, filename)))
        imageio.mimsave(f'{report_settings.OUTPUT_GIF_DIR}/movie.gif', images)
