import time, threading, random, operator

import d3dshot

import cv2

import pytesseract

import InputTrigger

from protobuf_settings import Settings

import numpy as np

import Constants as const



def getCorrectPos(pos):
    return (int(Settings().settings.shiftX + pos[0]), int(Settings().settings.shiftY + pos[1]))




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

    def checkSatisfy(self, frame) -> bool:
        for crop in self.crops:
            crop_frame = frame[crop.area.y:crop.area.ys, crop.area.x:crop.area.xs]
            low_txt = pytesseract.image_to_string(crop_frame, lang='eng').lower()
            if crop.requiredMatch and (low_txt not in crop.expectedStrs):
                return False
            pass
        print("Step", self.screenStep.name, ">>>> SATISFIED")
        return True
    
    def executeClick(self):
        for crop in self.crops:
            if crop.willClick:
                InputTrigger.mouseClick(getCorrectPos(crop.clickPos))
                time.sleep(crop.clickWaitTime)

    def addFailCount(self) -> bool:
        self.retryCount += 1
        if self.retryCount >= self.allowedRetryCount:
            self.retryCount = 0
            print("Step", self.screenStep.name, ">>>> FAILED")
            return False
        return True
        


def bot():

    global isAlreadySelfDestruct
    global isAlreadyBackStirring
    global battleStartDelay

    currentStep = const.ScreenStep.MainMenu

    login_crops = [
        CropProperty(
            "Login Button",
            CropArea(const.login_label_width_start, const.login_label_height_start, const.login_label_width_end, const.login_label_height_end),
            True,
            Point(const.login_label_trigger_pos_x, const.login_label_trigger_pos_y),
            True,
            ["login","log in", "log ln", "logln"],
            5
        )
    ]
    LoginScreen = Screen(const.ScreenStep.Login, login_crops, 30)

    welcome_crops = [
        CropProperty(
            "Welcome Promo Close Button",
            CropArea(const.welcome_promo_label_width_start, const.welcome_promo_label_height_start, const.welcome_promo_label_width_end, const.welcome_promo_label_height_end),
            True,
            Point(const.welcome_promo_label_trigger_pos_x, const.welcome_promo_label_trigger_pos_y),
            True,
            ["close", "c1ose", "ciose"],
            1
        )
    ]
    WelcomeScreen = Screen(const.ScreenStep.WelcomeScreen, welcome_crops, 30)
    
    mainmenu_challenge_crops = [
        CropProperty(
            "Mainmenu Challenge Complete OK Button",
            CropArea(const.mainmenu_challenge_complete_ok_width_start, const.mainmenu_challenge_complete_ok_height_start, const.mainmenu_challenge_complete_ok_width_end, const.mainmenu_challenge_complete_ok_height_end),
            True,
            Point(const.mainmenu_challenge_complete_ok_trigger_pos_x, const.mainmenu_challenge_complete_ok_trigger_pos_y),
            True,
            ["ok", "0k"],
            1
        )
    ]
    ChallengeCompleteScreen = Screen(const.ScreenStep.ChallengeCompleteScreen, mainmenu_challenge_crops, 30)
    
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
        getCorrectPos((const.battery_btn_trigger_pos_x, const.battery_btn_trigger_pos_y))
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
    BattlePreparationScreen = Screen(const.ScreenStep.BattlePrepareScreen, battle_preparation_crops, 2000)

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
            3
        ),
        CropProperty(
            "Finish Battle BATTLE Button",
            CropArea(const.finish_battle_battle_label_width_start, const.finish_battle_battle_label_height_start, const.finish_battle_battle_label_width_end, const.finish_battle_battle_label_height_end),
            False,
            Point(const.finish_battle_battle_label_trigger_pos_x, const.finish_battle_battle_label_trigger_pos_y),
            False,
            ["battle", "batt1e"],
            3
        )
    ]

    FinishBattleScreen = Screen(const.ScreenStep.FinishBattleScreen, finish_battle_crops, 5000)

    d = d3dshot.create(capture_output='numpy')
    if (len(d.displays) > 1):
        d.display = d.displays[1]
    else:
        d.display = d.displays[0]
    d.capture(target_fps=10, region=(0, 0, const.screenWidth, const.screenHeight))
    time.sleep(1)

    while True:

        np_frame = d.get_latest_frame()
        prev_frame = d.get_frame(10)
        frame = cv2.cvtColor(np_frame, cv2.COLOR_BGR2RGB)

        # test_frame = frame[ const.battle_victory_defeat_giant_width_height_start:const.battle_victory_defeat_giant_width_height_end, const.battle_victory_defeat_giant_width_start:const.battle_victory_defeat_giant_width_end ]
        # cv2.imshow("TestCrop", test_frame)
        # text = pytesseract.image_to_string(test_frame, lang='eng')
        # print(text)
        # if (text.lower == "victory" or text.lower == "defeat"):
        #     print("Good")

        if currentStep == const.ScreenStep.Login:
            screen = LoginScreen
            if screen.checkSatisfy(frame):
                screen.executeClick()
                currentStep += 1
            elif screen.addFailCount():
                pass
            else:
                currentStep += 1

        elif currentStep == const.ScreenStep.WelcomeScreen:
            screen = WelcomeScreen
            if screen.checkSatisfy(frame):
                screen.executeClick()
                currentStep += 1
            elif screen.addFailCount():
                pass
            else:
                currentStep += 1

        elif currentStep == const.ScreenStep.ChallengeCompleteScreen:
            screen = ChallengeCompleteScreen
            if screen.checkSatisfy(frame):
                screen.executeClick()
            elif screen.addFailCount():
                pass
            else:
                currentStep += 1

        elif currentStep == const.ScreenStep.MainMenu:
            screen = MainMenuScreen
            if screen.checkSatisfy(frame):
                screen.executeClick()
                currentStep += 1
            elif screen.addFailCount():
                pass
            else:
                currentStep += 1

        elif currentStep == const.ScreenStep.SelectMode:
            clickPos = random.choice(select_mode_click_pos)
            InputTrigger.mouseClick(clickPos)
            time.sleep(1)
            currentStep += 1
            
        elif currentStep == const.ScreenStep.GetResourceMenu:
            screen = ResourcePrepareBattleScreen
            if screen.checkSatisfy(frame):
                screen.executeClick()
                currentStep += 1
            elif screen.addFailCount():
                pass
            else:
                currentStep += 1
        
        elif currentStep == const.ScreenStep.BattlePrepareScreen:
            screen = BattlePreparationScreen
            if screen.checkSatisfy(frame):
                screen.executeClick()
                currentStep += 1
            elif screen.addFailCount():
                pass
            else:
                currentStep += 1

        elif currentStep == const.ScreenStep.InBattleNow:
            screen = InBattleScreen
            DoBattleNow()
            currentStep += 1

        elif currentStep == const.ScreenStep.DeathWaiting:
            currentStep += 1

        elif currentStep == const.ScreenStep.FinishBattleScreen:
            screen = FinishBattleScreen
            if screen.checkSatisfy(frame):
                battleEnded()
                screen.executeClick()
                currentStep = const.ScreenStep.ChallengeCompleteScreen
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
                    if percentage < 85:
                        backStir()

                    health_frame = frame[ const.in_battle_health_digit_height_start:const.in_battle_health_digit_height_end, const.in_battle_health_digit_width_start:const.in_battle_health_digit_width_end ]
                    a = pytesseract.image_to_string(health_frame)
                    try:
                        inta = int(a)
                        if (inta <= 200):
                            selfDesctruct()
                    except ValueError:
                        pass
            else:
                battleEnded()
                currentStep = const.ScreenStep.ChallengeCompleteScreen

        else:
            print("CURRENT STEP:", currentStep)
        
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


