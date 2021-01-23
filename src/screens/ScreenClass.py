import time
import InputControl
import pytesseract
from Constants import ScreenStep, DetectClickPair, CropArea, StepStatus
from Utils import getCorrectPos
from SettingsClass import getGlobalSetting
from DebugClass import getDebugger
from DCaptureClass import getDCapture, DCaptureClass

class Screen():

    def __init__(self, screenStep: ScreenStep, crops: [DetectClickPair], allowedRetryCount: int, dcap):
        self.screenStep = screenStep
        self.crops = crops
        self.allowedRetryCount = allowedRetryCount
        self.retryCount = 0
        self.stepStatus = StepStatus.unknown

        self.isExecuting = False
        self.lastExecuteInnerStepIndex = -1
        
        self.dcap = dcap


    def checkSingleSatisfy(self, frame, index) -> (bool, str):
        crop = self.crops[index]
        crop_frame = frame[crop.area.y:crop.area.ys, crop.area.x:crop.area.xs]
        getDebugger().debugDisplay(crop_frame, "Third")

        low_txt = pytesseract.image_to_string(crop_frame, lang='eng').lower()
        print(low_txt)
        if crop.requiredMatch and (low_txt not in crop.expectedStrs):
            self.isExecuting = False
            return (False, low_txt)

        if not crop.willClick:
            self.isExecuting = False
        return (True, low_txt)

    def executeSingleClick(self, index):
        crop = self.crops[index]
        if crop.willClick:
            InputControl.mouseClick(getCorrectPos(crop.clickPos))
            self.lastExecuteInnerStepIndex = index


    def updateStepStatus(self, newStatus: StepStatus):
        self.stepStatus = newStatus

    # NEW
    def __checkSingleSatisfy(self, data: DetectClickPair) -> (bool):
        frame = self.dcap.get_frame(0)
        print(data.area)
        print(frame)
        crop_frame = frame[data.area.y:data.area.ys, data.area.x:data.area.xs]
        low_txt = pytesseract.image_to_string(crop_frame, lang='eng').lower()
        if data.requiredMatch and (low_txt not in data.expectedStrs):
            return False
        return True


    def processScreen(self):

        for data in self.crops:
            if (data.waitBeforeDetect > 0):
                time.sleep(data.waitBeforeDetect)
            isDetected = self.__checkSingleSatisfy(data)
            
            while (isDetected == False and self.retryCount < self.allowedRetryCount):
                isDetected = self.__checkSingleSatisfy(data)
                self.retryCount += 1
            
            if (isDetected == False):
                return False

            if (data.waitBeforeClick > 0):
                time.sleep(data.waitBeforeClick)
            
            if data.willClick:
                InputControl.mouseClick(getCorrectPos(data.clickPos))
            
        return True


    # DONOT USE FOR NOW
    def checkSatisfy(self, frame) -> bool:
        for i in range(len(self.crops)):
            if self.checkSingleSatisfy(frame, i)[0]:
                pass
            else:
                return False
        print("Step", self.screenStep.name, ">>>> SATISFIED")
        return True

    # DONOT USE
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
    # DONOT USE
    def resetRetryCount(self):
        self.retryCount = 0
