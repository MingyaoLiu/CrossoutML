


import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import time
from SettingsClass import getGlobalSetting

class UIAddAccountWindow(QtWidgets.QDialog):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui_addaccount.ui", self)
        
        self.saveBtn.clicked.connect(self.__saveAccount)
        


    def __saveAccount(self):
        setting = getGlobalSetting().settings
        # acct_proto = getGlobalSetting().acct_proto

        new_acct = setting.accounts.add()
        new_acct.username = self.usernameInput.text()
        new_acct.password = self.passwordInput.text()

        getGlobalSetting().saveSettings()
        self.close()


        print("save")