import win32con
import win32api
import time
import threading
import random

import d3dshot

import cv2

import pytesseract

from InputControl import mouseClick, kbDown, kbUp, KBPress

from MovementClass import Move

import numpy as np

import Constants as const
from Constants import ScreenStep, CropProperty, CropArea, Point

import math

from Utils import getCorrectPos


from ScreenClass import Screen

from SettingsClass import getGlobalSetting

import InBattleChecks

from BotClass import BotProgram
import inspect

lastFullyCompleteStep = 0
isAlreadySelfDestruct = False
isBattleAlreadyActive = False
isAlreadyBackStirring = False
battleStartDelay = True
battleStartDelayTimer = None


isFirstTimeAtLogin = True
detectedMap = None
isAlreadyExecutingTurn = False
isInAllowedZone = False
turnCommandStack = []
mapMask = None


bot = None


def stopBot():
    global bot
    if isinstance(bot, BotProgram):
        bot.stop()
        bot = None


def startBot():
    global bot
    if isinstance(bot, BotProgram):
        pass
    else:
        bot = BotProgram()


def runDetection():

    global isAlreadySelfDestruct
    global isAlreadyBackStirring
    global battleStartDelay
    global isFirstTimeAtLogin
    global detectedMap
    global isAlreadyExecutingTurn
    global isInAllowedZone
    global turnCommandStack
    global mapMask

    mouseClick(getCorrectPos(Point(400, 10)))
    ######################
    ## SET CURRENT STEP ##
    ######################
    currentStep = const.ScreenStep.BattlePrepareScreen

    d = d3dshot.create(capture_output='numpy')
    if (len(d.displays) > 1):
        d.display = d.displays[1]
        getGlobalSetting().settings.shiftX = -2560
        getGlobalSetting().saveSettings()
    else:
        d.display = d.displays[0]
        getGlobalSetting().settings.shiftX = 0
        getGlobalSetting().saveSettings()
    d.capture(target_fps=20, region=(
        0, 0, const.screenWidth, const.screenHeight))

    time.sleep(1)

    while True:
        np_frame = d.get_latest_frame()
        frame = cv2.cvtColor(np_frame, cv2.COLOR_BGR2RGB)

        # test_frame = frame[const.battle_map_name_label_height_start:const.battle_map_name_label_height_end,
        #                    const.battle_map_name_label_width_start:const.battle_map_name_label_width_end]
        # # test_frame = frame[174:920, 587:1330]
        # cv2.imshow("TestCrop", test_frame)
        # text = pytesseract.image_to_string(test_frame, lang='eng')
        # print(text)

        if currentStep == const.ScreenStep.Login:
            screen = LoginScreen

            if screen.retryCount == 0:
                screen.addFailCount()
                win32api.keybd_event(0x1B, 0, 0, 0)
                win32api.keybd_event(0x1B, 0, win32con.KEYEVENTF_KEYUP, 0)
                time.sleep(1)
                win32api.keybd_event(0x1B, 0, 0, 0)
                win32api.keybd_event(0x1B, 0, win32con.KEYEVENTF_KEYUP, 0)
                time.sleep(1)
            elif screen.checkSingleSatisfy(frame, 0)[0]:
                screen.executeSingleClick(0)
            elif screen.checkSingleSatisfy(frame, 1)[0]:
                screen.executeSingleClick(1)
            elif screen.checkSingleSatisfy(frame, 2)[0]:
                screen.resetRetryCount()
                screen.executeSingleClick(2)
                currentStep += 1
            elif screen.addFailCount():
                pass
            else:
                screen.resetRetryCount()
                currentStep += 1

        elif currentStep == const.ScreenStep.WelcomeScreen:
            screen = WelcomeScreen
            if screen.checkSatisfy(frame):
                screen.resetRetryCount()
                screen.executeClick()
                currentStep += 1
            elif screen.addFailCount():
                pass
            else:
                screen.resetRetryCount()
                currentStep += 1
        elif currentStep == const.ScreenStep.MasterJackUpgradeScreen:
            screen = MasterJackUpgradeScreen
            if screen.checkSatisfy(frame):
                screen.resetRetryCount()
                screen.executeClick()
            elif screen.addFailCount():
                pass
            else:
                screen.resetRetryCount()
                currentStep += 1
        elif currentStep == const.ScreenStep.ChallengeCompleteScreen:
            screen = ChallengeCompleteScreen
            if screen.checkSatisfy(frame):
                screen.resetRetryCount()
                screen.executeClick()
            elif screen.addFailCount():
                pass
            else:
                screen.resetRetryCount()
                currentStep += 1

        elif currentStep == const.ScreenStep.MainMenu:
            screen = MainMenuScreen
            if screen.checkSatisfy(frame):
                screen.resetRetryCount()
                screen.executeClick()
                currentStep += 1
            elif screen.addFailCount():
                pass
            else:
                screen.resetRetryCount()
                currentStep += 1

        elif currentStep == const.ScreenStep.SelectMode:
            clickPos = random.choice(select_mode_click_pos)
            # clickPos = select_mode_click_pos[3]
            mouseClick(clickPos)
            time.sleep(1)
            currentStep += 1

        elif currentStep == const.ScreenStep.GetResourceMenu:
            screen = ResourcePrepareBattleScreen
            if screen.checkSatisfy(frame):
                screen.resetRetryCount()
                screen.executeClick()
                currentStep += 1
            elif screen.addFailCount():
                pass
            else:
                screen.resetRetryCount()
                currentStep += 1

        elif currentStep == const.ScreenStep.BattlePrepareScreen:
            screen = BattlePreparationScreen

            prev_frame = d.get_frame(5)

            if screen.retryCount % 100 == 0 and screen.retryCount != 0:
                kbDown("tab")
            satisfaction_check = screen.checkSingleSatisfy(prev_frame, 1)
            if satisfaction_check[0]:

                detectedMap = frame[174:920, 587:1330]
                mapMask = cv2.imread(
                    const.map_mask_file_path[satisfaction_check[1]], 0)
                kbUp("tab")
                screen.resetRetryCount()
                currentStep += 1
            elif screen.addFailCount():
                pass
            else:
                screen.resetRetryCount()
                currentStep += 1

        elif currentStep == const.ScreenStep.InBattleNow:
            currentStep += 1
            DoBattleNow()

        elif currentStep == const.ScreenStep.DeathWaiting:
            currentStep += 1

        elif currentStep == const.ScreenStep.FinishBattleScreen:
            screen = FinishBattleScreen
            if screen.checkSatisfy(frame):
                cv2.destroyWindow('TrackingSourceMap')
                battleEnded()
                screen.resetRetryCount()
                screen.executeClick()
                currentStep = const.ScreenStep.Login
            elif screen.addFailCount():

                if battleStartDelay:
                    pass
                else:
                    prev_frame = d.get_frame(10)
                    battlecheck = InBattleChecks.BattleFrame(
                        frame, prev_frame, detectedMap, mapMask)

                    if battlecheck.isEnemyNear():
                        KBPress("1").start()
                    tentacle_pos_lst = battlecheck.calculateTentacle()
                    moveMgm =

            else:
                screen.resetRetryCount()
                battleEnded()
                currentStep = const.ScreenStep.Login

        else:
            # print("CURRENT STEP:", currentStep)
            pass

        if cv2.waitKey(1) & 0xFF == ord('q'):
            d.stop()
            cv2.destroyAllWindows()
            break


