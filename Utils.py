

from Constants import Point
from SettingsClass import getGlobalSetting
import threading
import time


def getCorrectPos(pos: Point) -> Point:
    return Point(int(getGlobalSetting().settings.mouseShiftX + pos.x), int(getGlobalSetting().settings.mouseShiftY + pos.y))


class setInterval:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()


def atLeastTwoTrue(a: bool, b: bool, c: bool):
    return a if a and (b or c) else (b and c)
