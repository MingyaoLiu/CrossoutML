
from PyQt5.QtCore import QThread
from ProcessFrameClass import DebugThread, DetectClickThread, InCombatVehicleDataCalculationThread
from DCaptureClass import getDCapture

class BotBackgroundThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.debugBot = None
        self.bot = None
        self.bot2 = None
        
    def __del__(self):
        self.wait()
        print("terminated")

    def stopBot(self):
        if self.bot:
            self.bot.isRunning = False
            self.bot = None
        if self.bot2:
            if self.bot2.battleVehicleCalcThread:
                self.bot2.battleVehicleCalcThread.isRunning = False
                self.bot2.battleVehicleCalcThread = None
            if self.bot2.battleControlThread:
                self.bot2.battleControlThread.isRunning = False
                self.bot2.battleControlThread = None
            if self.bot2.weaponFirethread:
                self.bot2.weaponFirethread.isRunning = False
                self.bot2.weaponFirethread = None
            self.bot2.isRunning = False
            self.bot2 = None
        
        if self.debugBot:
            self.debugBot.isRunning = False
            self.debugBot = None
        getDCapture().stopCapture()

    def startBot(self):
        if self.bot:
            pass
        else:
            getDCapture().startCapture()

            # self.debugBot = InCombatVehicleDataCalculationThread()
            # self.debugBot = DetectClickThread()
            # self.debugBot = DebugThread()

            if (self.debugBot is not None):
                self.debugBot.start()
            else:
                self.bot = DebugThread()
                self.bot.start()
                self.bot2 = DetectClickThread()
                self.bot2.start()


    def exit(self):
        self.stopBot()
        print("all threads exited")

    def run(self):
        self.startBot()
