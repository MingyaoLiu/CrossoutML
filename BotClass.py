import cv2
import d3dshot
import Constants as const
from Constants import ScreenStep, Point
from ScreenClass import Screen
from Utils import getCorrectPos
from InputControl import kbDown, kbUp, KBPress, mouseClick
from MovementClass import MoveManagement
from BattleClass import BattleManagement
import time
from SettingsClass import getGlobalSetting
import random
import threading
import numpy as np
import math
from DebugClass import getDebugger
from LoginScreenClass import LoginScreen

class BotProgram():

    def __init__(self):

        self.killBotNow = False

        # self.prev_frame_dist = 10

        self.d = d3dshot.create(capture_output='numpy')

        self.currentStep = ScreenStep(getGlobalSetting().settings.startScreen)

        self.battleMgm = BattleManagement()

        self.inBattleDelayTimer = None

        self.LoginScreen = LoginScreen(ScreenStep.Login, const.login_crops, 10)
        self.WelcomeScreen = Screen(ScreenStep.WelcomeScreen,
                                    const.welcome_crops, 20)

        self.MasterJackUpgradeScreen = Screen(
            ScreenStep.MasterJackUpgradeScreen, const.mainmenu_master_jack_crops, 10)

        self.ChallengeCompleteScreen = Screen(
            ScreenStep.ChallengeCompleteScreen, const.mainmenu_challenge_crops, 10)

        self.MainMenuScreen = Screen(
            ScreenStep.MainMenu, const.mainmenu_crops, 30)

        self.select_mode_click_pos = [
            getCorrectPos(Point(const.scrap_btn_trigger_pos_x,
                                const.scrap_btn_trigger_pos_y)),
            getCorrectPos(Point(const.wire_btn_trigger_pos_x,
                                const.wire_btn_trigger_pos_y)),
            getCorrectPos(Point(const.battery_btn_trigger_pos_x,
                                const.battery_btn_trigger_pos_y)),
            getCorrectPos(Point(const.raven_path_btn_trigger_pos_x,
                                const.raven_path_btn_trigger_pos_y))
        ]
        self.SelectModeScreen = Screen(ScreenStep.SelectMode, [], 30)

        self.ResourcePrepareBattleScreen = Screen(
            ScreenStep.GetResourceMenu, const.resource_prepare_crops, 30)

        self.BattlePreparationScreen = Screen(
            ScreenStep.BattlePrepareScreen, const.battle_preparation_crops, 1500)

        self.InBattleScreen = Screen(ScreenStep.InBattleNow, [], 30)

        self.FinishBattleScreen = Screen(
            ScreenStep.FinishBattleScreen, const.finish_battle_crops, 3000)

    def __advanceNextStep(self):
        if self.currentStep == ScreenStep.debug:
            pass
        elif self.currentStep == ScreenStep.FinishBattleScreen:
            self.currentStep = ScreenStep.Login
        else:
            self.currentStep += 1

    def __processFrame(self):
        if self.currentStep == ScreenStep.Login:
            screen = self.LoginScreen
            if screen.retryCount == 0:
                screen.addFailCount()
                kbDown("esc")
                kbUp("esc")
                time.sleep(0.5)
                kbDown("esc")
                kbUp("esc")
                time.sleep(0.5)
            elif screen.checkSingleSatisfy(self.frame, 0)[0]:
                screen.executeSingleClick(0)
            elif screen.checkSingleSatisfy(self.frame, 1)[0]:
                screen.executeSingleClick(1)
            elif screen.checkSingleSatisfy(self.frame, 2)[0]:
                screen.resetRetryCount()
                screen.executeSingleClick(2)
                self.__advanceNextStep()
            elif screen.addFailCount():
                pass
            else:
                screen.resetRetryCount()
                self.__advanceNextStep()

        elif self.currentStep == ScreenStep.WelcomeScreen:
            screen = self.WelcomeScreen
            if screen.checkSatisfy(self.frame):
                screen.resetRetryCount()
                screen.executeClick()
                self.__advanceNextStep()
            elif screen.addFailCount():
                pass
            else:
                screen.resetRetryCount()
                self.__advanceNextStep()
        elif self.currentStep == ScreenStep.MasterJackUpgradeScreen:
            screen = self.MasterJackUpgradeScreen
            if screen.checkSatisfy(self.frame):
                screen.resetRetryCount()
                screen.executeClick()
            elif screen.addFailCount():
                pass
            else:
                screen.resetRetryCount()
                self.__advanceNextStep()
        elif self.currentStep == ScreenStep.ChallengeCompleteScreen:
            screen = self.ChallengeCompleteScreen
            if screen.checkSatisfy(self.frame):
                screen.resetRetryCount()
                screen.executeClick()
            elif screen.addFailCount():
                pass
            else:
                screen.resetRetryCount()
                self.__advanceNextStep()

        elif self.currentStep == ScreenStep.MainMenu:
            screen = self.MainMenuScreen
            if screen.checkSatisfy(self.frame):
                screen.resetRetryCount()
                screen.executeClick()
                self.__advanceNextStep()
            elif screen.addFailCount():
                pass
            else:
                screen.resetRetryCount()
                self.__advanceNextStep()

        elif self.currentStep == ScreenStep.SelectMode:
            clickPos = random.choice(self.select_mode_click_pos)
            # clickPos = select_mode_click_pos[3]
            mouseClick(clickPos)
            time.sleep(1)
            self.__advanceNextStep()

        elif self.currentStep == ScreenStep.GetResourceMenu:
            screen = self.ResourcePrepareBattleScreen
            if screen.checkSatisfy(self.frame):
                screen.resetRetryCount()
                screen.executeClick()
                self.__advanceNextStep()
            elif screen.addFailCount():
                pass
            else:
                screen.resetRetryCount()
                self.__advanceNextStep()

        elif self.currentStep == ScreenStep.BattlePrepareScreen:
            screen = self.BattlePreparationScreen

            prev_frame = self.d.get_frame(20)

            if screen.retryCount % 100 == 0 and screen.retryCount != 0:
                kbDown("tab")

            satisfaction_check = screen.checkSingleSatisfy(prev_frame, 1)

            if satisfaction_check[0]:
                print("aaa")
                detectedMap = self.frame[174:920, 587:1330]
                mapMask = cv2.imread(
                    const.map_mask_file_path[satisfaction_check[1]], 0)
                self.battleMgm.loadMapMask(detectedMap, mapMask)
                kbUp("tab")
                screen.resetRetryCount()
                self.__advanceNextStep()
            elif screen.addFailCount():
                pass
            else:
                screen.resetRetryCount()
                self.__advanceNextStep()

        elif self.currentStep == ScreenStep.InBattleNow:
            self.__advanceNextStep()
            self.battleMgm.delayStart()

        elif self.currentStep == ScreenStep.DeathWaiting:

            self.battleMgm.loadFrame(
                self.frame)
            if self.inBattleDelayTimer is None:
                self.inBattleDelayTimer = threading.Timer(
                    180, self.__finishInBattle)
                self.inBattleDelayTimer.start()
            else:
                pass

        elif self.currentStep == ScreenStep.FinishBattleScreen:
            screen = self.FinishBattleScreen
            if screen.checkSatisfy(self.frame):
                self.battleMgm.stop()
                screen.resetRetryCount()
                screen.executeClick()
                self.__advanceNextStep()
            elif screen.addFailCount():
                self.battleMgm.loadFrame(
                    self.frame)
            else:
                self.battleMgm.stop()
                screen.resetRetryCount()
                self.__advanceNextStep()

        else:
            # print("CURRENT STEP:", currentStep)
            pass

    def __finishInBattle(self):
        self.inBattleDelayTimer = None
        self.__advanceNextStep()

    def stop(self):
        print("STOP BOT")
        self.killBotNow = True
        self.d.stop()
        self.battleMgm.stop()

    def start(self):
        print("START BOT")
        mouseClick(getCorrectPos(Point(400, 10)))
        target_fps = getGlobalSetting().settings.targetDisplayFPS or 20
        self.d.display = self.d.displays[getGlobalSetting(
        ).settings.displayIndex]
        displayShiftX = getGlobalSetting().settings.displayShiftX
        displayShiftY = getGlobalSetting().settings.displayShiftY
        self.d.capture(target_fps=target_fps, region=(
            0 + displayShiftX, 0 + displayShiftY, const.screenWidth, const.screenHeight))

        time.sleep(1)

        while self.killBotNow is False:
            np_frame = self.d.get_latest_frame()
            self.frame = cv2.cvtColor(np_frame, cv2.COLOR_BGR2RGB)
            self.prev_frame = self.d.get_frame(20)
            self.__processFrame()
            

            # test_frame = self.frame[const.in_battle_mini_map_arrow_height_start:const.in_battle_mini_map_arrow_height_end,
            #    const.in_battle_mini_map_arrow_width_start:const.in_battle_mini_map_arrow_width_end]
            
            # getDebugger().debugDisplay(test_frame)

            # img = cv2.cvtColor(test_frame, cv2.COLOR_BGR2GRAY)

            ## Test Center Image
            # ff = cv2.cvtColor(np_frame, cv2.COLOR_BGR2GRAY)
            # test_frame = ff[174:920, 587:1330]

            # cv2.imshow("TestCrop", test_frame)
            # text = pytesseract.image_to_string(test_frame, lang='eng')
            # print(text)
