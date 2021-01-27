


import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import time
from SettingsClass import getGlobalSetting

class UIAddAccountWindow(QtWidgets.QDialog):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("uis/ui_addaccount.ui", self)
        
        self.saveBtn.clicked.connect(self.__saveAccount)


    def __saveAccount(self):
        setting = getGlobalSetting().settings

        new_acct = setting.accounts.add()
        new_acct.username = self.usernameInput.text()
        new_acct.password = self.passwordInput.text()
        new_acct.playBattery = self.playForBatteryCB.isChecked()
        new_acct.playScrap = self.playForScrapCB.isChecked()
        new_acct.playWire = self.playForWireCB.isChecked()
        new_acct.playPatrol = self.playForPatrolCB.isChecked()

        getGlobalSetting().saveSettings()
        self.close()

    def __loadAccount(self): # implement a edit account feature.
        pass