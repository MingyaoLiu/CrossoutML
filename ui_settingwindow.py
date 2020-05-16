



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
        self.targetFPSInput.setText(str(setting.targetDisplayFPS))
        
        self.detectDistance.setText(str(setting.frontDetectDistance))
        self.detectRadius.setText(str(setting.frontDetectDegree))
        self.detectFPS.setText(str(setting.detectionFPS))
        self.showDebugCheckbox.setChecked(setting.showDebugWindow)
        self.checkStuckFrameCount.setText(str(setting.checkStuckFrameCount))
        
        
    def saveSettings(self):
        setting = getGlobalSetting().settings
        setting.displayIndex = int(self.displayIndex.text())
        setting.shiftX = int(self.shiftX.text())
        setting.shiftY = int(self.shiftY.text())
        setting.targetDisplayFPS = int(self.targetFPSInput.text())
        setting.frontDetectDistance = int(self.targetFPSInput.text())
        setting.frontDetectDegree = int(self.detectRadius.text())
        setting.detectionFPS = int(self.detectFPS.text())
        setting.showDebugWindow = self.showDebugCheckbox.isChecked()
        setting.checkStuckFrameCount = int(self.checkStuckFrameCount.text())
        getGlobalSetting().saveSettings()
        self.close()
        
        
        
        
        
        
        
        
