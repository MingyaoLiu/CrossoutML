from screens.ScreenClass import Screen, ScreenStep
from Constants import CropProperty, Point
import time
from SettingsClass import getGlobalSetting
import random
from Utils import getCorrectPos
from InputControl import mouseClick, kbDown, kbUp, fillInputWithString


class MainMenuScreen(Screen):

    def __init__(self, screenStep: ScreenStep, crops: [CropProperty], allowedRetryCount: int):
        super().__init__(screenStep, crops, allowedRetryCount)

    def initMassEsc(self, n):
        i = 0
        while i < n:
            kbDown("esc")
            kbUp("esc")
            time.sleep(1)
