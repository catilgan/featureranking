from PyQt5.QtCore import QCoreApplication

from fearank.controller.FileController import FileController
from fearank.controller.InputController import InputController
from fearank.controller.ProgressController import ProgressController
from fearank.controller.ValidationController import ValidationController
from fearank.file.CsvReader import CsvReader
from fearank.ranking.ChiSquare import ChiSquare
from fearank.ranking.ExtraTreesClassifierScore import ExtraTreesClassifierScore
from fearank.ranking.ExtraTreesRegressorScore import ExtraTreesRegressorScore
from fearank.ranking.FScore import FScore
from fearank.ranking.MRMR import MRMR
from fearank.ranking.MRMRCpp import MRMRCpp
from fearank.ranking.MutualInfoRegression import MutualInfoRegression
from fearank.ranking.RandomForestClassifierScore import RandomForestClassifierScore
from fearank.ranking.RandomForestRegressorScore import RandomForestRegressorScore
from fearank.ranking.Ranking import Ranking
from fearank.ui.MainWindow import Ui_MainWindow


class MainController:
    _ui: Ui_MainWindow
    _widget_ctrl: InputController
    _validation_ctrl: ValidationController
    _input_ctrl: InputController
    _file_ctrl: FileController
    _progress_ctrl: ProgressController

    def __init__(self, ui, quit_method):
        self._ui = ui
        self._quit_method = quit_method

        self._init_controllers()

    def _init_controllers(self):
        self._widget_ctrl = InputController(self._ui)
        self._validation_ctrl = ValidationController(self._ui)
        self._input_ctrl = InputController(self._ui)
        self._file_ctrl = FileController(self._ui)
        self._progress_ctrl = ProgressController(self._ui)

    def bind_events(self):
        self._ui.import_btn.clicked.connect(self._file_ctrl.import_action)
        self._ui.export_btn.clicked.connect(self._file_ctrl.export_action)
        self._ui.calculate_btn.clicked.connect(self.calculate_action)
        self._ui.close_btn.clicked.connect(self._quit_method)

        self._ui.gt_col.textEdited.connect(self._validation_ctrl.validate_gt_field)
        self._ui.feature_cols.textEdited.connect(self._validation_ctrl.validate_feature_cols_field)

    def calculate_action(self):
        self._ui.calculate_btn.setEnabled(False)
        QCoreApplication.processEvents()

        self.start_progress()
        self.calculate_ranking()

        self._ui.calculate_btn.setEnabled(True)

    def calculate_ranking(self):
        cols, data = self.fetch_data()

        ranking_methods = self._widget_ctrl.get_selected_ranking_methods()

        outputs = []
        for ranking_method in ranking_methods:
            output = self.execute_ranking(ranking_method, data, cols)
            self._file_ctrl.write_results(output, ranking_method)
            outputs.append(output)

        result = "".join(outputs)

        self._file_ctrl.write_results(result, Ranking.TYPE)
        self._ui.ranking_results.setText(result)

    def execute_ranking(self, ranking_method, data, cols):
        output = ''
        if ranking_method == MRMR.TYPE:
            output = MRMR.execute(data, cols)
        elif ranking_method == MRMRCpp.TYPE:
            output = MRMRCpp.execute(data, cols)
        elif ranking_method == RandomForestRegressorScore.TYPE:
            output = self.execute_ranking_algorithm(RandomForestRegressorScore, data, cols)
        elif ranking_method == FScore.TYPE:
            output = self.execute_ranking_algorithm(FScore, data, cols)
        elif ranking_method == ChiSquare.TYPE:
            output = self.execute_ranking_algorithm(ChiSquare, data, cols)
        elif ranking_method == MutualInfoRegression.TYPE:
            output = self.execute_ranking_algorithm(MutualInfoRegression, data, cols)
        elif ranking_method == ExtraTreesClassifierScore.TYPE:
            output = self.execute_ranking_algorithm(ExtraTreesClassifierScore, data, cols)
        elif ranking_method == RandomForestClassifierScore.TYPE:
            output = self.execute_ranking_algorithm(RandomForestClassifierScore, data, cols)
        elif ranking_method == ExtraTreesRegressorScore.TYPE:
            output = self.execute_ranking_algorithm(ExtraTreesRegressorScore, data, cols)

        return output + "\n\n"

    def execute_ranking_algorithm(self, algorithm, data, cols):
        """
        :param algorithm:
        :param data:
        :param cols:
        :return:
        """
        iterations = self.get_iterations()
        if iterations == 1:
            return algorithm.execute(data, cols)
        else:
            return algorithm.execute_multiple(data, cols, iterations)

    def get_iterations(self):
        iterations = int(self._ui.iterations.value())
        return iterations

    def fetch_data(self):
        csv_file = self._file_ctrl.get_import_file()
        cols = self._input_ctrl.get_data_columns()
        data = CsvReader.read_csv(csv_file, cols)

        return cols, data

    def start_progress(self):
        iterations = self.get_iterations()
        self._progress_ctrl.set_max_iterations(iterations)
        self._progress_ctrl.start()