def backStir4():
    global backStirTimer3
    global shortBackStirCount
    global needLongBackStir
    try:
        if backStirTimer3: 
            backStirTimer3.cancel()
    except ValueError:
        pass
    if shortBackStirCount >= 2:
        needLongBackStir = True
    shortBackStirCount = 0

def backStir3():
    global backStirDirection
    global backStirTimer2
    global backStirTimer3
    global isAlreadyBackStirring

    try:
        if backStirTimer2: 
            backStirTimer2.cancel()
    except ValueError:
        pass
    isAlreadyBackStirring = False
    backStirTimer3 = threading.Timer(20, backStir4)
    backStirTimer3.start()

def backStir2():
    global backStirTimer1
    global backStirTimer2
    try:
        if backStirTimer1: 
            backStirTimer1.cancel()
    except ValueError:
        pass
    InputTrigger.keyHold("w")
    backStirTimer2 = threading.Timer(3, backStir3)
    backStirTimer2.start()
        
def backStir():
    # print("<< In Battle >> Backing")
    global shortBackStirCount
    global backStirDirection
    global backStirTimer1
    global isAlreadyBackStirring
    global needLongBackStir

    if isAlreadyBackStirring:
        pass
    else:
        isAlreadyBackStirring = True
        InputTrigger.keyRelease("w")
        InputTrigger.keyRelease("a")
        InputTrigger.keyRelease("s")
        InputTrigger.keyRelease("d")
        moveLst = ["a", "d"]
        # ranPara = random.choice(moveLst)
        backStirDirection = random.choice(moveLst)
        InputTrigger.KeyPress("s", 2.5).start()
        if needLongBackStir:
            InputTrigger.KeyPress(backStirDirection, 1.75).start()
            needLongBackStir = False
        else:
            InputTrigger.KeyPress(backStirDirection, 1.5).start()
            shortBackStirCount += 1

        backStirTimer1 = threading.Timer(2.65, backStir2)
        backStirTimer1.start() 
        
lastStir = "a"

def stirringHorizontal():
    # print("<< In Battle >> Stirring")
    global lastStir
    global isAlreadyBackStirring
    if isAlreadyBackStirring:
        pass
    else:
        InputTrigger.keyRelease("a")
        InputTrigger.keyRelease("d")
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
    
    stirInterval = setInterval(6, stirringHorizontal)
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


