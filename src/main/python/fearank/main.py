import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from fbs_runtime.application_context import ApplicationContext

from fearank.controller.MainController import MainController
from fearank.ui.MainWindow import Ui_MainWindow

QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)


class AppContext(ApplicationContext):

    def run(self):
        qt_main_window = QMainWindow(flags=QtCore.Qt.WindowStaysOnTopHint)

        ui = Ui_MainWindow()
        ui.setupUi(qt_main_window)

        main_ctrl = MainController(ui, self._quit_app)
        main_ctrl.bind_events()

        qt_main_window.show()

        return self.app.exec_()

    def _quit_app(self):
        self.app.quit()


if __name__ == '__main__':
    app_context = AppContext()
    exit_code = app_context.run()
    input()
    sys.exit(exit_code)
