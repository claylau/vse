from PySide6.QtCore import (
    QObject, Signal
)


class Stream(QObject):
    newText = Signal(str)

    def write(self, text):
        self.newText.emit(str(text))
    
    def flush(self):
        pass


class ParamSignal(QObject):
    paramChanged = Signal(dict)

    def send(self, params):
        self.paramChanged.emit(params)