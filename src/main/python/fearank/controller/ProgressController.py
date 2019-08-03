import datetime

from PyQt5.QtCore import QTimer, QThreadPool

from fearank.thread.Worker import Worker
from fearank.ui.MainWindow import Ui_MainWindow


class ProgressController:
    current_method = 0
    current_iteration = 0

    _max_iterations: int
    _max_methods: int
    _current_progress = 0

    _thread_pool: QThreadPool
    _ui: Ui_MainWindow
    _time_start: datetime
    _time_current: datetime
    _timer: QTimer
    _interval: int

    def __init__(self, ui):
        self._ui = ui

        self._thread_pool = QThreadPool()
        print("Multithreading with maximum %d threads" % self._thread_pool.maxThreadCount())

        self._max_iterations = 0
        self._max_methods = 0

        self._interval = 1000
        self._timer = QTimer()
        self._timer.setInterval(self._interval)
        self._timer.timeout.connect(self._timer_tick)

    def init_progress(self, progress_fn):
        worker = Worker(progress_fn)
        worker.signals.result.connect(self._print_output)
        worker.signals.finished.connect(self._thread_complete)
        worker.signals.progress.connect(self._update_progress)

        self._thread_pool.start(worker)

    def _print_output(self, s):
        print(s)

    def _thread_complete(self):
        self.stop()
        print("THREAD COMPLETE!")

    def start(self):
        self._reset()
        self._update_progress()
        self._timer.start()

    def _reset(self):
        ProgressController.reset_iteration()
        ProgressController.reset_current_method()
        self._time_start = datetime.datetime.now()
        self._time_current = self._time_start

    def stop(self):
        self._timer.stop()

    def _update_progress(self):
        progress = self._get_progress_percent()
        self._ui.progress_bar.setValue(progress)

        text = self._get_progress_text()
        self._ui.progress_info.setText(text)

    def _get_progress_percent(self):
        total = self._max_methods * self._max_iterations
        progress = (ProgressController.current_method - 1) * self._max_iterations + ProgressController.current_iteration
        return int(progress / total * 100)

    def _get_progress_text(self):
        time_diff = self._time_current - self._time_start
        format_str = "{:d}. Method / {:d} of {:d} Iterations / {:.0f}s"
        text = format_str.format(
            ProgressController.current_method,
            ProgressController.current_iteration,
            self._max_iterations,
            time_diff.total_seconds()
        )
        return text

    def _timer_tick(self):
        self._time_current = datetime.datetime.now()
        self._update_progress()

    def set_max_iterations(self, iterations):
        self._max_iterations = iterations

    @staticmethod
    def inc_iteration():
        ProgressController.current_iteration += 1

    @staticmethod
    def reset_iteration():
        ProgressController.current_iteration = 0

    def set_max_methods(self, max_methods):
        self._max_methods = max_methods

    @staticmethod
    def inc_method_counter():
        ProgressController.current_method += 1

    @staticmethod
    def reset_current_method():
        ProgressController.current_method = 0
