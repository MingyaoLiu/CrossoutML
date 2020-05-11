import time, threading, random, operator

import d3dshot

import cv2

import pytesseract

import InputTrigger

import protobuf_settings as ProtoSetting

import numpy as np

import Constants as const





def getCorrectPos(pos):
    return (int(ProtoSetting.getGlobalSetting().settings.shiftX + pos[0]), int(ProtoSetting.getGlobalSetting().settings.shiftY + pos[1]))



lastFullyCompleteStep = 0
isAlreadySelfDestruct = False
isBattleAlreadyActive = False
isAlreadyBackStirring = False
battleStartDelay = True
battleStartDelayTimer = None

class Point(tuple):
    def __new__(self, x, y):
        Point.x = property(operator.itemgetter(0))
        Point.y = property(operator.itemgetter(1))
        return tuple.__new__(Point, (x, y))

class CropArea(tuple):
    def __new__(self, x, y, xs, ys):
        CropArea.x = property(operator.itemgetter(0))
        CropArea.y = property(operator.itemgetter(1))
        CropArea.xs = property(operator.itemgetter(2))
        CropArea.ys = property(operator.itemgetter(3))
        return tuple.__new__(CropArea, (x, y, xs, ys))

class CropProperty(tuple):
    def __new__(self, name: str, area: CropArea, requiredMatch: bool, clickPos: Point, willClick: bool, expectedStrs: [str],  clickWaitTime: int):
        CropProperty.name = property(operator.itemgetter(0))
        CropProperty.area = property(operator.itemgetter(1))
        CropProperty.requiredMatch = property(operator.itemgetter(2))
        CropProperty.clickPos = property(operator.itemgetter(3))
        CropProperty.willClick = property(operator.itemgetter(4))
        CropProperty.expectedStrs = property(operator.itemgetter(5))
        CropProperty.clickWaitTime = property(operator.itemgetter(6))
        return tuple.__new__(CropProperty, (name, area, requiredMatch, clickPos, willClick, expectedStrs, clickWaitTime))

class Screen():

    def __init__(self, screenStep: const.ScreenStep, crops: [CropProperty], allowedRetryCount: int):
        self.screenStep = screenStep
        self.crops = crops
        self.allowedRetryCount = allowedRetryCount
        self.retryCount = 0

    def checkSingleSatisfy(self, frame, index) -> bool:
        crop = self.crops[index]
        crop_frame = frame[crop.area.y:crop.area.ys, crop.area.x:crop.area.xs]
        low_txt = pytesseract.image_to_string(crop_frame, lang='eng').lower()
        if crop.requiredMatch and (low_txt not in crop.expectedStrs):
            return False
        return True
    

    def checkSatisfy(self, frame) -> bool:
        for i in range(len( self.crops)):
            if self.checkSingleSatisfy(frame, i):
                pass
            else:
                return False
        print("Step", self.screenStep.name, ">>>> SATISFIED")
        return True
    
    def executeSingleClick(self, index):
        crop = self.crops[index]
        if crop.willClick:
            InputTrigger.mouseClick(getCorrectPos(crop.clickPos))
            time.sleep(crop.clickWaitTime)

    def executeClick(self):
        for i in range(len(self.crops)):
            self.executeSingleClick(i)


    def addFailCount(self) -> bool:
        if self.retryCount == 0 or self.retryCount % 100 == 0:
            print("Retrying Step: ", self.screenStep.name, self.retryCount)
        self.retryCount += 1
        if self.retryCount >= self.allowedRetryCount:
            print("Step", self.screenStep.name, ">>>> FAILED")
            return False
        return True

    def resetRetryCount(self):
        self.retryCount = 0
        

import win32api
import win32con


isFirstTimeAtLogin = True

