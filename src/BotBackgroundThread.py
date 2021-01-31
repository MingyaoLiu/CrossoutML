
from PyQt5.QtCore import QThread
from threads.StepResolveThread import DetectClickThread

from threads.DebugThread import DebugThread
from DCaptureClass import getDCapture
import Constants as const
from SettingsClass import getGlobalSetting
from Utils import findStepById

class BotBackgroundThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.name = "CrossMLUIBackgroundThread"
        self.debugThread = None # debug thread for DetectClick
        self.detectThread = None
        
    def __del__(self):
        self.wait()
        print("terminated")

    def stopBot(self):
        if self.debugThread:
            self.debugThread.isRunning = False
            self.debugThread.join()
            self.debugThread = None
        if self.detectThread:
            self.detectThread.isRunning = False
            self.detectThread.join()
            self.detectThread = None
        getDCapture().stopCapture()

    def startBot(self):

        # temporary update chat detection list
        step = findStepById('in_game_detect_chat_callout')
        step.strings = getGlobalSetting().settings.chatDetectKeywords.split(',')

        if (self.debugThread or self.detectThread):
            self.stopBot() # reset if there is unclean bot thread.
        else:
            getDCapture().startCapture()
            
            if getGlobalSetting().settings.showDetectClickDebugWindow:
                self.debugThread = DebugThread()
                self.debugThread.start()

            self.detectThread = DetectClickThread()
            self.detectThread.start()

    def exit(self):
        self.stopBot()
        print("all threads exited")

    def run(self):
        self.startBot()
