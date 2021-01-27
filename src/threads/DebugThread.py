
import cv2
from threading import Thread
import Constants as const
from DCaptureClass import getDCapture

#
# Thread for showing debug info in a cv2 window. 
# This thread is non blocking.
#
class DebugThread(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        self.isRunning = True
        self.mouseClickPos = None
        print("Debug Thread Init")

    def monitorImageClick(self, event, x, y, p1, p2):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouseClickPos = 'x: ' + str(x) + ' y: ' + str(y)

    def run(self):
        while self.isRunning:
            np_frame = getDCapture().getFrame(0)
            thisStep = const.findStepById(const.getRunningStepId())
            if (thisStep.area):
                np_frame = cv2.rectangle(np_frame, (thisStep.area.x, thisStep.area.y), (thisStep.area.xs, thisStep.area.ys), (0,255,0), 5) 
            if (thisStep.point):
                np_frame = cv2.circle(np_frame, (thisStep.point.x, thisStep.point.y), radius=5, color=(0, 0, 255), thickness=-1)
            if (self.mouseClickPos):
                np_frame = cv2.putText(np_frame, self.mouseClickPos, (50, 50) , cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0) , 2, cv2.LINE_AA) 
            # enlargedFrameSize = (960, 540) # Choose the top left corner of the inner window.
            # resizedFrame = cv2.resize(np_frame, enlargedFrameSize, interpolation = cv2.INTER_AREA)
            # cv2.imshow("Capture" + self.name, resizedFrame)
            cv2.imshow("Capture" + self.name, np_frame)
            cv2.setMouseCallback("Capture" + self.name, self.monitorImageClick)
            cv2.waitKey(1)
        print("Debug Thread Exit")
