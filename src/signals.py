from PyQt5.QtCore import (
    QObject, pyqtSignal
)
from PyQt5.QtWidgets import QApplication


class Stream(QObject):
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))
        QApplication.processEvents()


class ParamSignal(QObject):
    paramChanged = pyqtSignal(dict)

    def send(self, params):
        self.paramChanged.emit(params)
        QApplication.processEvents()