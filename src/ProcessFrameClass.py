
from multiprocessing import Process, Value
import time
from DCaptureClass import getDCapture
from screens.LoginScreenClass import LoginScreen
import pytesseract
from Constants import DetectClickPair, Area, StepStatus, Point, findStepById, Step, loadNewUser, Action, getPassword, getUsername, getRunningStepId, setRunningStepId
import Constants as const
import d3dshot

from Utils import getCorrectPos
from threading import Thread
import cv2
import InputControl


class DebugThread(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        self.isRunning = True
        self.mouseClickPos = None

    def monitorImageClick(self, event, x, y, p1, p2):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouseClickPos = 'x: ' + str(x) + ' y: ' + str(y)

    def run(self):
        while self.isRunning:
            np_frame = getDCapture().getFrame(0)
            thisStep = const.findStepById(getRunningStepId())
            if (thisStep.area):
                np_frame = cv2.rectangle(np_frame, (thisStep.area.x, thisStep.area.y), (thisStep.area.xs, thisStep.area.ys), (0,255,0), 5) 
            if (thisStep.point):
                np_frame = cv2.circle(np_frame, (thisStep.point.x, thisStep.point.y), radius=5, color=(0, 0, 255), thickness=-1)
            if (self.mouseClickPos):
                np_frame = cv2.putText(np_frame, self.mouseClickPos, (50, 50) , cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0) , 1, cv2.LINE_AA) 
            # enlargedFrameSize = (960, 540) # Choose the top left corner of the inner window.
            # resizedFrame = cv2.resize(np_frame, enlargedFrameSize, interpolation = cv2.INTER_AREA)
            # cv2.imshow("Capture" + self.name, resizedFrame)
            cv2.imshow("Capture" + self.name, np_frame)
            cv2.setMouseCallback("Capture" + self.name, self.monitorImageClick)
            cv2.waitKey(1)

import random

class DetectClickThread(Thread):


    def __init__(self):
        Thread.__init__(self)
        self.isRunning = True
        self.isProcessingFrameIndication = False
        self.retryCount = 0

    def run(self):
        while self.isRunning:
            if (self.isProcessingFrameIndication == False):
                frame = getDCapture().getFrame(0)
                self.isProcessingFrameIndication = True
                step = findStepById(getRunningStepId())
                isSuccess = self.processThisFrame(frame, step, isFirst = self.retryCount == 0, randomizeData = self.retryCount > 5)
                if (isSuccess):
                    self.retryCount = 0
                    self.goToNextStep(isSuccess)
                else:
                    self.retryCount += 1
                    if (self.retryCount > 10):
                        self.retryCount = 0
                        self.goToNextStep(isSuccess)
                self.isProcessingFrameIndication = False



    def processThisFrame(self, frame, step: Step, isFirst: bool, randomizeData: bool):
        if (step.waitBefore > 0 and isFirst == True): # wait before timer will not trigger for subsequential retries.
            time.sleep(step.waitBefore)
        if (step.action == Action.textDetect):
            if (randomizeData == True):
                pixelMoveAround = [3,2,1,0,-1,-2,-3]
                if (self.__checkTextDetectionMatchString(frame, Area(
                    step.area.x + random.choice(pixelMoveAround),
                    step.area.y + random.choice(pixelMoveAround),
                    step.area.xs + random.choice(pixelMoveAround),
                    step.area.ys + random.choice(pixelMoveAround),
                ), step.strings) == False):
                    return False
            else:
                if (self.__checkTextDetectionMatchString(frame, step.area, step.strings) == False):
                    return False
            print("text detection executed")

        if (step.action == Action.mouseClick):
            InputControl.mouseClick(getCorrectPos(step.point))
            print("Mouse Click Action executed")

        if (step.action == Action.textInput):
            if getRunningStepId() == 'login_username_input':
                InputControl.fillInputWithString(const.getUsername())
            elif getRunningStepId() == 'login_password_input':
                InputControl.fillInputWithString(const.getPassword())
            else:
                InputControl.fillInputWithString(random.choice(step.strings))
            print("text input executed")

        if (step.waitAfter > 0):
            time.sleep(step.waitAfter)
        return True

    def __checkTextDetectionMatchString(self, frame, area: Area, expStrs: [str]) -> bool:
        crop_frame = frame[area.y:area.ys, area.x:area.xs]
        txt = pytesseract.image_to_string(crop_frame, lang='eng').lower()
        print(txt)
        for string in expStrs:
            if ((txt in string) or (string in txt)):
                print('text detection matched')
                return True
        print('text match failed')
        return False

    def goToNextStep(self, thisStepResult: bool):
        step = getRunningStepId()
        if step == 'login_disconnect_btn_text':
            setRunningStepId('login_disconnect_click')
        if step == 'login_disconnect_click':
            setRunningStepId('login_username_click')
        if step == 'login_username_click':
            setRunningStepId('login_username_input')
        if step == 'login_username_input':
            setRunningStepId('login_password_click')
        if step == 'login_password_click':
            setRunningStepId('login_password_input')
    


























class ProcessFrame(Process):
    def __init__(self, procIsDoneIndicator):
        super(ProcessFrame, self).__init__()
        self.procDone = procIsDoneIndicator

        self.dcap = d3dshot.create()
        
    def run(self):
        # self.frame = getDCapture().getFrame(0)
        self.dc = const.DetectClickPair(
            "Login Button",
            const.Area(const.login_label_width_start, const.login_label_height_start,
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