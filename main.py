import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget

from ui_mainwindow import UI_MainWindow



# import torch
# import cv2

# print(torch.cuda.is_available() == True)
# print(cv2.getBuildInformation())


# import InputTrigger
# InputTrigger.KeyPress("w", "12").start()
# InputTrigger.KeyPress("s", "2").start()



# import operator
# class Point(tuple):
#     def __new__(self, x, y):
#         Point.x = property(operator.itemgetter(0))
#         Point.y = property(operator.itemgetter(1))
#         return tuple.__new__(Point, (x, y))
# a = Point(1, 3)
# print(a.x)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = UI_MainWindow()
    window.show()

    app.exec_()

