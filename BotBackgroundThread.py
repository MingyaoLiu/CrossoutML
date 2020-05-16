
from PyQt5.QtCore import QThread
from BotClass import BotProgram


class BotBackgroundThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.bot = None

    def __del__(self):
        self.wait()
        print("terminated")

    def stopBot(self):
        if self.bot:
            self.bot.stop()
            self.bot = None
        else:
            pass

    def startBot(self):
        if self.bot:
            pass
        else:
            self.bot = BotProgram()
            self.bot.start()

    def exit(self):
        self.stopBot()
        print("exited")

    def run(self):
        self.startBot()
