from simulation.automatos.board import Board
from simulation.automatos.cell import Cell
from simulation.report.printer import Printer


class Progress:

    def __init__(self):
        self.current_time = 0
        self.board = Board()
        self.printer = Printer()

    def progress(self):
        while self.board.sick_cells():
            self.increase()
            self.printer.print(self.board, f'{self.current_time:0>5}')

            sick_cell: Cell
            for sick_cell in self.board.filter_sick():
                neighbours = self.board.get_neighbours(sick_cell)
                sick_cell.subject.agglomerate([cell.subject for cell in neighbours])

                sick_cell.subject.pathology.evolve()

        self.increase()
        self.printer.print(self.board, f'{self.current_time:0>5}')

    def increase(self):
        self.current_time += 1
