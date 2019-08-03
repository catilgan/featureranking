import datetime

from PyQt5.QtCore import QTimer, QThreadPool

from fearank.thread.Worker import Worker
from fearank.ui.MainWindow import Ui_MainWindow


class ProgressController:
    current_method = 0
    current_iteration = 0

    _thread_pool: QThreadPool
    _max_iterations: int
    _ui: Ui_MainWindow
    _time_start: datetime
    _time_current: datetime
    _timer: QTimer
    _interval: int

    def __init__(self, ui):
        self._ui = ui

        self._thread_pool = QThreadPool()
        print("Multithreading with maximum %d threads" % self._thread_pool.maxThreadCount())

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
        text = self._get_progress()
        self._ui.progress_info.setText(text)

    def _get_progress(self):
        time_diff = self._time_current - self._time_start
        format_str = "{:d}. Method / {:d} of {:d} Iterations / {:.0f}s"
        text = format_str.format(
            ProgressController.current_method,
            ProgressController.current_iteration,
            self._max_iterations,
            time_diff.total_seconds()
        )
        return text

    def set_max_iterations(self, iterations):
        self._max_iterations = iterations

    def _timer_tick(self):
        self._time_current = datetime.datetime.now()
        self._update_progress()

    @staticmethod
    def inc_iteration():
        ProgressController.current_iteration += 1

    @staticmethod
    def reset_iteration():
        ProgressController.current_iteration = 0

    @staticmethod
    def inc_method_counter():
        ProgressController.current_method += 1

    @staticmethod
    def reset_current_method():
        ProgressController.current_method = 0
