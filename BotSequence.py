import cv2
from BotClass import BotProgram


bot = None


def stopBot():
    global bot
    if isinstance(bot, BotProgram):
        bot.stop()
        cv2.destroyAllWindows()


def startBot():
    global bot
    if isinstance(bot, BotProgram):
        pass
    else:
        bot = BotProgram()
        bot.start()
