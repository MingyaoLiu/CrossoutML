



import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import time

class UI_SettingWindow(QtWidgets.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("settingwindow.ui", self)


