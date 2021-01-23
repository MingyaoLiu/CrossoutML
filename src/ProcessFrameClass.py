
from multiprocessing import Process, Value
import time
from DCaptureClass import getDCapture
from screens.LoginScreenClass import LoginScreen
import pytesseract
from Constants import ScreenStep, DetectClickPair, CropArea, StepStatus, Point
import Constants as const
import d3dshot

from Utils import getCorrectPos
from threading import Thread
import cv2
import InputControl

currentRunningStep = "login_btn"

class DebugThread(Thread):
    
    global currentRunningStep

    def __init__(self):
        Thread.__init__(self)
        self.isRunning = True

    def monitorImageClick(self, event, x, y, p1, p2):
        if event == cv2.EVENT_LBUTTONDOWN:
            print('mouse down on:')
            print((x, y))

    def run(self):

        while self.isRunning:
            np_frame = getDCapture().getFrame(0)

            thisStep = const.DetailStep[currentRunningStep]

            if (thisStep.area):
                np_frame = cv2.rectangle(np_frame, (thisStep.area.x, thisStep.area.y), (thisStep.area.xs, thisStep.area.ys), (0,255,0), 5) 
            if (thisStep.clickPos):
                np_frame = cv2.circle(np_frame, (thisStep.clickPos.x, thisStep.clickPos.y), radius=3, color=(0, 0, 255), thickness=-1)
            
            # enlargedFrameSize = (960, 540) # Choose the top left corner of the inner window.
            # resizedFrame = cv2.resize(np_frame, enlargedFrameSize, interpolation = cv2.INTER_AREA)
            # cv2.imshow("Capture" + self.name, resizedFrame)
            cv2.imshow("Capture" + self.name, np_frame)
            cv2.setMouseCallback("Capture" + self.name, self.monitorImageClick)
            cv2.waitKey(1)



import random

class DetectClickThread(Thread):

    global currentRunningStep

    def __init__(self):
        Thread.__init__(self)
        self.isRunning = True
        self.isProcessingFrameIndication = False

        self.retryCount = 0

    def run(self):
        while self.isRunning:
            frame = getDCapture().getFrame(0)
            
            if (self.isProcessingFrameIndication == False):
                self.isProcessingFrameIndication = True
                
                step = const.DetailStep[currentRunningStep] # CHANGE

                isSuccess = self.processThisFrame(frame, step, self.retryCount < 5)

                if (isSuccess):
                    self.retryCount = 0
                    pass #Update the current step global variable
                else:
                    self.retryCount += 1
                    if (self.retryCount >= 10):
                        self.retryCount = 0
                        pass # DETERMINE THE MAX FAIL LOGIC

                self.isProcessingFrameIndication = True


    def processThisFrame(self, frame, step, randomizeData: bool):
        if (step.waitBeforeDetect > 0):
            time.sleep(step.waitBeforeDetect)
        if (step.area):
            if randomizeData:
                
            if self.__checkSingleSatisfy(frame, step.area, step.expectedStrs) == False:
                return False
        if (step.waitBeforeClick > 0):
            time.sleep(step.waitBeforeClick)
        if (step.clickPos):
            InputControl.mouseClick(getCorrectPos(step.clickPos))
        return True

    def __checkSingleSatisfy(self, frame, area: CropArea, expStrs: [str]) -> bool:
        crop_frame = frame[area.y:area.ys, area.x:area.xs]
        low_txt = pytesseract.image_to_string(crop_frame, lang='eng').lower()
        print(low_txt)
        if (low_txt not in expStrs):
            return False
        return True

    def goToNextStep(self, thisStepResult: bool):
        if this.currentRunningStep
    

class ProcessFrame(Process):
    def __init__(self, procIsDoneIndicator):
        super(ProcessFrame, self).__init__()
        self.procDone = procIsDoneIndicator

        self.dcap = d3dshot.create()
        
    def run(self):
        # self.frame = getDCapture().getFrame(0)
        self.dc = const.DetectClickPair(
            "Login Button",
            const.CropArea(const.login_label_width_start, const.login_label_height_start,
                            const.login_label_width_end, const.login_label_height_end),
            True,
            const.Point(const.login_label_trigger_pos_x, const.login_label_trigger_pos_y),
            True,
            ["login", "log in", "log ln", "logln"],
            10,
            1
        )
        self.__checkSingleSatisfy()
        self.procDone.value = 1


    def __checkSingleSatisfy(self) -> (bool):
        frame = self.dcap.get_frame(0)
        print(frame)
        crop_frame = frame[self.dc.area.y:self.dc.area.ys, self.dc.area.x:self.dc.area.xs]
        low_txt = pytesseract.image_to_string(crop_frame, lang='eng').lower()
        print(low_txt)
        if self.dc.requiredMatch and (low_txt not in self.dc.expectedStrs):
            return False
        return True


class VehicleControlThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.isRunning = True

    def run(self):

        while self.isRunning:
            
            print('a')