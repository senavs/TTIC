from simulation.automatos.board import Board
from simulation.automatos.cell import Cell
from simulation.report.printer import Printer
from simulation.core.prevention import SocialIsolation, Mask, Vaccine
from simulation.settings import PreventionSettings


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

            if self.board.filter_have_been_sick().size >= self.board.n_cells * PreventionSettings.MASK_PERC_ACTIVATION:
                Mask.activate()
            if self.board.filter_have_been_sick().size >= self.board.n_cells * PreventionSettings.ISOLATION_PERC_ACTIVATION:
                SocialIsolation.activate()
            if self.board.filter_have_been_sick().size >= self.board.n_cells * PreventionSettings.VACCINE_PERC_ACTIVATION:
                Vaccine.activate()

        self.increase()
        self.printer.print(self.board, f'{self.current_time:0>5}')

    def increase(self):
        self.current_time += 1
