import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from uis.QTWindowSettings import UI_SettingWindow
import threading
from BotBackgroundThread import BotBackgroundThread
from DebugClass import getDebugger


game_main_window = None

def getMainWindow():
    global game_main_window
    if game_main_window:
        return game_main_window
    else:
        game_main_window = UI_MainWindow()
        return game_main_window


class UI_MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("uis/QTWindowMainUI.ui", self)

        self.isAllowedClick = True

        self.botWorker = None

        self.startBtn.clicked.connect(self.startApp)
        self.stopBtn.clicked.connect(self.stopApp)
        self.settingBtn.clicked.connect(self.goToSettingWindow)
        self.quitBtn.clicked.connect(self.closeApp)

        self.debugger = getDebugger()

    def __enableClick(self):
        self.isAllowedClick = True

    def __disableClick(self):
        self.isAllowedClick = False
        isAllowClickTimer = threading.Timer(
            1, self.__enableClick)
        isAllowClickTimer.start()

    def stopApp(self):
        if self.isAllowedClick and self.botWorker is not None:
            self.debugger.closeDebugWindow()
            self.__disableClick()
            # self.botWorker.stopBot()
            # self.botWorker.quit()
            self.botWorker.exit()
            self.botWorker = None

    def startApp(self):
        if self.isAllowedClick and self.botWorker is None:
            self.debugger.createDebugWindow()
            self.__disableClick()
            self.botWorker = BotBackgroundThread()
            self.botWorker.start()
            # self.botWorker.startBot()

    def goToSettingWindow(self):
        if self.isAllowedClick:
            self.__disableClick()
            self.window = QtWidgets.QMainWindow()
            self.ui = UI_SettingWindow(self.window)
            self.ui.show()

    def closeApp(self):
        self.debugger.closeDebugWindow()
        self.close()
        QtWidgets.QApplication.quit()
        return sys.exit(0)
