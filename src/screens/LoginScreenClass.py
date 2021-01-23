from screens.ScreenClass import Screen, ScreenStep
from Constants import DetectClickPair, Point
import time
from SettingsClass import getGlobalSetting
import random
from Utils import getCorrectPos
from InputControl import mouseClick, kbDown, kbUp, fillInputWithString
import Constants as const

class LoginScreen(Screen):

    def __init__(self, dcap):

        super().__init__(ScreenStep.Login, const.login_crops, 10, dcap)

        self.switchMinTimeSec = 3600
        # self.switchMinTimeSec = 1
        self.currentAccount = None
        self.accountStartTime = time.time()
        self.setRandomNewAccount()

    def checkIfSwitchAccount(self):
        if time.time() > self.accountStartTime + self.switchMinTimeSec:
            return True
        return False

    def setRandomNewAccount(self):
        accounts = getGlobalSetting().settings.accounts
        if accounts:
            new_acct = random.choice(list(accounts))
            while new_acct == self.currentAccount:
                new_acct = random.choice(list(accounts))
                print("same account")
            self.currentAccount = new_acct
            self.accountStartTime = time.time()
            print(self.currentAccount)

    def fillUsername(self):
        usenameInputPos = getCorrectPos(Point(190,360))
        mouseClick(usenameInputPos)
        time.sleep(0.05)
        fillInputWithString(self.currentAccount.username)

    def fillPassword(self):
        passwordInputPos = getCorrectPos(Point(200,430))
        mouseClick(passwordInputPos)
        time.sleep(0.05)
        fillInputWithString(self.currentAccount.password)
