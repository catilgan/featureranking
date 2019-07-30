from PyQt5.QtWidgets import QCheckBox


class InputController:

    def __init__(self, ui):
        self._ui = ui

    def get_ranking_checkboxes(self):
        group = self._ui.method_selection_group

        checkboxes = group.findChildren(QCheckBox)
        return checkboxes

    def get_selected_ranking_methods(self):
        methods = []
        checkboxes = self.get_ranking_checkboxes()

        for checkbox in checkboxes:
            if checkbox.isChecked():
                methods.append(checkbox.objectName())

        return methods

    def get_data_columns(self):
        gt = self._ui.gt_col.text()
        cols = [int(gt) - 1]
        feature_cols = self._ui.feature_cols.text()

        for part in feature_cols.split(','):
            if '-' in part:
                p = part.split('-')
                if p[1]:
                    cols.extend(list(range(int(p[0]) - 1, int(p[1]))))
                else:
                    cols.extend([int(p[0]) - 1, -1])
            elif part:
                cols.append(int(part) - 1)

        cols.sort()

        return cols
