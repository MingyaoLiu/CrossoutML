


import d3dshot
from SettingsClass import getGlobalSetting
import Constants as const

dcapture = None

def getDCapture() :
    global dcapture
    if (dcapture):
        return dcapture
    else:
        dcapture = DCaptureClass()
        return dcapture

class DCaptureClass:
    
    def __init__(self):
        self.d = d3dshot.create(capture_output='numpy')

    def startCapture(self):
        self.stopCapture()
        fps = getGlobalSetting().settings.targetDisplayFPS or 20
        self.d.display = self.d.displays[getGlobalSetting().settings.displayIndex or 0]
        displayShiftX = getGlobalSetting().settings.displayShiftX
        displayShiftY = getGlobalSetting().settings.displayShiftY
        self.d.capture(target_fps=fps, region=(displayShiftX, displayShiftY, const.screenWidth, const.screenHeight))

    def stopCapture(self):
        self.d.stop()


    def getFrame(self, previous_n: int):
        if (previous_n != 0):
            return self.d.get_frame(previous_n)
        else:
            return self.d.get_latest_frame()