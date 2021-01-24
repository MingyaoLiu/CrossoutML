
from PyQt5.QtCore import QThread
from ProcessFrameClass import DebugThread, DetectClickThread
from DCaptureClass import getDCapture

class BotBackgroundThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.bot = None
        self.bot2 = None
        self.bcap = None

    def __del__(self):
        self.wait()
        print("terminated")

    def stopBot(self):
        if self.bcap:
            self.bcap.stopCapture()
            self.bcap = None
        if self.bot:
            self.bot.isRunning = False
            self.bot = None
        if self.bot2:
            self.bot2.isRunning = False
            self.bot2 = None

    def startBot(self):
        if self.bot or self.bcap:
            pass
        else:
            # self.bot = BotProgram()
            # self.bot.start()
            
            self.bcap = getDCapture()
            self.bcap.startCapture()
            self.bot = DebugThread()
            self.bot.start()
            self.bot2 = DetectClickThread()
            self.bot2.start()

    def exit(self):
        self.stopBot()
        print("exited")

    def run(self):
        self.startBot()
