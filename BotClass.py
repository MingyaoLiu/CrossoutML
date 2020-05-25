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

class BotProgram():

    def __init__(self):

        self.killBotNow = False

        # self.prev_frame_dist = 10

        self.d = d3dshot.create(capture_output='numpy')

        self.currentStep = ScreenStep(getGlobalSetting().settings.startScreen)

        self.battleMgm = BattleManagement()

        self.inBattleDelayTimer = None

        self.LoginScreen = Screen(ScreenStep.Login, const.login_crops, 10)
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
            self.__processFrame()
            

            # test_frame = self.frame[const.in_battle_mini_map_arrow_height_start:const.in_battle_mini_map_arrow_height_end,
            #    const.in_battle_mini_map_arrow_width_start:const.in_battle_mini_map_arrow_width_end]

            # img = cv2.cvtColor(test_frame, cv2.COLOR_BGR2GRAY)
            

            # ret, thresh = cv2.threshold(img, 195, 255, cv2.THRESH_BINARY)


            # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_NONE )
            # print(len(contours))
            # if len(contours) >= 1:

            #     cnt = contours[0]

            #     cv2.drawContours(img, [cnt], 0, (0,255,0), 1)
            #     cv2.fillPoly(img, pts =[cnt], color=(255,255,255))

            #     rows,cols = img.shape[:2]
            #     # line = cv2.fitLine(cnt, cv2.DIST_C , 0, 0.01, 0.01)
            #     [vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01)
            #     print(math.atan2(vy,vx))

            #     lefty = int((-x*vy/vx) + y)
            #     righty = int(((cols-x)*vy/vx)+y)
            #     cv2.line(img,(cols-1,righty),(0,lefty),(0,255,0),1)


            # img2 = img.copy()
            # cv2.drawContours(img2, [cnt], 0, (0,255,0), 1)
            # cv2.fillPoly(img2, pts =[cnt], color=(255,255,255))


            # ret2, thresh2 = cv2.threshold(img2, 195, 255, cv2.THRESH_BINARY)

            # contours2, hierarchy2 = cv2.findContours(thresh2, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_NONE )

            # # cv2.circle(thresh, (int(const.in_battle_mini_map_arrow_width / 2),
            # #                                 int(const.in_battle_mini_map_arrow_height / 2)), 10, (255, 255, 255), 2)


            

            # dst = cv2.cornerHarris(contours2[0],3,3,0.04)


                        
            # for i in contours2:
            #     size = cv2.contourArea(i)
            #     rect = cv2.minAreaRect(i)
            #     if size <10000:
            #         gray = np.float32(img2)
            #         mask = np.zeros(gray.shape, dtype="uint8")
            #         cv2.fillPoly(mask, [i], (255,255,255))
            #         dst = cv2.cornerHarris(mask,3,3,0.04)
            #         ret, dst = cv2.threshold(dst,0.1*dst.max(),255,0)
            #         dst = np.uint8(dst)
            #         ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
            #         criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
            #         corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)

            #         # print(len(corners))

            #         if rect[2] == 0 and len(corners) == 5:
            #             x,y,w,h = cv2.boundingRect(i)
            #             if w == h or w == h +3: #Just for the sake of example
            #                 print('Square corners: ')
            #                 for i in range(1, len(corners)):
            #                     print(corners[i])
            #             else:
            #                 print('Rectangle corners: ')
            #                 for i in range(1, len(corners)):
            #                     print(corners[i])
            #         if len(corners) == 5 and rect[2] != 0:
            #             print('Rombus corners: ')
            #             for i in range(1, len(corners)):
            #                 print(corners[i])
            #         if len(corners) == 4:
            #             print('Triangle corners: ')
            #             for i in range(1, len(corners)):
            #                 print(corners[i])
            #         if len(corners) == 6:
            #             print('Pentagon corners: ')
            #             for i in range(1, len(corners)):
            #                 print(corners[i])
            #         for i in range(1, len(corners)):
            #             # print(corners[i,0])
            #             cv2.circle(img2, (int(corners[i,0]), int(corners[i,1])), 7, (0,255,0), 2)
            #         # cv2.imshow('image', img)


            
            # cv2.imshow("DebugWindow", img)


            ## Test Center Image
            # ff = cv2.cvtColor(np_frame, cv2.COLOR_BGR2GRAY)
            # test_frame = ff[174:920, 587:1330]

            # cv2.imshow("TestCrop", test_frame)
            # text = pytesseract.image_to_string(test_frame, lang='eng')
            # print(text)
