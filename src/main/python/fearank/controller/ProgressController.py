import datetime

from fearank.ui.MainWindow import Ui_MainWindow


class ProgressController:
    _max_iterations: int
    _current_iteration: int
    _ui: Ui_MainWindow
    _time_start: datetime
    _time_current: datetime

    def __init__(self, ui):
        self._ui = ui
        self._current_iteration = 0

    def start(self):
        self._time_start = datetime.datetime.now()
        self._time_current = self._time_start

        text = self.get_progress()
        self._ui.progress_info.setText(text)

    def get_progress(self):
        time_diff = self._time_start - self._time_current
        text = "{:d}/{:d} iterations, {:.2f} seconds".format(
            self._current_iteration,
            self._max_iterations,
            time_diff.total_seconds()
        )
        return text

    def set_max_iterations(self, iterations):
        self._max_iterations = iterations
        self._current_iteration = 0
