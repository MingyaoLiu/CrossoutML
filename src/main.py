import Constants
import sys


from PyQt5.QtWidgets import QApplication

from uis.QTWindowMain import getMainWindow
from uis.QTWindowOverlay import getOverlay

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



if __name__ == "__main__":
    
    
    getGlobalSetting()

    app = QApplication(sys.argv)

    window = getMainWindow()
    window.show()


    overlay = getOverlay()
    if (getGlobalSetting().settings.showDebugWindow):
        
        overlay.show()


    app.exec_()
