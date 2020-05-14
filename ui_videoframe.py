import win32con
import win32api
import time
import threading
import random

import d3dshot

import cv2

import pytesseract

import InputControl


import numpy as np

import Constants as const
from Constants import ScreenStep, CropProperty, CropArea, Point

import math

from Utils import getCorrectPos


from ScreenClass import Screen

from SettingsClass import getGlobalSetting

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


LoginScreen = Screen(ScreenStep.Login, const.login_crops, 10)

WelcomeScreen = Screen(ScreenStep.WelcomeScreen, const.welcome_crops, 20)

MasterJackUpgradeScreen = Screen(
    ScreenStep.MasterJackUpgradeScreen, const.mainmenu_master_jack_crops, 10)

ChallengeCompleteScreen = Screen(
    ScreenStep.ChallengeCompleteScreen, const.mainmenu_challenge_crops, 10)

MainMenuScreen = Screen(ScreenStep.MainMenu, const.mainmenu_crops, 30)

select_mode_click_pos = [
    getCorrectPos(Point(const.scrap_btn_trigger_pos_x,
                        const.scrap_btn_trigger_pos_y)),
    getCorrectPos(Point(const.wire_btn_trigger_pos_x,
                        const.wire_btn_trigger_pos_y)),
    getCorrectPos(Point(const.battery_btn_trigger_pos_x,
                        const.battery_btn_trigger_pos_y)),
    getCorrectPos(Point(const.raven_path_btn_trigger_pos_x,
                        const.raven_path_btn_trigger_pos_y))
]
SelectModeScreen = Screen(ScreenStep.SelectMode, [], 30)

ResourcePrepareBattleScreen = Screen(
    ScreenStep.GetResourceMenu, const.resource_prepare_crops, 30)

BattlePreparationScreen = Screen(
    ScreenStep.BattlePrepareScreen, const.battle_preparation_crops, 1500)

InBattleScreen = Screen(ScreenStep.InBattleNow, [], 30)

FinishBattleScreen = Screen(
    ScreenStep.FinishBattleScreen, const.finish_battle_crops, 3000)