class setInterval:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()


destructTimer = None


def destructComplete():
    global destructTimer
    global isAlreadySelfDestruct
    kbUp("m")
    destructTimer.cancel()


def selfDesctruct():
    global destructTimer
    global isAlreadySelfDestruct
    if isAlreadySelfDestruct == False:
        isAlreadySelfDestruct = True
        kbDown("m")
        destructTimer = threading.Timer(5.0, destructComplete)
        destructTimer.start()


def battleEnded():

    global stirInterval
    global isAlreadySelfDestruct
    global isBattleAlreadyActive
    global isAlreadyBackStirring
    global battleStartDelay
    global calloutInterval
    global carJackInterval
    global total_back_stir_count
    global detectedMap

    detectedMap = None
    try:
        if calloutInterval:
            calloutInterval.cancel()
    except ValueError:
        pass
    try:
        if carJackInterval:
            carJackInterval.cancel()
    except ValueError:
        pass
    try:
        if stirInterval:
            stirInterval.cancel()
    except ValueError:
        pass

    total_back_stir_count = 0
    battleStartDelay = True
    isBattleAlreadyActive = False
    isAlreadySelfDestruct = False
    isAlreadyBackStirring = False
    kbUp("w")
    kbUp("a")
    kbUp("s")
    kbUp("d")
    kbUp("m")


