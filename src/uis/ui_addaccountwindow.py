


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

        thisAccount = None
        if self.index is not None:
            thisAccount = setting.accounts[self.index]
        else:
            thisAccount = setting.accounts.add()
            
        thisAccount.username = self.usernameInput.text()
        thisAccount.password = self.passwordInput.text()
        thisAccount.playBattery = self.playForBatteryCB.isChecked()
        thisAccount.playScrap = self.playForScrapCB.isChecked()
        thisAccount.playWire = self.playForWireCB.isChecked()
        thisAccount.playPatrol = self.playForPatrolCB.isChecked()
        thisAccount.ign = self.inGameNameInput.text()
        thisAccount.enabled = self.enabledForBottingCB.isChecked()

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
        self.inGameNameInput.setText(acct.ign)
        self.enabledForBottingCB.setChecked(acct.enabled)