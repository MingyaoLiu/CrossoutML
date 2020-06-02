from ScreenClass import Screen, ScreenStep
from Constants import CropProperty, Point
import time
from SettingsClass import getGlobalSetting
import random
from Utils import getCorrectPos
from InputControl import mouseClick, kbDown, kbUp, fillInputWithString

class LoginScreen(Screen):

    def __init__(self, screenStep: ScreenStep, crops: [CropProperty], allowedRetryCount: int):
        super().__init__(screenStep, crops, allowedRetryCount)

        # self.switchMinTimeSec = 3600
        self.switchMinTimeSec = 1
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
            self.currentAccount = random.choice(accounts)
            self.accountStartTime = time.time()
            print(self.currentAccount)

    def fillUsername(self):
        usenameInputPos = getCorrectPos(Point(190,360))
        mouseClick(usenameInputPos)
        time.sleep(0.1)
        fillInputWithString(self.currentAccount.username)

    def fillPassword(self):
        passwordInputPos = getCorrectPos(Point(200,430))
        mouseClick(passwordInputPos)
        time.sleep(0.1)
        fillInputWithString(self.currentAccount.password)