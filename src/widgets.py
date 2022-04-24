import os.path
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout,
    QRadioButton, QPushButton, QLineEdit, QVBoxLayout,
    QFileDialog, QMessageBox, QTextEdit, QFormLayout
)
from PyQt5.QtGui import (
    QDoubleValidator, QTextCursor
)


class ParamWidget(QWidget):
    """Paramters Widget, supported mode (desktop, file, url)"""
    def __init__(self, parent=None):
        super().__init__(parent)
        # model select
        modeLayout = QHBoxLayout()
        self.btn1 = QRadioButton("桌面")
        self.btn1.setChecked(True)
        self.btn2 = QRadioButton("文件")
        self.btn3 = QRadioButton("网络")
        modeLayout.addWidget(self.btn1)
        modeLayout.addWidget(self.btn2)
        modeLayout.addWidget(self.btn3)
        # file select
        fileLayout = QHBoxLayout()
        self.openBtn = QPushButton("打开")
        self.openBtn.clicked.connect(self.getFile)
        self.filenameEdit = QLineEdit()
        fileLayout.addWidget(self.openBtn)
        fileLayout.addWidget(self.filenameEdit)
        # param select
        paramLayout = QFormLayout()
        self.intervalTime = QLineEdit()
        self.intervalTime.setText("1.0")
        self.intervalTime.setValidator(QDoubleValidator(0.99, 99.99, 2))
        paramLayout.addRow("间隔时间（秒）", self.intervalTime)

        layout1 = QVBoxLayout()
        layout1.addLayout(modeLayout)
        layout1.addLayout(fileLayout)
        layout1.addLayout(paramLayout)
        self.setLayout(layout1)
    
    def getFile(self):
        if self.btn1.isChecked():
            QMessageBox.information(self, "提示", "桌面模式下不需要选择视频文件")
        elif self.btn2.isChecked():
            fname, _ = QFileDialog.getOpenFileName(self, '打开文件', os.path.expanduser('~'), "Video file (*.mp4)")
            self.filenameEdit.setText(fname)
        elif self.btn3.isChecked():
            QMessageBox.information(self, "提示", "网络模式暂时没有实现")

    def getMode(self):
        if self.btn1.isChecked():
            return "desktop"
        elif self.btn2.isChecked():
            return "file"
        elif self.btn3.isChecked():
            return "url"
    
    def getFilename(self):
        return self.filenameEdit.text()
    
    def getIntervalTime(self):
        return float(self.intervalTime.text())

    def getParams(self):
        params = {
            "video_filename": None,
            "interval": 1,
            "isRunning": True
        }
        params["mode"] = self.getMode()
        if len(self.getFilename()) == 0:
            params["video_filename"] = None
        else:
            params["video_filename"] = self.getFilename()
        params["interval"] = self.getIntervalTime()
        return params


class SubtitleWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.textWidget = QTextEdit(readOnly=True)
        self.textWidget.setPlainText("subtitles")
        hLayout2 = QHBoxLayout()
        self.saveBtn = QPushButton("保存")
        self.saveBtn.clicked.connect(self.getFile)
        self.filenameEdit = QLineEdit()
        hLayout2.addWidget(self.saveBtn)
        hLayout2.addWidget(self.filenameEdit)
        layout.addWidget(self.textWidget)
        layout.addLayout(hLayout2)
        self.setLayout(layout)
    
    def getFile(self):
        fname, _ = QFileDialog.getSaveFileName(self, '保存文件', os.path.expanduser('~'), "txt file (*.txt)")
        if fname:
            self.filenameEdit.setText(fname)
            with open(fname, 'w', encoding="utf-8") as f:
                f.write(self.textWidget.toPlainText())
    
    def onUpdateText(self, text):
        cursor = self.textWidget.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.textWidget.setTextCursor(cursor)