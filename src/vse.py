import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QHBoxLayout,
    QPushButton, QVBoxLayout, QMessageBox,
)
from utils import *
from signals import *
from ocr_tool import *
from widgets import *


class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.initUI()
        outStream = Stream()
        outStream.newText.connect(self.subtitleWidget.onUpdateText)
        sys.stdout = outStream
        self.ocrEngine = OcrThread()
        self.paramSingal = ParamSignal()
        self.paramSingal.paramChanged.connect(self.ocrEngine.onUpdateParam)

    def initUI(self):
        self.setWindowTitle("Video Subtitles Extractor (VSE)")
        self.setWindowIcon(QIcon('../asserts/img/icon.svg'))
        self.resize(648, 480)

        self.paramWidget = ParamWidget()
        self.startBtn = QPushButton("开始")
        self.startBtn.clicked.connect(self.start)
        self.pauseBtn = QPushButton("暂停")
        self.pauseBtn.clicked.connect(self.pause)
        btnLayout = QHBoxLayout()
        btnLayout.addWidget(self.startBtn)
        btnLayout.addWidget(self.pauseBtn)
        headLayout = QHBoxLayout()
        headLayout.addWidget(self.paramWidget)
        headLayout.addLayout(btnLayout)
        self.subtitleWidget = SubtitleWidget()
        mainWindow = QWidget()
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(headLayout)
        mainLayout.addWidget(self.subtitleWidget)
        mainWindow.setLayout(mainLayout)
        self.setCentralWidget(mainWindow)

    def closeEvent(self, event):
        sys.stdout = sys.__stdout__
        super().closeEvent(event)
        
    def start(self):
        if self.startBtn.text() == "开始":
            params = self.paramWidget.getParams()
            if (params["mode"] == "video" or params["mode"] == "image")and params["filename"] is None:
                QMessageBox.information(self, "提示", "需要选择文件")
                return
            if params["mode"] == "url":
                QMessageBox.information(self, "提示", "网络模式暂时没有实现")
                return
            self.paramSingal.send(params)
            self.subtitleWidget.textWidget.clear()
            if params["mode"] != "image":
                self.startBtn.setText("停止")
            self.ocrEngine.start()
        else:
            params = {"isRunning": False, "isPaused": False}
            self.paramSingal.send(params)
            self.startBtn.setText("开始")
            self.pauseBtn.setText("暂停")
    
    def pause(self):
        if self.pauseBtn.text() == "暂停":
            params = {"isPaused": True}
            self.paramSingal.send(params)
            self.pauseBtn.setText("继续")
        else:
            params = {"isPaused": False}
            self.paramSingal.send(params)
            self.pauseBtn.setText("暂停")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())