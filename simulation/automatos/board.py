import numpy as np

from simulation.automatos.cell import Cell
from simulation.core.subject import Subject
from simulation.settings import BoardSettings


class Board:

    def __init__(self):
        self.board = self.initialize_board()

    @property
    def dimension(self) -> tuple[int, int]:
        selected_dimension = BoardSettings.DIMENSION
        dimension = selected_dimension if selected_dimension % 2 == 1 else selected_dimension + 1
        return dimension, dimension

    def initialize_board(self) -> np.ndarray:
        board = np.ndarray(self.dimension, dtype=object)
        x, y = board.shape

        # create board with health subjects
        for i in range(x):
            for j in range(y):
                if i == x // 2 and j == y // 2:
                    subject = Subject.create_sick_subject()
                else:
                    subject = Subject()
                board[i, j] = Cell(i, j, subject)

        return board
