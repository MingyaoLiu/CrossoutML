

from Constants import Point
from SettingsClass import getGlobalSetting


def getCorrectPos(pos: Point) -> Point:
    return Point(int(getGlobalSetting().settings.shiftX + pos.x), int(getGlobalSetting().settings.shiftY + pos.y))
