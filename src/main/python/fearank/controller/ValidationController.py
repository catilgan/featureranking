from PyQt5 import QtGui
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QIntValidator, QRegExpValidator


class ValidationController:

    def __init__(self, ui):
        self._ui = ui

        self._set_validators()

    def _set_validators(self):
        gt = QIntValidator(1, 99)
        self._ui.gt_col.setValidator(gt)

        rx = QRegExp("^([0-9]+(-[0-9]+)?)(,([0-9]+(-[0-9]+)?))*$")
        features = QRegExpValidator(rx)
        self._ui.feature_cols.setValidator(features)

    def validate_gt_field(self):
        field = self._ui.gt_col
        self._validate_field(field)

    def validate_feature_cols_field(self):
        field = self._ui.feature_cols
        self._validate_field(field)

    @staticmethod
    def _validate_field(field):
        validator = field.validator()
        state = validator.validate(field.text(), 0)[0]

        if state == QtGui.QValidator.Invalid or not field.text():
            color = '#f6989d'
        else:
            color = '#ffffff'

        font = 'font: normal 11pt "DejaVu Sans"'
        field.setStyleSheet('QLineEdit { background-color: %s; %s; }' % (color, font))
