import cv2
from SettingsClass import getGlobalSetting


class Debug():

    def __init__(self):
        print("INIT Debug Manager")
        self.debug_window_name = "DebugWindow"
        self.startedDebugger = False

    def createDebugWindow(self):
        if self.startedDebugger or getGlobalSetting().settings.showDebugWindow is False:
            pass
        else:
            self.startedDebugger = True
            cv2.namedWindow(
                self.debug_window_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(self.debug_window_name, 1280, 720)

    def closeDebugWindow(self):
        if self.startedDebugger:
            cv2.destroyWindow(self.debug_window_name)
            self.startedDebugger = False

    def debugDisplay(self, frame):
        if self.startedDebugger:
            cv2.imshow(self.debug_window_name, frame)


global_debugger = None


def getDebugger():
    global global_debugger
    if global_debugger:
        return global_debugger
    else:
        global_debugger = Debug()
        return global_debugger