def bot():

    global isAlreadySelfDestruct
    global isAlreadyBackStirring
    global battleStartDelay
    global isFirstTimeAtLogin
    global detectedMap
    global isAlreadyExecutingTurn
    global isInAllowedZone
    global turnCommandStack

    InputControl.mouseClick(getCorrectPos(Point(400, 10)))
    ######################
    ## SET CURRENT STEP ##
    ######################
    currentStep = const.ScreenStep.BattlePrepareScreen

    # garage_map_mask = cv2.imread("./assets/garage_map_1_mask_2.png", 0)
    bridge_mask = cv2.imread(
        "./assets/maps_in_game_crop_gray/bridgemask.png", 0)
    # cv2.imshow('TrackingMaskMap',bridge_mask)

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

    print(d.displays)
    time.sleep(1)

    while True:
        np_frame = d.get_latest_frame()
        frame = cv2.cvtColor(np_frame, cv2.COLOR_BGR2RGB)

        test_frame = frame[const.battle_map_name_label_height_start:const.battle_map_name_label_height_end,
                           const.battle_map_name_label_width_start:const.battle_map_name_label_width_end]
        # test_frame = frame[174:920, 587:1330]
        cv2.imshow("TestCrop", test_frame)
        text = pytesseract.image_to_string(test_frame, lang='eng')
        print(text)

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
            elif screen.checkSingleSatisfy(frame, 0):
                screen.executeSingleClick(0)
            elif screen.checkSingleSatisfy(frame, 1):
                screen.executeSingleClick(1)
            elif screen.checkSingleSatisfy(frame, 2):
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
            InputControl.mouseClick(clickPos)
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
                win32api.keybd_event(0x09, 0, 0, 0)

            if screen.checkSingleSatisfy(prev_frame, 1):
                detectedMap = frame[174:920, 587:1330]
                win32api.keybd_event(0x09, 0, win32con.KEYEVENTF_KEYUP, 0)
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
                if battleStartDelay == False:

                    # prev_frame = d.get_frame(10)
                    prev_1_frame = d.get_frame(10)

                    # InputControl.KeyPress("t").start()
                    minimap_frame = frame[const.in_battle_mini_map_height_start:const.in_battle_mini_map_height_end,
                                          const.in_battle_mini_map_width_start: const.in_battle_mini_map_width_end]

                    ########## MINIMAP CHECK LOCATION #############
                    srcmap = detectedMap.copy()
                    grey_src_map = srcmap.copy()
                    grey_src_map = cv2.cvtColor(srcmap, cv2.COLOR_RGB2GRAY)
                    grey_minimap_frame = minimap_frame.copy()
                    scale_percent = 80  # percent of original size
                    new_width = int(
                        grey_minimap_frame.shape[1] * scale_percent / 100)
                    new_height = int(
                        grey_minimap_frame.shape[0] * scale_percent / 100)
                    dim = (new_width, new_height)
                    grey_minimap_frame = cv2.resize(
                        grey_minimap_frame, dim, interpolation=cv2.INTER_AREA)
                    grey_minimap_frame = cv2.cvtColor(
                        grey_minimap_frame, cv2.COLOR_RGB2GRAY)
                    w, h = grey_minimap_frame.shape[::-1]
                    method = eval('cv2.TM_CCOEFF')
                    res = cv2.matchTemplate(
                        grey_src_map, grey_minimap_frame, method)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                        top_left = min_loc
                    else:
                        top_left = max_loc
                    # bottom_right = (top_left[0] + w, top_left[1] + h)
                    # cv2.rectangle(grey_src_map, top_left, bottom_right, 255, 2)  ## Draw Template Rect on Src
                    circle_center_x = int(top_left[0] + w / 2)
                    circle_center_y = int(top_left[1] + h / 2)

                    map_mask = bridge_mask.copy()

                    cv2.circle(map_mask, (circle_center_x,
                                          circle_center_y), 2, (255, 255, 0), 2)

                    ########## TRACK MOVING DIRECTION #############

                    prev_1_minimap_frame = prev_1_frame[const.in_battle_mini_map_height_start:const.in_battle_mini_map_height_end,
                                                        const.in_battle_mini_map_width_start: const.in_battle_mini_map_width_end]
                    prev_grey_minimap_frame = prev_1_minimap_frame.copy()
                    prev_grey_minimap_frame = cv2.cvtColor(
                        prev_grey_minimap_frame, cv2.COLOR_BGR2GRAY)
                    prev_grey_minimap_frame = cv2.resize(
                        prev_grey_minimap_frame, dim, interpolation=cv2.INTER_AREA)
                    res2 = cv2.matchTemplate(
                        grey_src_map, prev_grey_minimap_frame, method)
                    min_val2, max_val2, min_loc2, max_loc2 = cv2.minMaxLoc(
                        res2)
                    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                        top_left2 = min_loc2
                    else:
                        top_left2 = max_loc2
                    circle_center_x2 = int(top_left2[0] + w / 2)
                    circle_center_y2 = int(top_left2[1] + h / 2)

                    # cv2.circle(grey_src_map, (circle_center_x2, circle_center_y2), 3, (255, 0, 0), 3)

                    if isAlreadyExecutingTurn is False:

                        detect_angle_rad = math.radians(45)
                        detect_distance = 10

                        center_rad = 0

                        if circle_center_x == circle_center_x2:
                            if circle_center_y > circle_center_y2:
                                center_rad = -1 * math.pi / 2
                            else:
                                center_rad = math.pi / 2
                        else:
                            center_tan = abs(
                                (circle_center_y - circle_center_y2) / (circle_center_x - circle_center_x2))
                            if circle_center_x > circle_center_x2:

                                if circle_center_y > circle_center_y2:  # BotRight
                                    center_rad = -1 * math.atan(center_tan)
                                else:  # TopRight
                                    center_rad = math.atan(center_tan)

                            else:
                                if circle_center_y > circle_center_y2:  # BotLeft
                                    center_rad = math.pi + \
                                        math.atan(center_tan)
                                else:  # TopLeft
                                    center_rad = math.pi - \
                                        math.atan(center_tan)

                        left_rad = center_rad + detect_angle_rad
                        right_rad = center_rad - detect_angle_rad

                        rad_list = [left_rad, center_rad, right_rad]

                        pos_list = []

                        # print(left_rad, center_rad,right_rad)

                        for rad in rad_list:
                            if rad > 0 and rad <= math.pi / 2:
                                pos_x = circle_center_x + \
                                    detect_distance * abs(math.cos(rad))
                                pos_y = circle_center_y - \
                                    detect_distance * abs(math.sin(rad))
                                pos_list.append((int(pos_x), int(pos_y)))
                            elif rad > math.pi / 2 and rad <= math.pi:
                                pos_x = circle_center_x - \
                                    detect_distance * abs(math.cos(rad))
                                pos_y = circle_center_y - \
                                    detect_distance * abs(math.sin(rad))
                                pos_list.append((int(pos_x), int(pos_y)))
                            elif (rad > math.pi and rad <= math.pi / 2 * 3) or (rad <= -1 * math.pi / 2):
                                pos_x = circle_center_x - \
                                    detect_distance * abs(math.cos(rad))
                                pos_y = circle_center_y + \
                                    detect_distance * abs(math.sin(rad))
                                pos_list.append((int(pos_x), int(pos_y)))
                            elif (rad > -1 * math.pi / 2 and rad <= 0) or (rad > math.pi / 2 * 3 and rad <= math.pi * 2):
                                pos_x = circle_center_x + \
                                    detect_distance * abs(math.cos(rad))
                                pos_y = circle_center_y + \
                                    detect_distance * abs(math.sin(rad))
                                pos_list.append((int(pos_x), int(pos_y)))
                            else:
                                print("Check Rad Failed")

                        left_pos = pos_list[0]
                        left_too_close = False if map_mask[left_pos[1],
                                                           left_pos[0]] == 0 else True
                        center_pos = pos_list[1]
                        center_too_close = False if map_mask[center_pos[1],
                                                             center_pos[0]] == 0 else True
                        right_pos = pos_list[2]
                        right_too_close = False if map_mask[right_pos[1],
                                                            right_pos[0]] == 0 else True

                        straight_block_time = 0
                        minor_turn_block_time = 0
                        right_angle_block_time = 1.2
                        extra_turn_block_time = 2
                        full_turn_block_time = 2.6

                        direction = const.MoveDirection.front
                        lastTurnCmd = const.MoveDirection.front
                        if len(turnCommandStack) > 0:
                            lastTurnCmd = turnCommandStack[0]

                        if center_too_close:
                            if left_too_close:
                                if right_too_close:  # 1 1 1
                                    if isInAllowedZone == False:
                                        direction = const.MoveDirection.front
                                        AutoGo(
                                            direction, straight_block_time).start()
                                    else:
                                        if lastTurnCmd == const.MoveDirection.frontRight or lastTurnCmd == const.MoveDirection.right:
                                            direction = const.MoveDirection.backRight
                                            AutoGo(
                                                direction, extra_turn_block_time).start()
                                        elif lastTurnCmd == const.MoveDirection.frontLeft or lastTurnCmd == const.MoveDirection.left:
                                            direction = const.MoveDirection.backLeft
                                            AutoGo(
                                                direction, extra_turn_block_time).start()
                                        else:
                                            direction = const.MoveDirection.back
                                            AutoGo(
                                                direction, full_turn_block_time).start()
                                else:  # 1 1 0
                                    direction = const.MoveDirection.right
                                    AutoGo(
                                        direction, right_angle_block_time).start()
                            else:
                                if right_too_close:  # 0 1 1
                                    direction = const.MoveDirection.left
                                    AutoGo(
                                        direction, right_angle_block_time).start()
                                else:  # 0 1 0
                                    if lastTurnCmd == const.MoveDirection.frontRight or lastTurnCmd == const.MoveDirection.right:
                                        direction = const.MoveDirection.right
                                        AutoGo(
                                            direction, right_angle_block_time).start()
                                    elif lastTurnCmd == const.MoveDirection.frontLeft or lastTurnCmd == const.MoveDirection.left:
                                        direction = const.MoveDirection.left
                                        AutoGo(
                                            direction, right_angle_block_time).start()
                        else:
                            isInAllowedZone = True
                            if left_too_close:
                                if right_too_close:  # 1 0 1
                                    direction = const.MoveDirection.front
                                    AutoGo(
                                        direction, straight_block_time).start()
                                else:  # 1 0 0
                                    direction = const.MoveDirection.frontRight
                                    AutoGo(
                                        direction, minor_turn_block_time).start()
                            else:
                                if right_too_close:  # 0 0 1
                                    direction = const.MoveDirection.frontLeft
                                    AutoGo(
                                        direction, minor_turn_block_time).start()
                                else:  # 0 0 0
                                    if lastTurnCmd == const.MoveDirection.frontRight or lastTurnCmd == const.MoveDirection.right:
                                        direction = const.MoveDirection.frontLeft
                                        AutoGo(
                                            direction, right_angle_block_time).start()
                                    elif lastTurnCmd == const.MoveDirection.frontLeft or lastTurnCmd == const.MoveDirection.left:
                                        direction = const.MoveDirection.frontRight
                                        AutoGo(
                                            direction, right_angle_block_time).start()
                        print(direction)
                        turnCommandStack.insert(0, direction)
                        if len(turnCommandStack) >= 5:
                            turnCommandStack.pop()

                        for pos in pos_list:
                            # if garage_map_mask[pos[0], pos[1]] == (0, 0, 0):
                            cv2.line(map_mask, (circle_center_x,
                                                circle_center_y), pos, (255, 0, 0), 1)
                            # cv2.circle(map_mask, pos, 1, (255, 0, 0), 1)

                    else:
                        # print("already in moving process")
                        pass
                        # InputControl.KeyPress("w")

                    cv2.imshow("TrackingMaskMap", map_mask)
                    cv2.imshow("TrackingSourceMap", grey_src_map)

                    ########## MINIMAP TRACK ENEMY COUNT #############
                    hsv_minimap_frame = cv2.cvtColor(
                        minimap_frame, cv2.COLOR_BGR2HSV)
                    lower_red = np.array([0, 180, 180])
                    upper_red = np.array([10, 255, 255])
                    mask = cv2.inRange(hsv_minimap_frame, lower_red, upper_red)
                    if cv2.countNonZero(mask) > 10:
                        executeOrder66()

                    ########## FRONT VIEW CHECK STUCK #############
                    # front_frame = np_frame[const.in_battle_front_view_height_start:const.in_battle_front_view_height_end,
                    #                        const.in_battle_front_view_width_start:const.in_battle_front_view_width_end]
                    # prev_front_frame = prev_1_frame[const.in_battle_front_view_height_start:const.in_battle_front_view_height_end,
                    #                               const.in_battle_front_view_width_start:const.in_battle_front_view_width_end]
                    # comp = cv2.absdiff(front_frame, prev_front_frame)
                    # res = comp.astype(np.uint8)
                    # percentage = (np.count_nonzero(res) * 100) / res.size
                    # if percentage < 75:
                    #     determineBackStir()

                    ########## HEALTH BAR CHECK HEALTH #############
                    # health_frame = frame[ const.in_battle_health_digit_height_start:const.in_battle_health_digit_height_end, const.in_battle_health_digit_width_start:const.in_battle_health_digit_width_end ]
                    # a = pytesseract.image_to_string(health_frame)
                    # try:
                    #     inta = int(a)
                    #     if (inta <= 150):
                    #         selfDesctruct()
                    # except ValueError:
                    #     pass
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
    InputControl.keyRelease("m")
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
    InputControl.keyRelease("w")
    InputControl.keyRelease("a")
    InputControl.keyRelease("s")
    InputControl.keyRelease("d")
    InputControl.keyRelease("m")


