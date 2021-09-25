from simulation.automatos.board import Board
from simulation.core.subject import Subject
from simulation.report.printer import Printer
from simulation.core.prevention import SocialIsolation, Mask, Vaccine, PreventionEnum
from simulation.report.reporter import Reporter
from simulation.settings import prevention_settings

PREVS = {
    'mask': [Mask, prevention_settings.MASK_PERC_ACTIVATION],
    'isolation': [SocialIsolation, prevention_settings.ISOLATION_PERC_ACTIVATION],
    'vaccine': [Vaccine, prevention_settings.VACCINE_PERC_ACTIVATION],
}


class Progress:

    def __init__(self, *preventions: PreventionEnum):
        self.selected_prevention = list(set(preventions))
        Subject.set_preventions([prevention.value for prevention in preventions])

        self.current_time = 0
        self.board = Board()

        self.printer = Printer()
        self.reporter = Reporter(self.board)

    def progress(self):
        self.reporter.report_cells()

        while self.board.sick_cells():
            self.record()

            for sick_cell in self.board.filter_sick():
                neighbours = self.board.get_neighbours(sick_cell)
                sick_cell.subject.agglomerate([cell.subject for cell in neighbours])

                sick_cell.subject.pathology.evolve()

            self.activate_preventions()

        self.record()
        self.reporter.save()
        self.printer.make_gif()

    def record(self):
        self.current_time += 1
        self.printer.draw(self.board, f'{self.current_time:0>5}')
        self.reporter.report_steps()

    def activate_preventions(self):
        n_cells_have_been_sick = self.board.filter_have_been_sick().size

        for name, (prev, prec_setting) in PREVS.items():
            if not PreventionEnum[name] in self.selected_prevention:
                continue
            if n_cells_have_been_sick < self.board.n_cells * prec_setting:
                continue
            if not prev.activate():
                continue

            self.reporter.report_prevt(name, self.current_time)