def calllOut():
    calloutLst = ["b", "c", "x", "z"]
    callout = random.choice(list(calloutLst))
    KBPress(callout).start()


def carJack():
    KBPress("r").start()


total_back_stir_count = 0
left_short_back_stir_in_a_roll = 0
right_long_back_stir_in_a_roll = 0


# Left 3, RIght 3, back

def setBackByOneLeftShortBackStirCount():
    global left_short_back_stir_in_a_roll
    if left_short_back_stir_in_a_roll > 0:
        left_short_back_stir_in_a_roll -= 1
    print("Set back left, currently", left_short_back_stir_in_a_roll)


def setBackByOneRightLongBackStirCount():
    global right_long_back_stir_in_a_roll
    if right_long_back_stir_in_a_roll > 0:
        right_long_back_stir_in_a_roll -= 1
    print("Set back right, currently", right_long_back_stir_in_a_roll)


def stopMoving():
    kbUp("w")
    kbUp("a")
    kbUp("s")
    kbUp("d")


def determineBackStir():
    global isAlreadyBackStirring
    global left_short_back_stir_in_a_roll
    global right_long_back_stir_in_a_roll
    global total_back_stir_count

    if isAlreadyBackStirring == False and total_back_stir_count < 6:
        total_back_stir_count += 1
    elif isAlreadyBackStirring == False and total_back_stir_count >= 6:
        # fullStuckTimer = threading.Timer(20, selfDesctruct)
        # fullStuckTimer.start()
        return stopMoving()

    if isAlreadyBackStirring:
        pass
    elif right_long_back_stir_in_a_roll >= 2:
        full_reverse_back_stir()
        left_short_back_stir_in_a_roll = 0
        right_long_back_stir_in_a_roll = 0
    elif left_short_back_stir_in_a_roll >= 2:
        rightLongBackStir()
        right_long_back_stir_in_a_roll += 1

    elif right_long_back_stir_in_a_roll > 0:
        rightLongBackStir()
        right_long_back_stir_in_a_roll += 1

    elif left_short_back_stir_in_a_roll > 0:
        leftShortBackStir()
        left_short_back_stir_in_a_roll += 1

    else:
        leftShortBackStir()
        left_short_back_stir_in_a_roll += 1


leftShortBackStirTimer1 = None
leftShortBackStirTimer2 = None
leftShortBackStirTimer3 = None


class backStir():

    def __init__(self, direction, duration,):
        self.direction = direction


def leftShortBackStir():
    global left_short_back_stir_in_a_roll
    global isAlreadyBackStirring

    isAlreadyBackStirring = True

    kbUp("w")

    global leftShortBackStirTimer1
    global leftShortBackStirTimer2
    global leftShortBackStirTimer3

    rollBackOneTimer = threading.Timer(25, setBackByOneLeftShortBackStirCount)
    rollBackOneTimer.start()

    def finish():
        global isAlreadyBackStirring
        global leftShortBackStirTimer3
        leftShortBackStirTimer3.cancel()
        isAlreadyBackStirring = False

    def turnFinalRight():
        global leftShortBackStirTimer2
        global leftShortBackStirTimer3
        leftShortBackStirTimer2.cancel()
        kbDown("w")
        KBPress("d", 0.73).start()

        leftShortBackStirTimer3 = threading.Timer(1, finish)
        leftShortBackStirTimer3.start()

    def turnForwardLeft():
        global leftShortBackStirTimer1
        global leftShortBackStirTimer2
        leftShortBackStirTimer1.cancel()
        KBPress("w", 2.65).start()
        KBPress("a", 1.65).start()

        leftShortBackStirTimer2 = threading.Timer(2.75, turnFinalRight)
        leftShortBackStirTimer2.start()

    KBPress("s", 1.6).start()

    leftShortBackStirTimer1 = threading.Timer(1.7, turnForwardLeft)
    leftShortBackStirTimer1.start()


