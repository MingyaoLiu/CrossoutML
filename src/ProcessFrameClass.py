
from multiprocess import Process, Value
import time
from DCaptureClass import getDCapture
from screens.LoginScreenClass import LoginScreen
import pytesseract
from Constants import ScreenStep, DetectClickPair, CropArea, StepStatus, Point
import Constants as const
import d3dshot

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

from threading import Thread
import cv2

exitFlag = 0

currentRunningStep = "login_btn"

class ProcessThread(Thread):
    def __init__(self, threadID, name, counter):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.isRunning = True

    def run(self):

        while self.isRunning:
            np_frame = getDCapture().getFrame(0)
            cv2.imshow("Capture" + self.name, np_frame)
            cv2.waitKey(1)


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

            image = cv2.rectangle(np_frame, (thisStep.area.x, thisStep.area.y), (thisStep.area.xs, thisStep.area.ys), (0,255,0), 5) 


            cv2.imshow("Capture" + self.name, image)
            cv2.setMouseCallback("Capture" + self.name, self.monitorImageClick)
            cv2.waitKey(1)





class DetectClickThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.isRunning = True
        self.isProcessingFrameIndication = Value('i', 1)
        self.pf = None

    def run(self):
        while self.isRunning:

            np_frame = getDCapture().getFrame(0)
            cv2.imshow("Capture" + self.name, np_frame)
            cv2.waitKey(1)


class VehicleControlThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.isRunning = True

    def run(self):

        while self.isRunning:
            
            print('a')