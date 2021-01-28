import operator


#######################################################
##                      Dicts                        ##
#######################################################


map_mask_file_path = {
    # "engineer garage": "./assets/maps_masks/garage_map_1_mask.png",
    "engineer garage": "./assets/maps_masks/garage_map_3_mask.png",
    "naukograd": "./assets/maps_masks/naukugrad_mask_v2.png",
    "sandy gulf": "./assets/maps_masks/sandy_gulf_mask_v2.png",
    "sector ex": "./assets/maps_masks/sector_ex_mask_v2.png",
    "rock city": "./assets/maps_masks/rock_city_mask_v2.png",
    "founders canyon": "./assets/maps_masks/founders_canyon_mask_v2.png",
    "factory": "./assets/maps_masks/factory_mask_v2.png",
    "bridge": "./assets/maps_masks/bridge_mask_v2.png",
    "powerplant": "./assets/maps_masks/powerplant_mask_v2.png",
    "old town": "./assets/maps_masks/default_test_v2.png",
    "broken arrow": "./assets/maps_masks/broken_arrow_mask_v2.png",
    "fortress": "./assets/maps_masks/fortress_mask_v2.png",
    "“control-17” station": "./assets/maps_masks/control-17_station_mask_v2.png",
    "ship graveyard": "./assets/maps_masks/ship_graveyard_mask_v2.png",
    "desert valley": "./assets/maps_masks/desert_valley_mask_v2.png",
    "nameless tower": "./assets/maps_masks/nameless tower_mask_v2.png",
    "chemical plant": "./assets/maps_masks/chemical_plant_mask_v2.png",
    "crater": "./assets/maps_masks/crater_mask_v2.png",
    "clean island": "./assets/maps_masks/clean_island_mask_v2.png",
    "ravagers foothold": "./assets/maps_masks/ravagers_foothold_mask_v2.png",
    "ashen ring": "./assets/maps_masks/ashen_ring_mask_v2.png",
}

#######################################################
##                      Enums                        ##
#######################################################

import enum

class StepStatus(enum.Enum):
    unknown = 0
    succeed = 1
    failed = 2

class MoveDirection(enum.Enum):
    backLeft = 0
    left = 1
    frontLeft = 2
    front = 3
    frontRight = 4
    right = 5
    backRight = 6
    back = 7
    stop = 8


class Quadrant(enum.Enum):
    topRight = 0
    topLeft = 1
    botLeft = 2
    botRight = 3


class BattleMode(enum.IntEnum):
    scrap = 0
    wire = 1
    battery = 2
    # patrol = 3
    raven = 3

#
# Step - Type of actions that can be performed.
# 
class Action(enum.Enum):
    textDetect = enum.auto()
    colorDetect = enum.auto()
    textInput = enum.auto()
    mouseClick = enum.auto()
    keyDown = enum.auto()
    keyUp = enum.auto()
    wait = enum.auto()


#######################################################
##                      tuples                       ##
#######################################################

#
# Point - coordinate data
# x: horizontal
# y: vertical
#
class Point(tuple):
    def __new__(self, x, y):
        Point.x = property(operator.itemgetter(0))
        Point.y = property(operator.itemgetter(1))
        return tuple.__new__(Point, (x, y))

#
# Area - coordinate data of an area
# x: horizontal start
# y: vertical start
# xs: horizontal end
# ys: vertical end
#
class Area(tuple):
    def __new__(self, x, y, xs, ys):
        Area.x = property(operator.itemgetter(0))
        Area.y = property(operator.itemgetter(1))
        Area.xs = property(operator.itemgetter(2))
        Area.ys = property(operator.itemgetter(3))
        return tuple.__new__(Area, (x, y, xs, ys))

#
# Step - Each step is meant to be 1 action to perform, with details.
# id: identifier of this step.
# area: used for text detection, color detection.
# point: used for mouse click.
# strings: used for text detection, text input, keyDown, keyUp. 
#   for text input, if strings array has more than 1 element, it will fill a random one.
#   for keyDown keyUp, strings array should be array of char as string. It will apply keyboard status to all in array.
# waitBeforeAction: Wait timer before an action is executed.
#
class Step(tuple):
    def __new__(self, id: str, action: Action, area: Area, point: Point, strings: [str],  waitBefore: int, waitAfter: int):
        Step.id = property(operator.itemgetter(0))
        Step.action = property(operator.itemgetter(1))
        Step.area = property(operator.itemgetter(2))
        Step.point = property(operator.itemgetter(3))
        Step.strings = property(operator.itemgetter(4))
        Step.waitBefore = property(operator.itemgetter(5))
        Step.waitAfter = property(operator.itemgetter(6))
        return tuple.__new__(Step, (id, action, area, point, strings, waitBefore, waitAfter))

