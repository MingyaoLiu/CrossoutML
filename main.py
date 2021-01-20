import Constants
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QWindow, QPaintDeviceWindow, QPainter, QPen, QBrush
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QMainWindow
from PyQt5.QtCore import Qt

from ui_mainwindow import UI_MainWindow

# temporary
import d3dshot
import cv2
import pytesseract
import numpy


import ctypes

# import torch
# import cv2

# print(torch.cuda.is_available() == True)
# print(cv2.getBuildInformation())


# import InputControl
# InputControl.KeyPress("w", "12").start()
# InputControl.KeyPress("s", "2").start()


# import operator
# class Point(tuple):
#     def __new__(self, x, y):
#         Point.x = property(operator.itemgetter(0))
#         Point.y = property(operator.itemgetter(1))
#         return tuple.__new__(Point, (x, y))
# a = Point(1, 3)
# print(a.x)

from SettingsClass import getGlobalSetting


def checkSettings():
    return getGlobalSetting()


class TITLEBARINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.wintypes.DWORD), ("rcTitleBar", ctypes.wintypes.RECT),
                ("rgstate", ctypes.wintypes.DWORD * 6)]




class OverlayWindow(QMainWindow ):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("CrossML Overlay")
        crossoutwindowpos = self.__GetWindowRectFromName('Crossout 0.12.30.159199')





        self.setGeometry(crossoutwindowpos[0], crossoutwindowpos[1], crossoutwindowpos[2] - crossoutwindowpos[0], crossoutwindowpos[3] - crossoutwindowpos[1])

        


        # self.setWindowFlags(
        #     QtCore.Qt.WindowStaysOnTopHint |
        #     QtCore.Qt.FramelessWindowHint |
        #     QtCore.Qt.X11BypassWindowManagerHint
        #     # QtCore.Qt.WindowTransparentForInput
        # )
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # self.setWindowOpacity(0.2)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        print(self.__GetWindowRectFromName('Crossout 0.12.30.159199'))
        

    def mousePressEvent(self, event):
        QtWidgets.qApp.quit()

    

    def __GetWindowRectFromName(self, name:str)-> tuple:
        hwnd = ctypes.windll.user32.FindWindowW(0, name)
        rect = ctypes.wintypes.RECT() # This rect return the window rect with title bar and shadow
        rect2 = ctypes.wintypes.RECT() # this rect return the innerwindow only, without title bar and shadow
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect2))


        title_info = TITLEBARINFO()
        title_info.cbSize = ctypes.sizeof(title_info)
        ctypes.windll.user32.GetTitleBarInfo(hwnd, ctypes.byref(title_info))
        print(title_info.rcTitleBar.left, title_info.rcTitleBar.top, title_info.rcTitleBar.right, title_info.rcTitleBar.bottom)

        foundwindow = ctypes.windll.dwmapi.DwmGetWindowAttribute
        if foundwindow:
            rect = ctypes.wintypes.RECT()
            DWMWA_EXTENDED_FRAME_BOUNDS = 9
            foundwindow(
                hwnd,
                ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
                ctypes.byref(rect), ctypes.sizeof(rect))
            window_size = (rect.left, rect.top, rect.right, rect.bottom)
        print(hwnd)
        print(window_size)
        print("GOT SIZE 1 ")
        print((rect2.left, rect2.top, rect2.right, rect2.bottom))
        print("GOT SIZE 2 ")
        return (rect.left, title_info.rcTitleBar.bottom, rect.right, rect.bottom)
    
    def paintEvent(self, event):
        painter  = QPainter(self)
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
 
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        #painter.setBrush(QBrush(Qt.green, Qt.DiagCrossPattern))
 
        painter.drawEllipse(100,100, 400,200)


if __name__ == "__main__":
    
    def __GetWindowRectFromName( name:str)-> tuple:
        hwnd = ctypes.windll.user32.FindWindowW(0, name)
        rect = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect))
        # print(hwnd)
        # print(rect)
        return (rect.left, rect.top, rect.right, rect.bottom)
    
    checkSettings()

    app = QtWidgets.QApplication(sys.argv)
    window = UI_MainWindow()
    window.show()


    mywindow = OverlayWindow()
    mywindow.show()

    print(__GetWindowRectFromName('CrossML Overlay'))

    app.exec_()
