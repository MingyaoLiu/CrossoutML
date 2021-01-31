import Constants
import sys

from PyQt5.QtWidgets import QApplication

from uis.QTWindowMain import getMainWindow
from uis.QTWindowOverlay import getOverlay

# temporary
import cv2
import pytesseract
import numpy
import Constants as const

import os, errno




if __name__ == "__main__":
            
    try:
        if not os.path.exists("logmap"):
            os.makedirs("logmap")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    

    app = QApplication(sys.argv)

    window = getMainWindow()
    window.show()


    app.exec_()
