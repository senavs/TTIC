from typing import Type

from simulation.automatos.board import Board
from simulation.core.subject import Subject
from simulation.report.printer import Printer
from simulation.core.prevention import SocialIsolation, Mask, Vaccine, Prevention
from simulation.report.reporter import Reporter
from simulation.settings import PreventionSettings


class Progress:

    def __init__(self, preventions: list[Type['Prevention']]):
        self.selected_prevention = preventions
        Subject.set_preventions(preventions)

        self.current_time = 0
        self.board = Board()
        self.printer = Printer()
        self.reporter = Reporter(self.board)

    def progress(self):
        self.reporter.report_cells()

        while self.board.sick_cells():
            self.increase()
            self.printer.print(self.board, f'{self.current_time:0>5}')
            self.reporter.report_steps()

            for sick_cell in self.board.filter_sick():
                neighbours = self.board.get_neighbours(sick_cell)
                sick_cell.subject.agglomerate([cell.subject for cell in neighbours])

                sick_cell.subject.pathology.evolve()

            self.activate_preventions()

        self.increase()
        self.printer.print(self.board, f'{self.current_time:0>5}')
        self.reporter.report_steps()

        self.reporter.save()

    def increase(self):
        self.current_time += 1

    def activate_preventions(self):
        if Mask in self.selected_prevention and \
                self.board.filter_have_been_sick().size >= self.board.n_cells * PreventionSettings.MASK_PERC_ACTIVATION:
            if Mask.activate():
                self.reporter.report_prevt('mask', self.current_time)
        if SocialIsolation in self.selected_prevention and \
                self.board.filter_have_been_sick().size >= self.board.n_cells * PreventionSettings.ISOLATION_PERC_ACTIVATION:
            if SocialIsolation.activate():
                self.reporter.report_prevt('isolation', self.current_time)
        if Vaccine in self.selected_prevention and \
                self.board.filter_have_been_sick().size >= self.board.n_cells * PreventionSettings.VACCINE_PERC_ACTIVATION:
            if Vaccine.activate():
                self.reporter.report_prevt('vaccine', self.current_time)