def calllOut():
    calloutLst = ["b", "c", "x", "z"]
    callout = random.choice(list(calloutLst))
    InputControl.KeyPress(callout).start()


def carJack():
    InputControl.KeyPress("r").start()


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
    InputControl.keyRelease("w")
    InputControl.keyRelease("a")
    InputControl.keyRelease("s")
    InputControl.keyRelease("d")


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

    InputControl.keyRelease("w")

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
        InputControl.KeyPress("d", 0.73).start()

        leftShortBackStirTimer3 = threading.Timer(1, finish)
        leftShortBackStirTimer3.start()

    def turnForwardLeft():
        global leftShortBackStirTimer1
        global leftShortBackStirTimer2
        leftShortBackStirTimer1.cancel()
        InputControl.KeyPress("w", 2.65).start()
        InputControl.KeyPress("a", 1.65).start()

        leftShortBackStirTimer2 = threading.Timer(2.75, turnFinalRight)
        leftShortBackStirTimer2.start()

    InputControl.KeyPress("s", 1.6).start()

    leftShortBackStirTimer1 = threading.Timer(1.7, turnForwardLeft)
    leftShortBackStirTimer1.start()


rightLongBackStirTimer1 = None
rightLongBackStirTimer2 = None
rightLongBackStirTimer3 = None


