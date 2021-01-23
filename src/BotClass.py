import cv2
import Constants as const
from Constants import ScreenStep, Point
from screens.ScreenClass import Screen
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
from screens.LoginScreenClass import LoginScreen
from screens.MainMenuScreenClass import MainMenuScreen
from DCaptureClass import getDCapture
from multiprocess import Value
from ProcessFrameClass import ProcessFrame, ProcessThread
import Constants as const

class BotProgram():

    def __init__(self):

        self.isProcessingFrameIndication = Value('i', 1)
        self.pf = None

        self.killBotNow = False

        # self.prev_frame_dist = 10
        self.lastProcessTime = None


        self.battleMgm = BattleManagement()

        self.inBattleDelayTimer = None

        self.LoginScreen = LoginScreen(None)
        self.WelcomeScreen = Screen(ScreenStep.WelcomeScreen,
                                    const.welcome_crops, 20, None)

        self.MasterJackUpgradeScreen = Screen(
            ScreenStep.MasterJackUpgradeScreen, const.mainmenu_master_jack_crops, 10, None)

        self.ChallengeCompleteScreen = Screen(
            ScreenStep.ChallengeCompleteScreen, const.mainmenu_challenge_crops, 10, None)

        self.MainMenuScreen = MainMenuScreen(
            ScreenStep.MainMenu, const.mainmenu_crops, 30, None)

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
        self.SelectModeScreen = Screen(ScreenStep.SelectMode, [], 30, None)

        self.ResourcePrepareBattleScreen = Screen(
            ScreenStep.GetResourceMenu, const.resource_prepare_crops, 30, None)

        self.BattlePreparationScreen = Screen(
            ScreenStep.BattlePrepareScreen, const.battle_preparation_crops, 1500, None)

        self.InBattleScreen = Screen(ScreenStep.InBattleNow, [], 30, None)

        self.FinishBattleScreen = Screen(
            ScreenStep.FinishBattleScreen, const.finish_battle_crops, 3000, None)


        self.currentStep = Value('i',  ScreenStep(getGlobalSetting().settings.startScreen))

        self.currentScreen = self.LoginScreen
        self.StepFlow = [
            self.LoginScreen,
            self.WelcomeScreen,
            self.MainMenuScreen
        ]

    def __advanceNextStep(self):
        if self.currentStep == ScreenStep.FinishBattleScreen:
            self.currentStep = ScreenStep.MasterJackUpgradeScreen
        else:
            self.currentStep += 1

    def getLastStepScreen(self):
        currentIndex = self.StepFlow.index(self.currentScreen)
        if (currentIndex == len(self.StepFlow) - 1):
            return self.StepFlow[len(self.StepFlow) - 1]
        return self.StepFlow[currentIndex - 1]

    def getNextStepScreen(self):
        currentIndex = self.StepFlow.index(self.currentScreen)
        if (currentIndex == len(self.StepFlow) - 1):
            return self.StepFlow[0]
        return self.StepFlow[currentIndex + 1]


    def __processFrame(self, newFrame):
        currentTimeSecond = time.time()
        if (self.lastProcessTime):
            if ((currentTimeSecond - self.lastProcessTime) < 5):
                return 0
        self.lastProcessTime = currentTimeSecond
        print(self.lastProcessTime)

    def OLD__processFrame(self):
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
            elif screen.checkSingleSatisfy(self.frame, 2)[0]:  # login button
                screen.setRandomNewAccount()
                screen.fillUsername()
                screen.fillPassword()
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

            if screen.retryCount == 0:
                screen.initMassEsc(6)
                print("esc")

            elif self.LoginScreen.checkIfSwitchAccount():
                if screen.checkSingleSatisfy(self.frame, 3)[0]:
                    screen.executeSingleClick(3)
                    self.currentStep = ScreenStep.Login
                    screen.resetRetryCount()
                elif screen.checkSingleSatisfy(self.frame, 2)[0]:
                    screen.executeSingleClick(2)
                else:
                    kbDown("esc")
                    kbUp("esc")
                    time.sleep(1)
            elif screen.checkSingleSatisfy(self.frame, 1)[0]:
                screen.resetRetryCount()
                screen.executeSingleClick(1)
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

            prev_frame = getDCapture().getFrame(20)

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
        self.battleMgm.stop()
        cv2.destroyAllWindows()
        if (self.pf):
            self.pf.terminate()


    def monitorImageClick(self, event, x, y, p1, p2):
        if event == cv2.EVENT_LBUTTONDOWN:
            print('mouse down on:')
            print((x, y))

    def start(self):

        print("START BOT")
        # mouseClick(getCorrectPos(Point(0, 0)))


        while self.killBotNow is False:
            np_frame = getDCapture().getFrame(0)
            # self.frame = cv2.cvtColor(np_frame, cv2.COLOR_BGR2RGB)
            # self.prev_frame = getDCapture().getFrame(20)
            # # self.__processFrame()
            # # detectedMap = self.frame[174:920, 587:1330]
            # detectedMap = self.frame[171:923, 583:1335]
            # cv2.imshow("FRAME", self.frame)
            # cv2.imshow("MAP", detectedMap)

            # self.__processFrame(np_frame)

            
            if (self.isProcessingFrameIndication.value == 1):
                detectClickPair = const.DetectClickPair(
                    "Login Button",
                    const.CropArea(const.login_label_width_start, const.login_label_height_start,
                            const.login_label_width_end, const.login_label_height_end),
                    True,
                    const.Point(const.login_label_trigger_pos_x,
                        const.login_label_trigger_pos_y),
                    True,
                    ["login", "log in", "log ln", "logln"],
                    10,
                    1
                )
                # if (self.pf):
                #     self.pf.terminate()
                # self.isProcessingFrameIndication.value = 0
                # self.pf = ProcessFrame(procIsDoneIndicator = self.isProcessingFrameIndication, dcap= getDCapture().d)
                # self.pf.start()

                # self.pf = ProcessThread(1, "Thread-1", 1)
                # self.pf.start()
            
            
            cv2.imshow("Capture", np_frame)
            cv2.setMouseCallback('Capture', self.monitorImageClick)
            cv2.waitKey(1)









            # titlescreen = self.frame[658:697, 883:1029]
            # cv2.imshow("title", titlescreen)
            # print(self.MainMenuScreen.checkSingleSatisfy(self.frame, 2))

            # print(self.MainMenuScreen.checkSingleSatisfy(self.frame, 3))

            # test_frame = self.frame[const.in_battle_mini_map_arrow_height_start:const.in_battle_mini_map_arrow_height_end,
            #    const.in_battle_mini_map_arrow_width_start:const.in_battle_mini_map_arrow_width_end]

            # getDebugger().debugDisplay(test_frame)

            # img = cv2.cvtColor(test_frame, cv2.COLOR_BGR2GRAY)

            # Test Center Image
            # ff = cv2.cvtColor(np_frame, cv2.COLOR_BGR2GRAY)
            # test_frame = ff[174:920, 587:1330]

            # cv2.imshow("TestCrop", test_frame)
            # text = pytesseract.image_to_string(test_frame, lang='eng')
            # print(text)
