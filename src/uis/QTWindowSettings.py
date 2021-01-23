



import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import time
from SettingsClass import getGlobalSetting
from uis.ui_addaccountwindow import UIAddAccountWindow
from operator import itemgetter
import cv2
from uis.QTWindowOverlay import getOverlay
import ctypes
from DCaptureClass import getDCapture

class TITLEBARINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.wintypes.DWORD), ("rcTitleBar", ctypes.wintypes.RECT),
                ("rgstate", ctypes.wintypes.DWORD * 6)]

class UI_SettingWindow(QtWidgets.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("uis/QTWindowSettingsUI.ui", self)
        self.loadSettings()
        
        self.saveBtn.clicked.connect(self.saveSettings)
        
        self.addAcctBtn.clicked.connect(self.__goToAddAcct)
        self.delAcctBtn.clicked.connect(self.__deleteCurrentAcct)

        self.detectAllSettingBtn.clicked.connect(self.__detectAllSettings)

    def __GetWindowRectFromName(self, name:str)-> tuple:
        hwnd = ctypes.windll.user32.FindWindowW(0, name)

        # This rect return the window rect with titlebar but no shadow.
        rect = ctypes.wintypes.RECT()
        foundwindow = ctypes.windll.dwmapi.DwmGetWindowAttribute
        if foundwindow:
            rect = ctypes.wintypes.RECT()
            DWMWA_EXTENDED_FRAME_BOUNDS = 9
            foundwindow(
                hwnd,
                ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
                ctypes.byref(rect), ctypes.sizeof(rect))

        # this rect return the outer window, with titlebar and 4 side shadow.
        rect2 = ctypes.wintypes.RECT() 
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect2))

        # this returns the title bar rect, bottom would be the top of the inner window.
        title_info = TITLEBARINFO()
        title_info.cbSize = ctypes.sizeof(title_info)
        ctypes.windll.user32.GetTitleBarInfo(hwnd, ctypes.byref(title_info))

        return (rect.left, title_info.rcTitleBar.bottom, rect.right, rect.bottom) # return only inner window rect.
    
    def __detectAllSettings(self): ## This only support less than 2 monitor of same resolution from left to right arranged. left is the main monitor.
        innerWindow = self.__GetWindowRectFromName(self.gameTitleInput.text())
        left = innerWindow[0]
        top = innerWindow[1]
        right = innerWindow[2]
        bottom = innerWindow[3]
        width = innerWindow[2] - innerWindow[0]
        height = innerWindow[3] - innerWindow[1]
        getOverlay().resize((left, top, width, height))
        if (self.showDebugCheckbox.isChecked()):
            getOverlay().show()
        d = getDCapture().d
        d.display = d.displays[int(self.displayIndex.text())]
        if (left > d.displays[0].resolution[0]):
            self.displayIndex.setText(str(1))
            self.displayShiftX.setText(str(left - d.displays[0].resolution[0]))
        else:
            self.displayShiftX.setText(str(left))
        
        self.displayShiftY.setText(str(top))

        self.mouseShiftX.setText(str(left))
        self.mouseShiftY.setText(str(top))

        

    def __goToSelectDisplayShift(self): # NOT USED RN
        d = getDCapture()
        d.display = d.displays[int(self.displayIndex.text())]
        currentScreen = d.screenshot()
        fullScreenShot = cv2.cvtColor(currentScreen, cv2.COLOR_BGR2GRAY)
        selectFrameX = 400
        selectFrameY = 200
        enlargeFactor = 4
        selectFrame = fullScreenShot[0: selectFrameY, 0: selectFrameX]
        enlargedFrameSize = (selectFrameX * enlargeFactor, selectFrameY * enlargeFactor) # Choose the top left corner of the inner window.
        resized = cv2.resize(selectFrame, enlargedFrameSize, interpolation = cv2.INTER_AREA)
        resizedAddDot = cv2.circle(resized, (int(self.displayShiftX.text()) * enlargeFactor, int(self.displayShiftY.text()) * enlargeFactor),1, (255, 255, 255), -1)
        cv2.imshow("ChooseGameWindowTopLeftCorner", resizedAddDot )
        cv2.namedWindow('ChooseGameWindowTopLeftCorner', cv2.WINDOW_AUTOSIZE)
        def on_click(event, x, y, p1, p2):
            print(event)
            if event == cv2.EVENT_LBUTTONDOWN:
                print('mouse down')
                print(x)
                print(y)
                self.displayShiftX.setText(str(round(x / enlargeFactor)))
                self.displayShiftY.setText(str(round(y / enlargeFactor)))
                cv2.destroyWindow('ChooseGameWindowTopLeftCorner') 
        cv2.setMouseCallback('ChooseGameWindowTopLeftCorner', on_click)

    def __goToAddAcct(self):
        self.window = QtWidgets.QDialog()
        self.ui = UIAddAccountWindow(self.window)
        self.ui.show()

    def __deleteCurrentAcct(self):
        del getGlobalSetting().settings.accounts[self.acctDropdown.currentIndex()]
        getGlobalSetting().saveSettings()
        print("deleted account")
        self.loadSettings()

        
    def loadSettings(self):
        setting = getGlobalSetting().settings
        self.displayIndex.setText(str(setting.displayIndex))
        self.gameTitleInput.setText(setting.gameTitle)
        self.displayShiftX.setText(str(setting.displayShiftX))
        self.displayShiftY.setText(str(setting.displayShiftY))
        self.mouseShiftX.setText(str(setting.mouseShiftX))
        self.mouseShiftY.setText(str(setting.mouseShiftY))
        
        self.targetFPSInput.setText(str(setting.targetDisplayFPS or 20))
        self.centerFarDetectDistance.setText(
            str(setting.centerFarDetectDistance or 3 * (setting.lrDetectDistance or 10)))
        self.centerLowDetectDistance.setText(
            str(setting.centerLowDetectDistance or (setting.lrDetectDistance or 10)))
        
        self.lrDetectDistance.setText(str(setting.lrDetectDistance or 10))
        self.detectRadius.setText(str(setting.frontDetectDegree or 45))
        self.detectFPS.setText(str(setting.detectionFPS))
        self.showDebugCheckbox.setChecked(setting.showDebugWindow)
        self.checkStuckFrameCount.setText(
            str(setting.checkStuckFrameCount or 20))
        
        if setting.startScreen == 0:
            self.startScreenDropDown.setCurrentIndex(0)
        elif setting.startScreen == 4:
            self.startScreenDropDown.setCurrentIndex(1)
        elif setting.startScreen == 7:
            self.startScreenDropDown.setCurrentIndex(2)
        elif setting.startScreen == 10:
            self.startScreenDropDown.setCurrentIndex(3)
        elif setting.startScreen == 11:
            self.startScreenDropDown.setCurrentIndex(4)
        else:
            self.startScreenDropDown.setCurrentIndex(0)

        self.acctDropdown.clear()
        self.acctDropdown.addItems(str(i) + " - " + x.username for i,x in enumerate(setting.accounts))
            
        
        
    def saveSettings(self):
        setting = getGlobalSetting().settings
        setting.displayIndex = int(self.displayIndex.text())
        setting.gameTitle = self.gameTitleInput.text() or 'Crossout X.XX.XX.XXXXXX'
        setting.displayShiftX = int(self.displayShiftX.text())
        setting.displayShiftY = int(self.displayShiftY.text())
        setting.mouseShiftX = int(self.mouseShiftX.text())
        setting.mouseShiftY = int(self.mouseShiftY.text())
        setting.targetDisplayFPS = int(self.targetFPSInput.text()) or 20
        setting.centerFarDetectDistance = int(
            self.centerFarDetectDistance.text()) or 3 * (setting.lrDetectDistance or 10)
        setting.centerLowDetectDistance = int(
            self.centerLowDetectDistance.text()) or (setting.lrDetectDistance or 10)
        setting.lrDetectDistance = int(self.lrDetectDistance.text()) or 10
        setting.frontDetectDegree = int(self.detectRadius.text()) or 45
        setting.detectionFPS = int(self.detectFPS.text())
        setting.showDebugWindow = self.showDebugCheckbox.isChecked()
        setting.checkStuckFrameCount = int(
            self.checkStuckFrameCount.text()) or 20
        if self.startScreenDropDown.currentIndex() == 0:
            setting.startScreen = 0
        elif self.startScreenDropDown.currentIndex() == 1:
            setting.startScreen = 4
        elif self.startScreenDropDown.currentIndex() == 2:
            setting.startScreen = 7
        elif self.startScreenDropDown.currentIndex() == 3:
            setting.startScreen = 10
        elif self.startScreenDropDown.currentIndex() == 4:
            setting.startScreen = 11
        else:
            setting.startScreen = 0
        
        getGlobalSetting().saveSettings()
        self.close()
        
        
        
        
        
        
        
        
