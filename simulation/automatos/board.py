import numpy as np

from simulation.automatos.cell import Cell
from simulation.core.subject import Subject
from simulation.core.pathology import ConcretePathology
from simulation.settings import BoardSettings


class Board:

    def __init__(self):
        self.board = self.initialize_board()
        self.n_cells = BoardSettings.DIMENSION * BoardSettings.DIMENSION

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
                board[i, j] = Cell(i, j, Subject())

        x, y = BoardSettings.CELL_SICK_POSITION
        board[x, y] = Cell(x, y, Subject.create_sick_subject())

        return board

    def sick_cells(self) -> bool:
        return self.filter_sick().size > 0

    def filter_sick(self) -> np.ndarray:
        return self.board[np.bool_(self.board) == True]  # noqa

    def filter_have_been_sick(self) -> np.ndarray:
        return self.board[np.equal(self.board, ConcretePathology)]  # noqa

    def get_neighbours(self, cell: Cell) -> list[Cell]:
        x, y = cell.x, cell.y

        neighbours: np.ndarray = np.concatenate(list(row[y - (y > 0):y + 2] for row in self.board[x - (x > 0): x + 2]))
        neighbours: list = neighbours.tolist()  # noqa
        neighbours.remove(cell)

        return neighbours