rightLongBackStirTimer1 = None
rightLongBackStirTimer2 = None
rightLongBackStirTimer3 = None


def rightLongBackStir():
    global isAlreadyBackStirring

    isAlreadyBackStirring = True
    kbUp("w")

    global rightLongBackStirTimer1
    global rightLongBackStirTimer2
    global rightLongBackStirTimer3

    rollBackOneTimer = threading.Timer(30, setBackByOneRightLongBackStirCount)
    rollBackOneTimer.start()

    def finish():
        global isAlreadyBackStirring
        global rightLongBackStirTimer3

        rightLongBackStirTimer3.cancel()
        isAlreadyBackStirring = False

    def turnFinalLeft():
        global rightLongBackStirTimer2
        global rightLongBackStirTimer3

        rightLongBackStirTimer2.cancel()
        kbDown("w")
        KBPress("a", 0.72).start()

        rightLongBackStirTimer3 = threading.Timer(1, finish)
        rightLongBackStirTimer3.start()

    def turnForwardRight():
        global rightLongBackStirTimer1
        global rightLongBackStirTimer2

        rightLongBackStirTimer1.cancel()
        KBPress("w", 3.5).start()
        KBPress("d", 1.75).start()

        rightLongBackStirTimer2 = threading.Timer(3.6, turnFinalLeft)
        rightLongBackStirTimer2.start()

    KBPress("s", 2.4).start()

    rightLongBackStirTimer1 = threading.Timer(2.5, turnForwardRight)
    rightLongBackStirTimer1.start()


fullreverseBackStirTimer1 = None
fullreverseBackStirTimer2 = None


def full_reverse_back_stir():
    global isAlreadyBackStirring

    isAlreadyBackStirring = True
    kbUp("w")

    global fullreverseBackStirTimer1
    global fullreverseBackStirTimer2

    def finish():
        global isAlreadyBackStirring
        global fullreverseBackStirTimer2
        fullreverseBackStirTimer2.cancel()
        isAlreadyBackStirring = False

    def turnAround():
        global fullreverseBackStirTimer1
        global fullreverseBackStirTimer2
        fullreverseBackStirTimer1.cancel()
        kbDown("w")
        KBPress("a", 2.4).start()

        fullreverseBackStirTimer2 = threading.Timer(3, finish)
        fullreverseBackStirTimer2.start()

    KBPress("s", 2.1).start()

    fullreverseBackStirTimer1 = threading.Timer(2.4, turnAround)
    fullreverseBackStirTimer1.start()


stirInterval = None
calloutInterval = None
carJackInterval = None

backStirTimer1 = None
backStirTimer2 = None
backStirTimer3 = None
backStirTimer4 = None

needLongBackStir = False
shortBackStirCount = 0
backStirDirection = "a"


lastStir = "a"


def stirringHorizontal():
    # print("<< In Battle >> Stirring")
    global lastStir
    global isAlreadyBackStirring
    if isAlreadyBackStirring:
        pass
    else:

        if lastStir == "a":
            KBPress("d", 0.3).start()
            lastStir = "d"
        else:
            KBPress("a", 0.3).start()
            lastStir = "a"


def delayBattleStart():
    global stirInterval
    global battleStartDelay
    global battleStartDelayTimer
    global calloutInterval
    global carJackInterval
    battleStartDelay = False
    try:
        if battleStartDelayTimer:
            battleStartDelayTimer.cancel()
    except ValueError:
        pass

    # stirInterval = setInterval(6, stirringHorizontal)
    # calloutInterval = setInterval(40, calllOut)
    # carJackInterval = setInterval(10, carJack)


def DoBattleNow():
    global isAlreadySelfDestruct
    global isBattleAlreadyActive
    global battleStartDelayTimer
    if isBattleAlreadyActive:
        # print("Battle Happening")
        pass
    else:
        isBattleAlreadyActive = True
        battleStartDelayTimer = threading.Timer(1, delayBattleStart)
        battleStartDelayTimer.start()
        kbDown("s")