def bot():

    global isAlreadySelfDestruct
    global isAlreadyBackStirring
    global battleStartDelay
    global isFirstTimeAtLogin


    InputTrigger.mouseClick(getCorrectPos((100, 10)))
    ######################
    ## SET CURRENT STEP ##
    ######################
    currentStep = const.ScreenStep.Login

    login_crops = [
        CropProperty(
            "Exit No Button",
            CropArea(const.login_exit_no_width_start, const.login_exit_no_height_start, const.login_exit_no_width_end, const.login_exit_no_height_end),
            True,
            Point(const.login_exit_no_trigger_pos_x, const.login_exit_no_trigger_pos_y),
            True,
            ["no"],
            1
        ),
        CropProperty(
            "Escape Return Button",
            CropArea(const.esc_return_button_width_start, const.esc_return_button_height_start, const.esc_return_button_width_end, const.esc_return_button_height_end),
            True,
            Point(const.esc_return_button_trigger_pos_x, const.esc_return_button_trigger_pos_y),
            True,
            ["return", "toate"],
            1
        ),

        CropProperty(
            "Login Button",
            CropArea(const.login_label_width_start, const.login_label_height_start, const.login_label_width_end, const.login_label_height_end),
            True,
            Point(const.login_label_trigger_pos_x, const.login_label_trigger_pos_y),
            True,
            ["login","log in", "log ln", "logln"],
            10
        )
    ]
    LoginScreen = Screen(const.ScreenStep.Login, login_crops, 10)

    welcome_crops = [
        CropProperty(
            "Welcome Promo Close Button",
            CropArea(const.welcome_promo_label_width_start, const.welcome_promo_label_height_start, const.welcome_promo_label_width_end, const.welcome_promo_label_height_end),
            True,
            Point(const.welcome_promo_label_trigger_pos_x, const.welcome_promo_label_trigger_pos_y),
            True,
            ["close", "c1ose", "ciose"],
            2
        )
    ]
    WelcomeScreen = Screen(const.ScreenStep.WelcomeScreen, welcome_crops, 10)

    mainmenu_master_jack_crops = [
        CropProperty(
            "Mainmenu MasterJack Upgrade level Close",
            CropArea(const.co_pilot_upgrade_close_width_start, const.co_pilot_upgrade_close_height_start, const.co_pilot_upgrade_close_width_end, const.co_pilot_upgrade_close_height_end),
            True,
            Point(const.co_pilot_upgrade_close_trigger_pos_x, const.co_pilot_upgrade_close_trigger_pos_x),
            True,
            ["close", "c1ose"],
            2
        )
    ]
    MasterJackUpgradeScreen = Screen(const.ScreenStep.MasterJackUpgradeScreen, mainmenu_master_jack_crops, 10)

    mainmenu_challenge_crops = [
        CropProperty(
            "Mainmenu Challenge Complete OK Button",
            CropArea(const.mainmenu_challenge_complete_ok_width_start, const.mainmenu_challenge_complete_ok_height_start, const.mainmenu_challenge_complete_ok_width_end, const.mainmenu_challenge_complete_ok_height_end),
            True,
            Point(const.mainmenu_challenge_complete_ok_trigger_pos_x, const.mainmenu_challenge_complete_ok_trigger_pos_y),
            True,
            ["ok", "0k"],
            2
        )
    ]
    ChallengeCompleteScreen = Screen(const.ScreenStep.ChallengeCompleteScreen, mainmenu_challenge_crops, 10)
    
    mainmenu_crops = [
        CropProperty(
            "Main Menu Battle Button",
            CropArea(const.mainmenu_battle_label_width_start, const.mainmenu_battle_label_height_start, const.mainmenu_battle_label_width_end, const.mainmenu_battle_label_height_end),
            False,
            Point(const.mainmenu_battle_label_trigger_pos_x, const.mainmenu_battle_label_trigger_pos_y),
            False,
            ["battle", "batt1e"],
            1
        ),
        CropProperty(
            "Main Menu Select Mode Button",
            CropArea(const.mainmenu_select_mode_label_width_start, const.mainmenu_select_mode_label_height_start, const.mainmenu_select_mode_label_width_end, const.mainmenu_select_mode_label_height_end),
            True,
            Point(const.mainmenu_select_mode_label_trigger_pos_x, const.mainmenu_select_mode_label_trigger_pos_y),
            True,
            ["select mode", "selectmode", "se1ect mode"],
            1
        )
    ]
    MainMenuScreen = Screen(const.ScreenStep.MainMenu, mainmenu_crops, 30)

    select_mode_click_pos = [
        getCorrectPos((const.scrap_btn_trigger_pos_x, const.scrap_btn_trigger_pos_y)),
        getCorrectPos((const.wire_btn_trigger_pos_x, const.wire_btn_trigger_pos_y)),
        getCorrectPos((const.battery_btn_trigger_pos_x, const.battery_btn_trigger_pos_y)),
        getCorrectPos((const.raven_path_btn_trigger_pos_x, const.raven_path_btn_trigger_pos_y))
    ]
    SelectModeScreen = Screen(const.ScreenStep.SelectMode, [], 30)

    resource_prepare_crops = [
        CropProperty(
            "Scrap/Wire/Battery Prepare to Battle Button",
            CropArea(const.get_resource_battle_label_width_start, const.get_resource_battle_label_height_start, const.get_resource_battle_label_width_end, const.get_resource_battle_label_height_end),
            True,
            Point(const.get_resource_battle_label_trigger_pos_x, const.get_resource_battle_label_trigger_pos_y),
            True,
            ["battle", "batt1e"],
            1
        ),
        CropProperty(
            "Patrol Mode Prepare to Battle Button",
            CropArea(const.get_resource_battle_label_width_start, const.get_resource_patrol_battle_label_height_start, const.get_resource_battle_label_width_end, const.get_resource_patrol_battle_label_height_end),
            False,
            Point(const.get_resource_patrol_battle_label_trigger_pos_x, const.get_resource_patrol_battle_label_trigger_pos_y),
            False,
            ["battle", "batt1e"],
            1
        )
    ]
    ResourcePrepareBattleScreen = Screen(const.ScreenStep.GetResourceMenu, resource_prepare_crops, 30)

    battle_preparation_crops = [
        CropProperty(
            "Prepare to Battle Summary Screen Title",
            CropArea(const.battle_type_title_label_width_start, const.battle_type_title_label_height_start, const.battle_type_title_label_width_end, const.battle_type_title_label_height_end),
            True,
            Point(const.mainmenu_challenge_complete_ok_trigger_pos_x, const.mainmenu_challenge_complete_ok_trigger_pos_y),
            False,
            ["assault", "encounter", "domination"],
            1
        )
    ]
    BattlePreparationScreen = Screen(const.ScreenStep.BattlePrepareScreen, battle_preparation_crops, 1500)

    # in_battle_crops = [
    #     CropProperty(
    #         "Defeat / Victory Screen",
    #         CropArea(const.battle_lose_survivor_part_width_start, const.battle_lose_survivor_part_height_start, const.battle_lose_survivor_part_width_end, const.battle_lose_survivor_part_height_end),
    #         False,
    #         Point(const.battle_lose_survivor_part_trigger_pos_x, const.battle_lose_survivor_part_trigger_pos_y),
    #         False,
    #         ["survivor's parts", "survivors parts", "survivorsparts"],
    #         1
    #     ),
    #     CropProperty(
    #         "Survivor's Kit",
    #         CropArea(const.battle_lose_survivor_part_width_start, const.battle_lose_survivor_part_height_start, const.battle_lose_survivor_part_width_end, const.battle_lose_survivor_part_height_end),
    #         False,
    #         Point(const.battle_lose_survivor_part_trigger_pos_x, const.battle_lose_survivor_part_trigger_pos_y),
    #         False,
    #         ["survivor's parts", "survivors parts", "survivorsparts"],
    #         1
    #     )
    # ]
    InBattleScreen = Screen(const.ScreenStep.InBattleNow, [], 30)

    finish_battle_crops = [
        CropProperty(
            "Finish Battle Close Button",
            CropArea(const.finish_battle_close_label_width_start, const.finish_battle_close_label_height_start, const.finish_battle_close_label_width_end, const.finish_battle_close_label_height_end),
            True,
            Point(const.finish_battle_close_label_trigger_pos_x, const.finish_battle_close_label_trigger_pos_y),
            True,
            ["close", "c1ose"],
            1
        ),
        CropProperty(
            "Finish Battle BATTLE Button",
            CropArea(const.finish_battle_battle_label_width_start, const.finish_battle_battle_label_height_start, const.finish_battle_battle_label_width_end, const.finish_battle_battle_label_height_end),
            False,
            Point(const.finish_battle_battle_label_trigger_pos_x, const.finish_battle_battle_label_trigger_pos_y),
            False,
            ["battle", "batt1e"],
            1
        )
    ]

    FinishBattleScreen = Screen(const.ScreenStep.FinishBattleScreen, finish_battle_crops, 3000)

    d = d3dshot.create(capture_output='numpy')
    if (len(d.displays) > 1):
        d.display = d.displays[1]
        ProtoSetting.getGlobalSetting().settings.shiftX = -2560
        ProtoSetting.getGlobalSetting().saveSettings()
    else:
        d.display = d.displays[0]
        ProtoSetting.getGlobalSetting().settings.shiftX = 0
        ProtoSetting.getGlobalSetting().saveSettings()
    d.capture(target_fps=10, region=(0, 0, const.screenWidth, const.screenHeight))
    time.sleep(1)

    while True:

        np_frame = d.get_latest_frame()
        prev_frame = d.get_frame(10)
        frame = cv2.cvtColor(np_frame, cv2.COLOR_BGR2RGB)


        # test_frame = frame[ const.esc_return_button_height_start:const.esc_return_button_height_end,const.esc_return_button_width_start:const.esc_return_button_width_end ]
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
            InputTrigger.mouseClick(clickPos)
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
            if screen.checkSatisfy(frame):
                screen.resetRetryCount()
                screen.executeClick()
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
                battleEnded()
                screen.resetRetryCount()
                screen.executeClick()
                currentStep = const.ScreenStep.Login
            elif screen.addFailCount():
                if battleStartDelay == False:
                    InputTrigger.KeyPress("t").start()
                    test_frame = frame[const.in_battle_mini_map_height_start:const.in_battle_mini_map_height_end, const.in_battle_mini_map_width_start:const.in_battle_mini_map_width_end ]
                    hsv = cv2.cvtColor(test_frame, cv2.COLOR_BGR2HSV)
                    lower_red = np.array([0,180,180])
                    upper_red = np.array([10,255,255])
                    mask = cv2.inRange(hsv, lower_red, upper_red)
                    if cv2.countNonZero(mask) > 10:
                        executeOrder66()
                        
                    front_frame = np_frame[const.in_battle_front_view_height_start:const.in_battle_front_view_height_end, const.in_battle_front_view_width_start:const.in_battle_front_view_width_end]
                    prev_front_frame = prev_frame[const.in_battle_front_view_height_start:const.in_battle_front_view_height_end, const.in_battle_front_view_width_start:const.in_battle_front_view_width_end]

                    comp = cv2.absdiff(front_frame, prev_front_frame)
                    res = comp.astype(np.uint8)
                    percentage = (np.count_nonzero(res) * 100) / res.size
                    if percentage < 75:
                        determineBackStir()

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


