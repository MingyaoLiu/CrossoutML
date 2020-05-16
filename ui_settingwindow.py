



import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import time
from SettingsClass import getGlobalSetting

class UI_SettingWindow(QtWidgets.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("settingwindow.ui", self)
        self.loadSettings()
        
        self.saveBtn.clicked.connect(self.saveSettings)
        
        
        
    def loadSettings(self):
        setting = getGlobalSetting().settings
        self.displayIndex.setText(str(setting.displayIndex))
        self.shiftX.setText(str(setting.shiftX))
        self.shiftY.setText(str(setting.shiftY))
        self.targetFPSInput.setText(str(setting.targetDisplayFPS or 20))
        
        self.detectDistance.setText(str(setting.frontDetectDistance or 10))
        self.detectRadius.setText(str(setting.frontDetectDegree or 45))
        self.detectFPS.setText(str(setting.detectionFPS))
        self.showDebugCheckbox.setChecked(setting.showDebugWindow)
        self.checkStuckFrameCount.setText(
            str(setting.checkStuckFrameCount or 20))
        
        
    def saveSettings(self):
        setting = getGlobalSetting().settings
        setting.displayIndex = int(self.displayIndex.text())
        setting.shiftX = int(self.shiftX.text())
        setting.shiftY = int(self.shiftY.text())
        setting.targetDisplayFPS = int(self.targetFPSInput.text()) or 20
        setting.frontDetectDistance = int(self.detectDistance.text()) or 10
        setting.frontDetectDegree = int(self.detectRadius.text()) or 45
        setting.detectionFPS = int(self.detectFPS.text())
        setting.showDebugWindow = self.showDebugCheckbox.isChecked()
        setting.checkStuckFrameCount = int(
            self.checkStuckFrameCount.text()) or 20
        getGlobalSetting().saveSettings()
        self.close()
        
        
        
        
        
        
        
        
