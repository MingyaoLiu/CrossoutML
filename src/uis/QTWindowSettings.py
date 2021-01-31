import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import time
from SettingsClass import getGlobalSetting
from uis.ui_addaccountwindow import UIAddAccountWindow
import cv2
from uis.QTWindowOverlay import getOverlay
from DCaptureClass import getDCapture
import Constants as const
import Utils

class UI_SettingWindow(QtWidgets.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("uis/QTWindowSettingsUI.ui", self)
        self.loadSettings()
        self.saveBtn.clicked.connect(self.saveSettings)
        self.addAcctBtn.clicked.connect(self.__goToAddAcct)
        self.EditAccountBtn.clicked.connect(self.__editAcct)
        self.delAcctBtn.clicked.connect(self.__deleteCurrentAcct)
        self.detectAllSettingBtn.clicked.connect(self.__detectAllSettings)
    
    def __detectAllSettings(self):
        getGlobalSetting().updateDisplayMouseShift()
        getGlobalSetting().saveSettings()

    def __goToAddAcct(self):
        self.window = QtWidgets.QDialog()
        self.ui = UIAddAccountWindow(self.window, None)
        self.ui.show()

    def __editAcct(self):
        index = self.acctDropdown.currentIndex()
        self.ui = UIAddAccountWindow(self.window, index)
        self.ui.show()

    def __deleteCurrentAcct(self):
        del getGlobalSetting().settings.accounts[self.acctDropdown.currentIndex()]
        getGlobalSetting().saveSettings()
        print("deleted account")
        self.loadSettings()

        
    def loadSettings(self):
        setting = getGlobalSetting().settings

        self.acctDropdown.clear()
        self.acctDropdown.addItems(str(i) + " - " + (x.ign if x.ign != '' else x.username) for i,x in enumerate(setting.accounts))

        self.startScreenDropDown.clear()
        self.stepIds = [val.id for val in const.Steps]
        self.startScreenDropDown.addItems(self.stepIds)
        if (setting.startScreen is not None):
            self.startScreenDropDown.setCurrentIndex(setting.startScreen)
        else:
            self.startScreenDropDown.setCurrentIndex(0)

        self.targetFPSInput.setText(str(setting.targetDisplayFPS))
        self.displayIndexInput.setText(str(setting.displayIndex))
        self.gameTitleInput.setText(setting.gameTitle)
        self.autoUpdateWindowSettingCheckbox.setChecked(setting.autoDetect)

        self.displayShiftXInput.setText(str(setting.displayShiftX))
        self.displayShiftYInput.setText(str(setting.displayShiftY))
        self.mouseShiftXInput.setText(str(setting.mouseShiftX))
        self.mouseShiftYInput.setText(str(setting.mouseShiftY))

        self.showDetectClickCB.setChecked(setting.showDetectClickDebugWindow)
        self.showMapTrackingCB.setChecked(setting.showMapTrackingDebugWindow)
        self.showMinimapDebugWindowCB.setChecked(setting.showMinimapTrackingDebugWindow)
        self.showOverlayWindowCB.setChecked(setting.showOverlay)

        self.centerDetectDistanceInput.setText(str(setting.centerDetectDistance))
        self.lrDetectDistanceInput.setText(str(setting.lrDetectDistance))
        self.detectRadiusInput.setText(str(setting.frontDetectDegree))
        self.speedMinInput.setText(str(setting.carMinSpeed))
        self.speedMaxInput.setText(str(setting.carMaxSpeed))
        self.enemyDetectSizeAdjustInput.setText(str(setting.enemyDetectionSizeMidifier))

        self.takeTurnHoldADDurationInput.setText(format(setting.turnHoldDuration, '.2f'))
        self.afterTurnWaitForNextCalcDurationInput.setText(format(setting.turnAfterWaitDuration, '.2f'))
        self.speedChangeHoldKeyDurationInput.setText(format(setting.speedHoldDuration, '.2f'))
        self.afterSpeedChangeWaitDurationInput.setText(format(setting.speedAfterWaitDuration, '.2f'))
        self.fullStuckForceResetTimerInput.setText(str(setting.fullStuckTimer))

        self.weaponDeployKeyInput.setText(setting.weaponKey)
        self.selfExplodeKeyInput.setText(setting.selfExplodeKey)
        self.calloutKeyInput.setText(setting.calloutKeys)
        self.chatKeywordInput.setText(setting.chatDetectKeywords)

        
    def saveSettings(self):
        setting = getGlobalSetting().settings

        setting.startScreen = self.startScreenDropDown.currentIndex()

        setting.displayIndex = int(self.displayIndexInput.text())
        setting.targetDisplayFPS = int(self.targetFPSInput.text())
        setting.gameTitle = self.gameTitleInput.text()
        setting.autoDetect = self.autoUpdateWindowSettingCheckbox.isChecked()

        setting.displayShiftX = int(self.displayShiftXInput.text())
        setting.displayShiftY = int(self.displayShiftYInput.text())
        setting.mouseShiftX = int(self.mouseShiftXInput.text())
        setting.mouseShiftY = int(self.mouseShiftYInput.text())

        setting.showDetectClickDebugWindow = self.showDetectClickCB.isChecked()
        setting.showMapTrackingDebugWindow = self.showMapTrackingCB.isChecked()
        setting.showMinimapTrackingDebugWindow = self.showMinimapDebugWindowCB.isChecked()
        setting.showOverlay = self.showOverlayWindowCB.isChecked()

        setting.centerDetectDistance = int(self.centerDetectDistanceInput.text())
        setting.lrDetectDistance = int(self.lrDetectDistanceInput.text())
        setting.frontDetectDegree = int(self.detectRadiusInput.text())
        setting.carMinSpeed = int(self.speedMinInput.text())
        setting.carMaxSpeed = int(self.speedMaxInput.text())
        setting.enemyDetectionSizeMidifier = int(self.enemyDetectSizeAdjustInput.text())

        setting.turnHoldDuration = float(self.takeTurnHoldADDurationInput.text())
        setting.turnAfterWaitDuration = float(self.afterTurnWaitForNextCalcDurationInput.text())
        setting.speedHoldDuration = float(self.speedChangeHoldKeyDurationInput.text())
        setting.speedAfterWaitDuration = float(self.afterSpeedChangeWaitDurationInput.text())
        setting.fullStuckTimer = int(self.fullStuckForceResetTimerInput.text())


        setting.weaponKey = self.weaponDeployKeyInput.text()
        setting.selfExplodeKey = self.selfExplodeKeyInput.text()
        setting.calloutKeys = self.calloutKeyInput.text()
        setting.chatDetectKeywords = self.chatKeywordInput.text()

        getGlobalSetting().saveSettings()
        self.close()
        