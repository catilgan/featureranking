from os import access, R_OK
from os.path import isfile

from PyQt5.QtWidgets import QFileDialog


class FileDialog(QFileDialog):

    def show_import_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "QFileDialog.getOpenFileNames()",
            "",
            "CSV Files (*.csv)",
            options=options,

        )

        return file_name

    def show_export_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "QFileDialog.getSaveFileName()",
            "",
            "Text Files (*.txt)",
            options=options
        )

        return file_name

    @staticmethod
    def file_exists(file_name):
        return (
                file_name and
                isfile(file_name) and
                access(file_name, R_OK)
        )
