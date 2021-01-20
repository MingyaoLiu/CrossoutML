

from Constants import Point
from SettingsClass import getGlobalSetting
import threading
import time
import cv2


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

def imgRotate(image, angle, center = None, scale = 1.0):
    (h, w) = image.shape[:2]

    if center is None:
        center = (w / 2, h / 2)

    # Perform the rotation
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))

    return rotated