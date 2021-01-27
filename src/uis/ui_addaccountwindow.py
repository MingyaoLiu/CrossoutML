


import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import time
from SettingsClass import getGlobalSetting

class UIAddAccountWindow(QtWidgets.QDialog):
    
    def __init__(self, parent, index):
        super().__init__()
        uic.loadUi("uis/ui_addaccount.ui", self)

        self.index = None
        
        if index is not None:
            self.index = index
            self.__loadAccount()
        self.saveBtn.clicked.connect(self.__saveAccount)

    def __saveAccount(self):
        setting = getGlobalSetting().settings

        if self.index is not None:
            acct = setting.accounts[self.index]
            acct.username = self.usernameInput.text()
            acct.password = self.passwordInput.text()
            acct.playBattery = self.playForBatteryCB.isChecked()
            acct.playScrap = self.playForScrapCB.isChecked()
            acct.playWire = self.playForWireCB.isChecked()
            acct.playPatrol = self.playForPatrolCB.isChecked()
        else:
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
        setting = getGlobalSetting().settings
        acct = setting.accounts[self.index]
        self.usernameInput.setText(acct.username)
        self.passwordInput.setText(acct.password)
        self.playForBatteryCB.setChecked(acct.playBattery)
        self.playForScrapCB.setChecked(acct.playScrap)
        self.playForWireCB.setChecked(acct.playWire)
        self.playForPatrolCB.setChecked(acct.playPatrol)