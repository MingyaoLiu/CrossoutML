


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QWindow, QPaintDeviceWindow, QPainter, QPen, QBrush, QFontMetrics
from PyQt5.QtWidgets import QDesktopWidget, QWidget, QMainWindow
from PyQt5.QtCore import Qt
from SettingsClass import getGlobalSetting

game_overlay = None

def getOverlay():
    global game_overlay
    if game_overlay:
        return game_overlay
    else:
        game_overlay = OverlayWindow()
        return game_overlay

class OverlayWindow(QMainWindow ):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("CrossML Overlay")

        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
            # QtCore.Qt.WindowTransparentForInput
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def resize(self, rect):
        self.setGeometry(rect[0], rect[1], rect[2], rect[3])

    def autoResize(self):
        setting = getGlobalSetting().settings
        left = setting
        top = innerWindow[1]
        right = innerWindow[2]
        bottom = innerWindow[3]
        width = innerWindow[2] - innerWindow[0]
        height = innerWindow[3] - innerWindow[1]
        getOverlay().resize((left, top, width, height))
        overlay.show()



    def mousePressEvent(self, event):
        QtWidgets.qApp.quit()
    
    def paintEvent(self, event):
        painter  = QPainter(self)
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
 
        painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))
        painter.drawRect(0,0, 100,10)
        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        painter.drawText(0, 10, "Overlay Working")