from screens.ScreenClass import Screen, ScreenStep
from Constants import DetectClickPair, Point
import time
from SettingsClass import getGlobalSetting
import random
from Utils import getCorrectPos
from InputControl import mouseClick, kbDown, kbUp, fillInputWithString


class MainMenuScreen(Screen):

    def __init__(self, screenStep: ScreenStep, crops: [DetectClickPair], allowedRetryCount: int, dcap):
        super().__init__(screenStep, crops, allowedRetryCount, dcap)

    def initMassEsc(self, n):
        i = 0
        while i < n:
            kbDown("esc")
            kbUp("esc")
            time.sleep(1)