#
# All the steps that's possible in game
#
Steps = [

    Step(
        id = "login_button_label",
        action = Action.textDetect,
        area = Area(229, 512, 290, 538), 
        point = None,
        strings = ["login", "log in", "log ln", "logln"],
        waitBefore = 5,
        waitAfter = 1
    ),    
    Step(
        id = "login_btn_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(251,520),
        strings = None,
        waitBefore = 1,
        waitAfter = 1 # it will click the steam one after, so delay will be there.
    ),
    Step(
        id = "login_button_steam_label",
        action = Action.textDetect,
        area = Area(229, 464, 290, 490), 
        point = None,
        strings = ["login", "log in", "log ln", "logln"],
        waitBefore = 1,
        waitAfter = 1
    ),
    Step(
        id = "login_btn_steam_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(251,475),
        strings = None,
        waitBefore = 1,
        waitAfter = 20
    ),
    Step(
        id = "login_username_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(116,300),
        strings = None,
        waitBefore = 1,
        waitAfter = 0.5
    ),
    Step(
        id = "login_username_input",
        action = Action.textInput,
        area = None, 
        point = None,
        strings = None,
        waitBefore = 1,
        waitAfter = 0.5
    ),
    Step(
        id = "login_password_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(124,366),
        strings = None,
        waitBefore = 1,
        waitAfter = 0.5
    ),
    Step(
        id = "login_password_input",
        action = Action.textInput,
        area = None, 
        point = None,
        strings = None,
        waitBefore = 1,
        waitAfter = 0.5
    ),
    Step(
        id = "login_disconnect_btn_text",
        action = Action.textDetect,
        area = Area(924, 573, 1014, 603), 
        point = None,
        strings = ["ok", "0k"],
        waitBefore = 1,
        waitAfter = 0.5
    ),
    Step(
        id = "login_disconnect_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(963, 589),
        strings = None,
        waitBefore = 1,
        waitAfter = 0.5
    ),
    Step(
        id = "mainmenu_battle_label",
        action = Action.textDetect,
        area = Area(883,143, 1032, 187), 
        point = None,
        strings = ["battle", "batt1e"],
        waitBefore = 0.5,
        waitAfter = 0.5
    ),
    Step(
        id = "mainmenu_select_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(950,245),
        strings = None,
        waitBefore = 0.5,
        waitAfter = 0.5,
    ),
    Step(
        id = "battle_select_scrap_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(962,237),
        strings = None,
        waitBefore = 0.5,
        waitAfter = 0.5
    ),
    Step(
        id = "battle_select_battery_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(843,240),
        strings = None,
        waitBefore = 0.5,
        waitAfter = 0.5
    ),
    Step(
        id = "battle_select_wire_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(1072,240),
        strings = None,
        waitBefore = 0.5,
        waitAfter = 0.5
    ),
    Step(
        id = "battle_select_patrol_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(962,352),
        strings = None,
        waitBefore = 0.5,
        waitAfter = 0.5
    ),
    Step(
        id = "battle_select_battle_start_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(556,759),
        strings = None,
        waitBefore = 0.5,
        waitAfter = 0.5
    ),
    Step(
        id = "battle_select_battle_patrol_start_click", # different from above, patrol has different click target.
        action = Action.mouseClick,
        area = None, 
        point = Point(556,789),
        strings = None,
        waitBefore = 0.5,
        waitAfter = 0.5
    ),
    Step(
        id = "before_game_wait", # wait for 10 sec before start to detect.
        action = Action.wait,
        area = None, 
        point = Point(10,10),
        strings = None,
        waitBefore = 10,
        waitAfter = 1
    ),
    Step(
        id = "in_game_map_name_label",
        action = Action.textDetect,
        area = Area(1420, 37, 1830, 73), 
        point = None,
        strings = list(map_mask_file_path.keys()),
        waitBefore = 1,
        waitAfter = 0.5
    ),    
    Step(
        id = "in_game_wait_for_finish",
        action = Action.wait,
        area = None, 
        point = Point(10,10),
        strings = None,
        waitBefore = 30,
        waitAfter = 0.5
    ),
    Step(
        id = "in_game_detect_chat_callout",
        action = Action.textDetect,
        area = Area(11, 968, 580, 1033), 
        point = None,
        strings = ['tensor', 'daddy', 'igor', 'mom', 'shtick', 'vortex', 'dick', 'long', 'plz'],
        waitBefore = 0.5,
        waitAfter = 0.5
    ),
    Step(
        id = "in_game_early_finish_esc_return_to_garage_label",
        action = Action.textDetect,
        area = Area(845, 621, 1076, 665), 
        point = None,
        strings = ["return to garage", "garage", "return"],
        waitBefore = 0.5,
        waitAfter = 0.5
    ),
    Step(
        id = "in_game_early_finish_esc_return_to_garage_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(950, 640),
        strings = None,
        waitBefore = 0.5,
        waitAfter = 0.5
    ),
    Step(
        id = "in_game_early_finish_confirm_return_garage_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(850, 600),
        strings = None,
        waitBefore = 0.5,
        waitAfter = 0.5
    ),
    Step(
        id = "finish_battle_close_btn_label",
        action = Action.textDetect,
        area = Area(1200, 955, 1300, 995), 
        point = None,
        strings = ["close", "c1ose"],
        waitBefore = 10,
        waitAfter = 0.5
    ),
    Step(
        id = "finish_battle_close_btn_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(1230, 970),
        strings = None,
        waitBefore = 1,
        waitAfter = 2
    ),
    Step(
        id = "mainmenu_welcome_close_btn_label",
        action = Action.textDetect,
        area = Area(1478, 981, 1558,1009), 
        point = None,
        strings = ['close'],
        waitBefore = 1,
        waitAfter = 1
    ),
    Step(
        id = "mainmenu_esc_return_btn_label",
        action = Action.textDetect,
        area = Area(910,417,1007,447), 
        point = None,
        strings = ['return'],
        waitBefore = 1,
        waitAfter = 1
    ),
    Step(
        id = "mainmenu_esc_return_btn_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(950,430),
        strings = None,
        waitBefore = 1,
        waitAfter = 1
    ),
    Step(
        id = "mainmenu_esc_titlescreen_btn_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(954,672),
        strings = None,
        waitBefore = 1,
        waitAfter = 1
    ),
    Step(
        id = "mainmenu_esc_titlescreen_confirm_btn_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(846,587),
        strings = None,
        waitBefore = 1,
        waitAfter = 10
    ),

    Step(
        id = "TEMPLATE",
        action = Action.mouseClick,
        area = None, 
        point = None,
        strings = None,
        waitBefore = 1,
        waitAfter = 1
    )
]

