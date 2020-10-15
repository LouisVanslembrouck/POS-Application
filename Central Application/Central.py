import sys

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QPushButton, QLineEdit, QMainWindow, QListWidget, QMessageBox, QWidget, QVBoxLayout

# from db_conn import SqlServer
from style import global_style

class CentralApp(QMainWindow):

    switch_window = QtCore.pyqtSignal()

    def __init__(self):

        super(CentralApp, self).__init__()
        uic.loadUi('Central_Application.ui', self)

        self.setStyleSheet(global_style())

        self.item_menu = self.findChild(QWidget, 'ItemWindow')
        self.item_menu.setHidden(True)

        self.button1 = self.findChild(QPushButton, 'Button1')
        self.button2 = self.findChild(QPushButton, 'Button2')
        self.button3 = self.findChild(QPushButton, 'Button3')
        self.button4 = self.findChild(QPushButton, 'Button4')
        self.button5 = self.findChild(QPushButton, 'Button5')
        self.button6 = self.findChild(QPushButton, 'Button6')

        self.button1.clicked.connect(self.show_item_menu)

    def show_item_menu(self):
        if self.item_menu.isVisible():
            self.item_menu.setHidden(True)
        else:
            self.item_menu.setHidden(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CentralApp()
    window.show()
    sys.exit(app.exec_())
