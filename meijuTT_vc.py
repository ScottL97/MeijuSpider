#!-*-coding:utf-8 -*-
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from meijuTT_v import Ui_mainWindow
from meijuTT_c import get_info
import sys

global get_keyword


class DataCollect(QThread):
    sinOut = pyqtSignal(str)  # 自定义信号，执行run()函数时，从相关线程发射此信号

    def __init__(self, parent=None):
        super(DataCollect, self).__init__(parent)

    def __del__(self):
        print("Close thread!")
        self.wait()

    def run(self):
        self.collect_data()

    def collect_data(self):
        global get_keyword
        print("Searching... "+"("+get_keyword+")")
        get_info(get_keyword)
        status = "Done!"
        # 发出信号
        self.sinOut.emit(status)
        # 线程休眠1秒
        # self.sleep(1)


class meijuTT_control(QtWidgets.QMainWindow, Ui_mainWindow):
    def __init__(self, parent=None):
        super(meijuTT_control, self).__init__(parent)
        self.setupUi(self)
        # 添加按钮响应事件
        self.pushButton.clicked.connect(self.slotStart)

        # 创建新线程，将自定义信号sinOut连接到txtShow()槽函数
        self.thread = DataCollect()
        self.thread.sinOut.connect(self.txtShow)

    # 开始按钮按下后使其不可用，启动线程
    def slotStart(self):
        self.label_3.setText("Searching...")
        global get_keyword
        get_keyword = self.lineEdit.text()
        self.pushButton.setEnabled(False)
        self.thread.start()

    def txtShow(self, status):
        global get_keyword
        print("Display...")
        with open("%s.txt" % get_keyword, "r") as txt:
            self.textEdit.setText(txt.read())
        self.label_3.setText(status)
        self.pushButton.setEnabled(True)
        print(status)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    meijuTT_control = meijuTT_control()
    meijuTT_control.show()
    sys.exit(app.exec_())

