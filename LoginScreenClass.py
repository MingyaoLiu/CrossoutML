from ScreenClass import Screen, ScreenStep
from Constants import CropProperty
import time

class LoginScreen(Screen):

    def __init__(self, screenStep: ScreenStep, crops: [CropProperty], allowedRetryCount: int):
        super().__init__(screenStep, crops, allowedRetryCount)

        self.switchMinTimeSec = 3600
        self.currentAccount = None
        self.accountStartTime = time.time()

    def __checkIfSwitchAccount(self):
        if time.time() > self.accountStartTime + self.switchMinTimeSec:
            return True
        return False

    def __setRandomNewAccount(self):

        print("a")