class setInterval :
    def __init__(self,interval,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stopEvent.set()

destructTimer = None

def destructComplete():
    global destructTimer
    global isAlreadySelfDestruct
    InputTrigger.keyRelease("m")
    isAlreadySelfDestruct = True
    destructTimer.cancel()

def selfDesctruct():
    global destructTimer
    global isAlreadySelfDestruct
    if isAlreadySelfDestruct == False:
        InputTrigger.keyHold("m")
        destructTimer = threading.Timer(5.0, destructComplete )
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
    InputTrigger.keyRelease("w")
    InputTrigger.keyRelease("a")
    InputTrigger.keyRelease("s")
    InputTrigger.keyRelease("d")
    InputTrigger.keyRelease("m")


def calllOut():
    calloutLst = ["b", "c", "x", "z"]
    callout = random.choice(list(calloutLst))
    InputTrigger.KeyPress(callout).start()

def carJack():
    InputTrigger.KeyPress("r").start()

total_back_stir_count = 0
left_short_back_stir_in_a_roll = 0
right_long_back_stir_in_a_roll = 0


## Left 3, RIght 3, back

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

def checkFullStuck():
    if left_short_back_stir_in_a_roll > 0:
        selfDesctruct()

def determineBackStir():
    global isAlreadyBackStirring
    global left_short_back_stir_in_a_roll
    global right_long_back_stir_in_a_roll
    global total_back_stir_count

    
    if isAlreadyBackStirring == False and total_back_stir_count < 6:
        total_back_stir_count += 1
    elif isAlreadyBackStirring == False and total_back_stir_count >= 6:
        selfDesctruct()
    
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

def leftShortBackStir():
    global left_short_back_stir_in_a_roll
    global isAlreadyBackStirring


    isAlreadyBackStirring = True

    InputTrigger.keyRelease("w")

    global leftShortBackStirTimer1
    global leftShortBackStirTimer2
    global leftShortBackStirTimer3


    rollBackOneTimer = threading.Timer(20, setBackByOneLeftShortBackStirCount)
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
        InputTrigger.keyHold("w")
        InputTrigger.KeyPress("d", 0.73).start()

        leftShortBackStirTimer3 = threading.Timer(1, finish)
        leftShortBackStirTimer3.start()

    def turnForwardLeft():
        global leftShortBackStirTimer1
        global leftShortBackStirTimer2
        leftShortBackStirTimer1.cancel()
        InputTrigger.KeyPress("w", 2.55).start()
        InputTrigger.KeyPress("a", 2).start()

        leftShortBackStirTimer2 = threading.Timer(2.75, turnFinalRight)
        leftShortBackStirTimer2.start()

    InputTrigger.KeyPress("s", 1.4).start()
        
    leftShortBackStirTimer1 = threading.Timer(1.7, turnForwardLeft)
    leftShortBackStirTimer1.start()
        

rightLongBackStirTimer1 = None
rightLongBackStirTimer2 = None
rightLongBackStirTimer3 = None

def rightLongBackStir():
    global isAlreadyBackStirring

    isAlreadyBackStirring = True
    InputTrigger.keyRelease("w")


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
        InputTrigger.keyHold("w")
        InputTrigger.KeyPress("a", 0.72).start()

        rightLongBackStirTimer3 = threading.Timer(1, finish)
        rightLongBackStirTimer3.start()

    def turnForwardRight():
        global rightLongBackStirTimer1
        global rightLongBackStirTimer2

        rightLongBackStirTimer1.cancel()
        InputTrigger.KeyPress("w", 3.5).start()
        InputTrigger.KeyPress("d", 2).start()

        rightLongBackStirTimer2 = threading.Timer(3.8, turnFinalLeft)
        rightLongBackStirTimer2.start()

    InputTrigger.KeyPress("s", 2.2).start()
        
    rightLongBackStirTimer1 = threading.Timer(2.5, turnForwardRight)
    rightLongBackStirTimer1.start()
        

fullreverseBackStirTimer1 = None
fullreverseBackStirTimer2 = None

def full_reverse_back_stir():
    global isAlreadyBackStirring

    isAlreadyBackStirring = True
    InputTrigger.keyRelease("w")

    global fullreverseBackStirTimer1
    global fullreverseBackStirTimer2


    fullStuckTimer = threading.Timer(20, checkFullStuck)
    fullStuckTimer.start()



    def finish():
        global isAlreadyBackStirring
        global fullreverseBackStirTimer2
        fullreverseBackStirTimer2.cancel()
        isAlreadyBackStirring = False

    def turnAround():
        global fullreverseBackStirTimer1
        global fullreverseBackStirTimer2
        fullreverseBackStirTimer1.cancel()
        InputTrigger.keyHold("w")
        InputTrigger.KeyPress("a", 2.2).start()

        fullreverseBackStirTimer2 = threading.Timer(5, finish)
        fullreverseBackStirTimer2.start()



    InputTrigger.KeyPress("s", 2.1).start()
        
    fullreverseBackStirTimer1 = threading.Timer(3, turnAround)
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
            InputTrigger.KeyPress("d", 0.3).start()
            lastStir = "d"
        else:
            InputTrigger.KeyPress("a", 0.3).start()
            lastStir = "a"

def executeOrder66():
    # print("<< In Battle >> Attack")
    InputTrigger.KeyPress("1").start()

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
    
    stirInterval = setInterval(8, stirringHorizontal)
    calloutInterval = setInterval(40, calllOut)
    carJackInterval = setInterval(10, carJack)



def DoBattleNow():
    global isAlreadySelfDestruct
    global isBattleAlreadyActive
    global battleStartDelayTimer
    if isBattleAlreadyActive:
        # print("Battle Happening")
        pass
    else:
        isBattleAlreadyActive = True
        battleStartDelayTimer = threading.Timer(18, delayBattleStart)
        battleStartDelayTimer.start() 
        InputTrigger.keyHold("w")


