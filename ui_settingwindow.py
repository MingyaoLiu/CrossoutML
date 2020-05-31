



import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import time
from SettingsClass import getGlobalSetting
from ui_addaccountwindow import UIAddAccountWindow
from operator import itemgetter

class UI_SettingWindow(QtWidgets.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("settingwindow.ui", self)
        self.loadSettings()
        
        self.saveBtn.clicked.connect(self.saveSettings)
        
        self.addAcctBtn.clicked.connect(self.__goToAddAcct)
        self.delAcctBtn.clicked.connect(self.__deleteCurrentAcct)


    def __goToAddAcct(self):
        self.window = QtWidgets.QDialog()
        self.ui = UIAddAccountWindow(self.window)
        self.ui.show()

    def __deleteCurrentAcct(self):
        del getGlobalSetting().settings.accounts[self.acctDropdown.currentIndex()]
        getGlobalSetting().saveSettings()
        print("delete")
        self.loadSettings()

        
    def loadSettings(self):
        setting = getGlobalSetting().settings
        self.displayIndex.setText(str(setting.displayIndex))
        self.displayShiftX.setText(str(setting.displayShiftX))
        self.displayShiftY.setText(str(setting.displayShiftY))
        self.mouseShiftX.setText(str(setting.mouseShiftX))
        self.mouseShiftY.setText(str(setting.mouseShiftY))
        self.isFullScreenCheckbox.setChecked(setting.isFullScreen)
        
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
        setting.displayShiftX = int(self.displayShiftX.text())
        setting.displayShiftY = int(self.displayShiftY.text())
        setting.mouseShiftX = int(self.mouseShiftX.text())
        setting.mouseShiftY = int(self.mouseShiftY.text())
        setting.isFullScreen = self.isFullScreenCheckbox.isChecked()
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
        
        
        
        
        
        
        
        