def rightLongBackStir():
    global isAlreadyBackStirring

    isAlreadyBackStirring = True
    InputControl.keyRelease("w")

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
        InputControl.KeyPress("a", 0.72).start()

        rightLongBackStirTimer3 = threading.Timer(1, finish)
        rightLongBackStirTimer3.start()

    def turnForwardRight():
        global rightLongBackStirTimer1
        global rightLongBackStirTimer2

        rightLongBackStirTimer1.cancel()
        InputControl.KeyPress("w", 3.5).start()
        InputControl.KeyPress("d", 1.75).start()

        rightLongBackStirTimer2 = threading.Timer(3.6, turnFinalLeft)
        rightLongBackStirTimer2.start()

    InputControl.KeyPress("s", 2.4).start()

    rightLongBackStirTimer1 = threading.Timer(2.5, turnForwardRight)
    rightLongBackStirTimer1.start()


fullreverseBackStirTimer1 = None
fullreverseBackStirTimer2 = None


def full_reverse_back_stir():
    global isAlreadyBackStirring

    isAlreadyBackStirring = True
    InputControl.keyRelease("w")

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
        InputControl.KeyPress("a", 2.4).start()

        fullreverseBackStirTimer2 = threading.Timer(3, finish)
        fullreverseBackStirTimer2.start()

    InputControl.KeyPress("s", 2.1).start()

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
            InputControl.KeyPress("d", 0.3).start()
            lastStir = "d"
        else:
            InputControl.KeyPress("a", 0.3).start()
            lastStir = "a"


def executeOrder66():
    # print("<< In Battle >> Attack")
    InputControl.KeyPress("1").start()


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
