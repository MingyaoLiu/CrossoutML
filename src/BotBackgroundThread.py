
from PyQt5.QtCore import QThread
from threads.StepResolveThread import DetectClickThread

from threads.DebugThread import DebugThread
from DCaptureClass import getDCapture
import Constants as const

class BotBackgroundThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.debugBot = None
        self.bot = None
        self.bot2 = None
        self.name = "BackgroundThread"
        
    def __del__(self):
        self.wait()
        print("terminated")

    def stopBot(self):
        if self.bot:
            self.bot.isRunning = False
            self.bot.join()
            self.bot = None
        if self.bot2:
            self.bot2.isRunning = False
            self.bot2.join()
            # if self.bot2.battleVehicleCalcThread:
            #     self.bot2.battleVehicleCalcThread.isRunning = False
            #     self.bot2.join()
            #     self.bot2.battleVehicleCalcThread = None
            # if self.bot2.speedControlThread:
            #     self.bot2.speedControlThread.isRunning = False
            #     self.bot2.speedControlThread.join()
            #     self.bot2.speedControlThread = None
            # if self.bot2.turnControlThread:
            #     self.bot2.turnControlThread.isRunning = False
            #     self.bot2.turnControlThread.join()
            #     self.bot2.turnControlThread = None
            # if self.bot2.weaponFirethread:
            #     self.bot2.weaponFirethread.isRunning = False
            #     self.bot2.weaponFirethread.join()
            #     self.bot2.weaponFirethread = None
            self.bot2 = None
        
        if self.debugBot:
            self.debugBot.isRunning = False
            self.debugBot = None
        getDCapture().stopCapture()

    def startBot(self):
        if (self.bot or self.bot2):
            pass
        else:
            getDCapture().startCapture()

            # self.debugBot = InCombatVehicleDataCalculationThread()
            # self.debugBot = DetectClickThread()
            # self.debugBot = DebugThread()

            if (self.debugBot is not None): # used for launching only one thread
                self.debugBot.start()
            else:
                if (const.isDevEnvironment()):
                    self.bot = DebugThread()
                    self.bot.start()
                self.bot2 = DetectClickThread()
                self.bot2.start()


    def exit(self):
        self.stopBot()
        print("all threads exited")

    def run(self):
        self.startBot()
