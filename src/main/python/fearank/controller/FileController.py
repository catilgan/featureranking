import os
import pathlib
import time
from os.path import dirname

from fearank.file.FileDialog import FileDialog
from fearank.file.ResultTextWriter import ResultTextWriter
from fearank.ranking.Ranking import Ranking


class FileController:

    def __init__(self, ui):
        self._ui = ui

        self._file_dialog = FileDialog()
        self._import_file = ''
        self._export_file = ''
        self._export_file_format = '{0}{1}.txt'

    def import_action(self):
        file_name = self._file_dialog.show_import_dialog()
        self.set_import_file(file_name)

    def export_action(self):
        file_name = self._file_dialog.show_export_dialog()
        self.set_export_file(file_name)

    def get_import_file(self):
        return self._import_file

    def set_import_file(self, file_name):
        if FileDialog.file_exists(file_name):
            self._import_file = file_name
            self._ui.import_file.setText(file_name)
            self._ui.calculate_btn.setEnabled(True)
        else:
            self._ui.calculate_btn.setEnabled(False)

    def get_export_file(self):
        return self._export_file

    def set_export_file(self, file_name):
        if file_name:
            self._export_file = file_name
            self._ui.export_file.setText(file_name)

    def write_results(self, output, method):
        result_file = self.get_export_file()

        if not result_file:
            now = time.strftime("%Y-%m-%dT%H%M%S")
            parent = dirname(self.get_import_file())
            import_file = pathlib.Path(self._import_file).stem
            file_name = self._export_file_format.format(import_file, '_' + now)

            self.set_export_file(os.path.join(parent, file_name))
        else:
            self._check_export_file_ending()

        if method == Ranking.TYPE:
            writer = ResultTextWriter(self.get_export_file())
            writer.write_content(output)
        else:
            writer = ResultTextWriter(self._get_export_file_for_method(method))
            writer.write_content(output)

    def _get_export_file_for_method(self, method):
        path = pathlib.Path(self._export_file)
        return path.with_name(path.stem + '_' + method + path.suffix)

    def _check_export_file_ending(self):
        extension = pathlib.Path(self._export_file).suffix
        if extension != '.txt':
            self._export_file += ".txt"
