import cv2
from SettingsClass import getGlobalSetting


class Debug():

    def __init__(self):
        print("INIT Debug Manager")
        self.main_debug_window_name = "MainDebugWindow"
        self.secondary_debug_window_name = "SecondaryDebugWindow"
        self.third_debug_window_name = "ThirdDebugWindow"
        self.startedDebugger = False

    def createDebugWindow(self):
        if self.startedDebugger or getGlobalSetting().settings.showDebugWindow is False:
            pass
        else:
            self.startedDebugger = True
            cv2.namedWindow(
                self.main_debug_window_name, cv2.WINDOW_NORMAL)
            cv2.namedWindow(
                self.secondary_debug_window_name, cv2.WINDOW_NORMAL)
            cv2.namedWindow(
                self.third_debug_window_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(self.main_debug_window_name, 1280, 720)
            cv2.resizeWindow(self.secondary_debug_window_name, 640, 480)
            cv2.resizeWindow(self.third_debug_window_name, 480, 320)


    def closeDebugWindow(self):
        if self.startedDebugger:
            cv2.destroyWindow(self.main_debug_window_name)
            cv2.destroyWindow(self.secondary_debug_window_name)
            cv2.destroyWindow(self.third_debug_window_name)
            self.startedDebugger = False

    def debugDisplay(self, frame, window = "Main"):
        if self.startedDebugger:
            if window == "Third":
                cv2.imshow(self.third_debug_window_name, frame)
            elif window == "Second":
                cv2.imshow(self.secondary_debug_window_name, frame)
            else:
                cv2.imshow(self.main_debug_window_name, frame)


global_debugger = None


def getDebugger():
    global global_debugger
    if global_debugger:
        return global_debugger
    else:
        global_debugger = Debug()
        return global_debugger
