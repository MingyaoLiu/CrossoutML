
import crossml_pb2
from os import path
import ctypes
import win32con as wcon
import win32api as wapi
import win32gui as wgui
import win32process as wproc
import wmi
import random
from Constants import Steps
import d3dshot

class Settings(object):

    def __init__(self):
        self.settings = crossml_pb2.CrossoutMLSetting()
        self.acct_proto = crossml_pb2.CrossoutMLAccount()
        self.getSettingsFile()

    def getSettingsFile(self):
        if path.exists('settings.bin'):
            with open('settings.bin', 'rb') as f:
                self.settings.ParseFromString(f.read())
                f.close()
        else:
            self.settings = crossml_pb2.CrossoutMLSetting()
            self.__initDefaultValue()
            self.saveSettings()

    def __initDefaultValue(self):

        self.startScreen = 0
        self.updateDisplayMouseShift()
        self.settings.autoDetect = True
        self.settings.targetDisplayFPS = 30
        self.settings.showOverlay = False
        self.settings.showDetectClickDebugWindow = False
        self.settings.showMapTrackingDebugWindow = False
        self.settings.showMinimapTrackingDebugWindow = False
        self.settings.centerDetectDistance = 20
        self.settings.lrDetectDistance = 15
        self.settings.frontDetectDegree = 35
        self.settings.carMinSpeed = 30
        self.settings.carMaxSpeed = 40
        self.settings.enemyDetectionSizeMidifier = -40
        self.settings.turnHoldDuration = 0.15
        self.settings.turnAfterWaitDuration = 0.2
        self.settings.speedHoldDuration = 0.15
        self.settings.speedAfterWaitDuration = 0.05
        self.settings.fullStuckTimer = 600
        self.settings.weaponKey = '1'
        self.settings.selfExplodeKey = 'backspace'
        self.settings.calloutKeys = 'b,x,z,j,m,k'
        self.settings.chatDetectKeywords = 'bot,daddyplz'

        

    def updateDisplayMouseShift(self, gameTitle=None):
        # update general display settings
        applicationName = None
        if gameTitle:
            applicationName = gameTitle
        else:
            applicationName = getCrossoutWindowName()
        if applicationName:
            self.settings.gameTitle = applicationName
            innerWindow = getWindowRectFromName(applicationName)
            if innerWindow:
                left = innerWindow[0]
                top = innerWindow[1]
                right = innerWindow[2]
                bottom = innerWindow[3]
                width = innerWindow[2] - innerWindow[0]
                height = innerWindow[3] - innerWindow[1]
                d = d3dshot.create(capture_output='numpy')
                if (len(d.displays) > 1):
                    # TODO: support multiple monitor in different arrangement. currently only 2 of the SAME monitor either horizontal or vertical arranged.
                    if (left > d.displays[0].resolution[0]): # game window is on right monitor
                        print("2 monitor arranged left right, game on right.")
                        self.settings.displayIndex = 1 # left is main, this needs to be changed
                        self.settings.displayShiftX = left - d.displays[0].resolution[0]
                        self.settings.displayShiftY = top
                    elif (top > d.displays[1].resolution[1]):
                        print("2 monitor arranged top bottom, game on bottom.")
                        self.settings.displayIndex = 0 # bottom is main, nobody do top main right
                        self.settings.displayShiftX = left
                        self.settings.displayShiftY = top - d.displays[1].resolution[1]
                    else:
                        print("game is on top left monitor, or only 1 monitor")
                        self.settings.displayIndex = 0
                        self.settings.displayShiftX = left
                        self.settings.displayShiftY = top
                else:
                    self.settings.displayIndex = 0
                    self.settings.displayShiftX = left
                    self.settings.displayShiftY = top
                
                self.settings.mouseShiftX = left
                self.settings.mouseShiftY = top
            else:
                print('cannot determine game window position.')


    def getSettings(self):
        return self.settings

    def saveSettings(self):
        settingsFile = open("settings.bin", "wb")
        settingsFile.write(self.settings.SerializeToString())
        settingsFile.close()


global_settings = None


def getGlobalSetting():
    global global_settings
    if global_settings:
        return global_settings
    else:
        global_settings = Settings()
        return global_settings

def getSettings():
    global global_settings
    if global_settings:
        return global_settings.getSettings()
    else:
        global_settings = Settings()
        return global_settings.getSettings()

def saveSettings():
    global global_settings
    if global_settings:
        global_settings.saveSettings()
    else:
        global_settings = Settings()


currentRunningStep = None

def getRunningStepId():
    global currentRunningStep
    if currentRunningStep:
        return currentRunningStep
    else:
        if getGlobalSetting().settings.startScreen is not None:
            currentRunningStep = Steps[getGlobalSetting().settings.startScreen].id
        else:
            currentRunningStep =  Steps[0].id
        return currentRunningStep

def setRunningStepId(id: str):
    global currentRunningStep
    currentRunningStep = id



# Get Crossout Window Name Automatically
def enum_windows_proc(wnd, param):
    pid = param.get("pid", None)
    data = param.get("data", None)
    if pid is None or wproc.GetWindowThreadProcessId(wnd)[1] == pid:
        text = wgui.GetWindowText(wnd)
        if text:
            style = wapi.GetWindowLong(wnd, wcon.GWL_STYLE)
            if style & wcon.WS_VISIBLE:
                if data is not None:
                    data.append((wnd, text))
                #else:
                    #print("%08X - %s" % (wnd, text))


def enum_process_windows(pid=None):
    data = []
    param = {
        "pid": pid,
        "data": data,
    }
    wgui.EnumWindows(enum_windows_proc, param)
    return data

def getCrossoutWindowName():
    f = wmi.WMI()
    crossoutProcess = None
    for process in f.Win32_Process():
        if ('Crossout' in process.name):
            print(process.ProcessId)
            crossoutProcess = process
            break

    if crossoutProcess is not None:
        data = enum_process_windows(crossoutProcess.ProcessId)
        if data:
            for _, text in data:
                return text
    return None

class TITLEBARINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.wintypes.DWORD), ("rcTitleBar", ctypes.wintypes.RECT),
                ("rgstate", ctypes.wintypes.DWORD * 6)]

# Get crossout window size
def getWindowRectFromName(name:str)-> tuple:
        hwnd = ctypes.windll.user32.FindWindowW(0, name)

        # This rect return the window rect with titlebar but no shadow.
        rect = ctypes.wintypes.RECT()
        foundwindow = ctypes.windll.dwmapi.DwmGetWindowAttribute
        if foundwindow:
            rect = ctypes.wintypes.RECT()
            DWMWA_EXTENDED_FRAME_BOUNDS = 9
            foundwindow(
                hwnd,
                ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
                ctypes.byref(rect), ctypes.sizeof(rect))

        # this rect return the outer window, with titlebar and 4 side shadow.
        rect2 = ctypes.wintypes.RECT() 
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect2))

        # this returns the title bar rect, bottom would be the top of the inner window.
        title_info = TITLEBARINFO()
        title_info.cbSize = ctypes.sizeof(title_info)
        ctypes.windll.user32.GetTitleBarInfo(hwnd, ctypes.byref(title_info))

        return (rect.left, title_info.rcTitleBar.bottom, rect.right, rect.bottom) # return only inner window rect.

