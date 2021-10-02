from datetime import datetime

from simulation.automatos.board import Board
from simulation.core.subject import Subject
from simulation.report.drawer import BoardImageDrawer, BoardGifDrawer, GraphDrawer
from simulation.core.prevention import SocialIsolation, Mask, Vaccine, PreventionEnum
from simulation.report.reporter import SheetReporter
from simulation.settings import prevention_settings, SIMULATION_UUID

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

    def run(self):
        with BoardImageDrawer() as board_drawer, SheetReporter(self.board) as sheet_reporter:
            sheet_reporter.report_steps()

            while self.board.sick_cells():
                self.current_time += 1

                board_drawer.draw(self.board, f'{self.current_time:0>5}')
                sheet_reporter.report_steps()

                for sick_cell in self.board.filter_sick():
                    neighbours = self.board.get_closest_neighbours(sick_cell)
                    sick_cell.subject.agglomerate([cell.subject for cell in neighbours])
                    sick_cell.subject.pathology.evolve()

                self._activate_preventions(sheet_reporter)
            else:
                self.current_time += 1

                board_drawer.draw(self.board, f'{self.current_time:0>5}')
                sheet_reporter.report_steps()

        with BoardGifDrawer() as gif_drawer:
            gif_drawer.draw()

        with GraphDrawer() as graph_drawer:
            graph_drawer.draw()

    def _activate_preventions(self, sheet_reporter: SheetReporter):
        n_cells_have_been_sick = self.board.filter_have_been_sick().size

        for name, (prev, prec_setting) in PREVS.items():
            if not PreventionEnum[name] in self.selected_prevention:
                continue
            if n_cells_have_been_sick < self.board.n_cells * prec_setting:
                continue
            if not prev.activate():
                continue

            sheet_reporter.report_prevt(name, self.current_time)
            print(f'{datetime.now().isoformat()} {SIMULATION_UUID} - {name} activated. {self.current_time} days')
