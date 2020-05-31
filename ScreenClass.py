import time
import InputControl
import pytesseract
from Constants import ScreenStep, CropProperty, CropArea, topTitleBarHeight
from Utils import getCorrectPos
from SettingsClass import getGlobalSetting
from DebugClass import getDebugger


class Screen():

    def __init__(self, screenStep: ScreenStep, crops: [CropProperty], allowedRetryCount: int):
        self.screenStep = screenStep
        self.crops = crops
        self.allowedRetryCount = allowedRetryCount
        self.retryCount = 0

    def checkSingleSatisfy(self, frame, index) -> (bool, str):
        crop = self.crops[index]
        heightShift = topTitleBarHeight if getGlobalSetting(
        ).settings.isFullScreen else 0
        crop_frame = frame[crop.area.y - heightShift:crop.area.ys -
                           heightShift, crop.area.x:crop.area.xs]
        getDebugger().debugDisplay(crop_frame, "Third")

        low_txt = pytesseract.image_to_string(crop_frame, lang='eng').lower()
        print(low_txt)
        if crop.requiredMatch and (low_txt not in crop.expectedStrs):
            return (False, low_txt)
        return (True, low_txt)

    def checkSatisfy(self, frame) -> bool:
        for i in range(len(self.crops)):
            if self.checkSingleSatisfy(frame, i)[0]:
                pass
            else:
                return False
        print("Step", self.screenStep.name, ">>>> SATISFIED")
        return True

    def executeSingleClick(self, index):
        crop = self.crops[index]
        if crop.willClick:
            InputControl.mouseClick(getCorrectPos(crop.clickPos))
            time.sleep(crop.clickWaitTime)

    def executeClick(self):
        for i in range(len(self.crops)):
            self.executeSingleClick(i)

    def addFailCount(self) -> bool:
        if self.retryCount != 0 and self.retryCount % 100 == 0:
            print("Retrying Step: ", self.screenStep.name, self.retryCount)
        self.retryCount += 1
        if self.retryCount >= self.allowedRetryCount:
            print("Step", self.screenStep.name, ">>>> FAILED")
            return False
        return True

    def resetRetryCount(self):
        self.retryCount = 0