BattleMiniMapArea = Area( # square with 240 edge length (max around 247, circle is 175 in radius)
    1579,
    738,
    1819,
    978
)
BattleMiniMapCenter = Point(
    1699,
    858
)

BattleFullMap = Area( # square of in game map
    585,
    141,
    1337,
    893
)

def findStepById(id: str):
    global Steps
    for step in Steps:
        if step.id == id:
            return step
    print("can't find step with id: " + id)
    return None

from SettingsClass import getGlobalSetting
import random


username = None
password = None
playModes = []
def loadNewUser():
    global username
    global password
    global playModes
    newAccount = random.choice(getGlobalSetting().settings.accounts)
    username = newAccount.username
    password = newAccount.password
    playModes = []
    if newAccount.playBattery:
        playModes.append('battle_select_battery_click')
    if newAccount.playScrap:
        playModes.append('battle_select_scrap_click')
    if newAccount.playWire:
        playModes.append('battle_select_wire_click')
    if newAccount.playPatrol:
        playModes.append('battle_select_patrol_click')        
    print("Account now switched to " + username + ", modes are: " + "".join(playModes))
    return True

def getUsername():
    global username
    if username:
        return username
    else:
        loadNewUser()
        return username

def getPassword():
    global password
    if password:
        return password
    else:
        loadNewUser()
        return password

def getPlayMode():
    global playModes
    if playModes:
        return playModes
    else:
        loadNewUser()
        return playModes


currentRunningStep = None

def getRunningStepId():
    global currentRunningStep
    if currentRunningStep:
        return currentRunningStep
    else:
        if getGlobalSetting().settings.startScreen is not None:
            currentRunningStep = Steps[getGlobalSetting().settings.startScreen].id
        else:
            currentRunningStep = "login_button_label"
        return currentRunningStep

def setRunningStepId(id: str):
    global currentRunningStep
    currentRunningStep = id


isDev = False
def isDevEnvironment():
    global isDev
    return isDev

def setDevEnv():
    global isDev
    isDev = True
    return isDev



class PointData(tuple):
    def __new__(self, pos: Point, isOutside: bool):
        PointData.pos = property(operator.itemgetter(0))
        PointData.isOutside = property(operator.itemgetter(1))
        return tuple.__new__(PointData, (pos, isOutside))


class CenterData(tuple):
    def __new__(self, low: PointData, mid: PointData, far: PointData):
        CenterData.low = property(operator.itemgetter(0))
        CenterData.mid = property(operator.itemgetter(1))
        CenterData.far = property(operator.itemgetter(2))
        return tuple.__new__(CenterData, (low, mid, far))

class VehicleMovementData(tuple):
    def __new__(self, time: float, pos: Point, rad: float):
        VehicleMovementData.time = property(operator.itemgetter(0))
        VehicleMovementData.pos = property(operator.itemgetter(1))
        VehicleMovementData.rad = property(operator.itemgetter(2))
        return tuple.__new__(VehicleMovementData, (time, pos, rad))

vehicleMovementStack: [VehicleMovementData] = []
def getVehicleMovementStack():
    global vehicleMovementStack
    return vehicleMovementStack

def updateVehicleMovementStack(newData: VehicleMovementData):
    global vehicleMovementStack
    vehicleMovementStack.insert(0, newData)
    if len(vehicleMovementStack) > 30:
        vehicleMovementStack.pop()

def clearVehicleMovementStack():
    global vehicleMovementStack
    vehicleMovementStack = []
    return True



#######################################################
##                      Constants                    ##
#######################################################

screenWidth = 1920
screenHeight = 1080
