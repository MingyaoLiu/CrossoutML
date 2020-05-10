import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from ui_videoframe import bot

import sys

from ui_settingwindow import UI_SettingWindow

class UI_MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("mainwindow.ui", self)
        
        self.startBtn.clicked.connect(self.startApp)
        self.settingBtn.clicked.connect(self.goToSettingWindow)
        self.quitBtn.clicked.connect(self.closeApp)

    def startApp(self):
        bot()
        
    def goToSettingWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = UI_SettingWindow(self.window)
        self.ui.show()

    def closeApp(self):
        self.close()
        QtWidgets.QApplication.quit()
        return sys.exit(0)