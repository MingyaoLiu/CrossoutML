import operator


#######################################################
##                      Dicts                        ##
#######################################################


map_mask_file_path = {
    # "engineer garage": "./assets/maps_masks/garage_map_1_mask.png",
    "engineer garage": "./assets/maps_masks/garage_map_2_mask.png",
    "naukograd": "./assets/maps_masks/naukugrad_mask.png",
    "sandy gulf": "./assets/maps_masks/sandy_gulf_mask.png",
    "sector ex": "./assets/maps_masks/sector_ex_mask.png",
    "rock city": "./assets/maps_masks/rock_city_mask.png",
    "founders canyon": "./assets/maps_masks/founders_canyon_mask.png",
    "factory": "./assets/maps_masks/factory_mask.png",
    "bridge": "./assets/maps_masks/bridge_mask.png",
    "powerplant": "./assets/maps_masks/powerplant_mask.png",
    "old town": "./assets/maps_masks/default_test.png",
    "broken arrow": "./assets/maps_masks/broken_arrow_mask.png",
    "fortress": "./assets/maps_masks/fortress_mask.png",
    "“control-17” station": "./assets/maps_masks/control-17_station_mask.png",
    "ship graveyard": "./assets/maps_masks/ship_graveyard_mask.png",
    "desert valley": "./assets/maps_masks/desert_valley_mask.png",
    "nameless tower": "./assets/maps_masks/nameless tower_mask.png",
    "chemical plant": "./assets/maps_masks/chemical_plant_mask.png",
    "crater": "./assets/maps_masks/crater_mask.png",
    "clean island": "./assets/maps_masks/garage_map_2_mask.png",
    "ravagers foothold": "./assets/maps_masks/garage_map_2_mask.png",
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
        id = "login_button",
        action = Action.textDetect,
        area = Area(229, 464, 290, 490), 
        point = None,
        strings = ["login", "log in", "log ln", "logln"],
        waitBefore = 5,
        waitAfter = 2
    ),
    Step(
        id = "login_username_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(116,300),
        strings = None,
        waitBefore = 1,
        waitAfter = 1
    ),
    Step(
        id = "login_username_input",
        action = Action.textInput,
        area = None, 
        point = None,
        strings = None,
        waitBefore = 1,
        waitAfter = 1
    ),
    Step(
        id = "login_password_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(124,366),
        strings = None,
        waitBefore = 1,
        waitAfter = 1
    ),
    Step(
        id = "login_password_input",
        action = Action.textInput,
        area = None, 
        point = None,
        strings = None,
        waitBefore = 1,
        waitAfter = 1
    ),
    Step(
        id = "login_btn_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(251,475),
        strings = None,
        waitBefore = 1,
        waitAfter = 20
    ),
    Step(
        id = "login_disconnect_btn_text",
        action = Action.textDetect,
        area = Area(924, 573, 1014, 603), 
        point = None,
        strings = ["ok", "0k"],
        waitBefore = 1,
        waitAfter = 1
    ),
    Step(
        id = "login_disconnect_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(963, 589),
        strings = None,
        waitBefore = 1,
        waitAfter = 1
    ),
    Step(
        id = "in_game_map_name_label",
        action = Action.textDetect,
        area = Area(1440, 37, 1830, 73), 
        point = None,
        strings = list(map_mask_file_path.keys()),
        waitBefore = 1,
        waitAfter = 1
    ),    
    Step(
        id = "in_game_wait_for_finish",
        action = Action.mouseClick,
        area = None, 
        point = Point(10,10),
        strings = None,
        waitBefore = 30,
        waitAfter = 1
    ),
    Step(
        id = "finish_battle_close_btn_label",
        action = Action.textDetect,
        area = Area(1180, 955, 1310, 1025), 
        point = None,
        strings = ["close", "c1ose"],
        waitBefore = 1,
        waitAfter = 1
    ),
    Step(
        id = "finish_battle_close_btn_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(1230, 1000),
        strings = None,
        waitBefore = 1,
        waitAfter = 1
    ),
    Step(
        id = "mainmenu_battle_label",
        action = Action.textDetect,
        area = Area(883,143, 1032, 187), 
        point = None,
        strings = ["battle", "batt1e"],
        waitBefore = 1,
        waitAfter = 1
    ),
    Step(
        id = "mainmenu_select_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(950,245),
        strings = None,
        waitBefore = 1,
        waitAfter = 1
    ),
    Step(
        id = "battle_select_scrap_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(962,237),
        strings = None,
        waitBefore = 1,
        waitAfter = 1
    ),
    Step(
        id = "battle_select_battery_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(843,240),
        strings = None,
        waitBefore = 1,
        waitAfter = 1
    ),
    Step(
        id = "battle_select_wire_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(1072,240),
        strings = None,
        waitBefore = 1,
        waitAfter = 1
    ),
    Step(
        id = "battle_select_battle_start_click",
        action = Action.mouseClick,
        area = None, 
        point = Point(556,759),
        strings = None,
        waitBefore = 1,
        waitAfter = 1
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
        id = "before_game_wait",
        action = Action.mouseClick,
        area = None, 
        point = Point(10,10),
        strings = None,
        waitBefore = 10,
        waitAfter = 1
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
def loadNewUser():
    global username
    global password
    newAccount = random.choice(getGlobalSetting().settings.accounts)
    username = newAccount.username
    password = newAccount.password
    print("Account now switched to " + username)
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


currentRunningStep = None

def getRunningStepId():
    global currentRunningStep
    if currentRunningStep:
        return currentRunningStep
    else:
        if getGlobalSetting().settings.startScreen is not None:
            currentRunningStep = Steps[getGlobalSetting().settings.startScreen].id
        else:
            currentRunningStep = "login_disconnect_btn_text"
        return currentRunningStep

def setRunningStepId(id: str):
    global currentRunningStep
    currentRunningStep = id




class DetectClickPair(tuple):
    def __new__(self, name: str, area: Area, requiredMatch: bool, clickPos: Point, willClick: bool, expectedStrs: [str],  waitBeforeDetect: int,  waitBeforeClick: int):
        DetectClickPair.name = property(operator.itemgetter(0))
        DetectClickPair.area = property(operator.itemgetter(1))
        DetectClickPair.requiredMatch = property(operator.itemgetter(2))
        DetectClickPair.clickPos = property(operator.itemgetter(3))
        DetectClickPair.willClick = property(operator.itemgetter(4))
        DetectClickPair.expectedStrs = property(operator.itemgetter(5))
        DetectClickPair.waitBeforeDetect = property(operator.itemgetter(6))
        DetectClickPair.waitBeforeClick = property(operator.itemgetter(7))
        return tuple.__new__(DetectClickPair, (name, area, requiredMatch, clickPos, willClick, expectedStrs, waitBeforeDetect, waitBeforeClick))
 

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


class BattleFrame(tuple):
    def __new__(self, record: bool, time: float, distance: float, speed: float, posData: PointData, centerRad: float, center: CenterData, left: PointData, right: PointData):
        BattleFrame.record = property(operator.itemgetter(0))
        BattleFrame.time = property(operator.itemgetter(1))
        BattleFrame.distance = property(operator.itemgetter(2))
        BattleFrame.speed = property(operator.itemgetter(3))
        BattleFrame.posData = property(operator.itemgetter(4))
        BattleFrame.centerRad = property(operator.itemgetter(5))
        BattleFrame.center = property(operator.itemgetter(6))
        BattleFrame.left = property(operator.itemgetter(7))
        BattleFrame.right = property(operator.itemgetter(8))
        return tuple.__new__(BattleFrame, (record, time, distance, speed, posData, centerRad, center, left, right))

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

scrap_btn_width = 40
scrap_btn_height = 40
scrap_btn_trigger_pos_x = int(screenWidth / 2)
scrap_btn_trigger_pos_y = int(270)

wire_btn_width = 30
wire_btn_height = 30
wire_btn_trigger_pos_x = int(screenWidth / 2 + 110)
wire_btn_trigger_pos_y = int(270)

battery_btn_width = 30
battery_btn_height = 30
battery_btn_trigger_pos_x = int(screenWidth / 2 - 110)
battery_btn_trigger_pos_y = int(270)

patrol_btn_width = 30
patrol_btn_height = 30
patrol_btn_trigger_pos_x = int(screenWidth / 2)
patrol_btn_trigger_pos_y = int(390)

raven_path_btn_width = 30
raven_path_btn_height = 30
raven_path_btn_trigger_pos_x = int(
    screenWidth / 2 + 220)
raven_path_btn_trigger_pos_y = int(270)

esc_return_button_width = 90
esc_return_button_width_start = int(
    screenWidth / 2 - esc_return_button_width / 2)
esc_return_button_width_end = int(
    screenWidth / 2 + esc_return_button_width / 2)
esc_return_button_height = 26
esc_return_button_height_start = int(
    screenHeight / 2.27 - esc_return_button_height / 2)
esc_return_button_height_end = int(
    screenHeight / 2.27 + esc_return_button_height / 2)
esc_return_button_trigger_pos_x = int(
    esc_return_button_width_start + esc_return_button_width / 2)
esc_return_button_trigger_pos_y = int(
    esc_return_button_height_start + esc_return_button_height / 2)


login_label_width = 70
login_label_width_start = int(screenWidth / 7.5 - login_label_width / 2)
login_label_width_end = int(screenWidth / 7.5 + login_label_width / 2)
login_label_height = 40
login_label_height_start = int(screenHeight / 2 - login_label_height / 2)
login_label_height_end = int(screenHeight / 2 + login_label_height / 2)
login_label_trigger_pos_x = int(
    login_label_width_start + login_label_width / 2)
login_label_trigger_pos_y = int(
    login_label_height_start + login_label_height / 2)


login_exit_no_width = 35
login_exit_no_width_start = int(screenWidth / 1.785 - login_exit_no_width / 2)
login_exit_no_width_end = int(screenWidth / 1.785 + login_exit_no_width / 2)
login_exit_no_height = 25
login_exit_no_height_start = int(
    screenHeight / 1.75 - login_exit_no_height / 2)
login_exit_no_height_end = int(screenHeight / 1.75 + login_exit_no_height / 2)
login_exit_no_trigger_pos_x = int(
    login_exit_no_width_start + login_exit_no_width / 2)
login_exit_no_trigger_pos_y = int(
    login_exit_no_height_start + login_exit_no_height / 2)


welcome_promo_label_width = 70
welcome_promo_label_width_start = int(
    screenWidth / 1.5 - welcome_promo_label_width / 2)
welcome_promo_label_width_end = int(
    screenWidth / 1.5 + welcome_promo_label_width / 2)
welcome_promo_label_height = 40
welcome_promo_label_height_start = int(
    screenHeight / 1.5 - welcome_promo_label_height / 2)
welcome_promo_label_height_end = int(
    screenHeight / 1.5 + welcome_promo_label_height / 2)
welcome_promo_label_trigger_pos_x = int(
    welcome_promo_label_width_start + welcome_promo_label_width / 2)
welcome_promo_label_trigger_pos_y = int(
    welcome_promo_label_height_start + welcome_promo_label_height / 2)

mainmenu_battle_label_width = 140
mainmenu_battle_label_width_start = int(
    screenWidth / 2 - mainmenu_battle_label_width / 2)
mainmenu_battle_label_width_end = int(
    screenWidth / 2 + mainmenu_battle_label_width / 2)
mainmenu_battle_label_height = 50
mainmenu_battle_label_height_start = int(
    screenHeight / 5.65 - mainmenu_battle_label_height / 2)
mainmenu_battle_label_height_end = int(
    screenHeight / 5.65 + mainmenu_battle_label_height / 2)
mainmenu_battle_label_trigger_pos_x = int(
    mainmenu_battle_label_width_start + mainmenu_battle_label_width / 2)
mainmenu_battle_label_trigger_pos_y = int(
    mainmenu_battle_label_height_start + mainmenu_battle_label_height / 2)

mainmenu_select_mode_label_width = 130
mainmenu_select_mode_label_width_start = int(
    screenWidth / 2 - mainmenu_select_mode_label_width / 2)
mainmenu_select_mode_label_width_end = int(
    screenWidth / 2 + mainmenu_select_mode_label_width / 2)
mainmenu_select_mode_label_height = 60
mainmenu_select_mode_label_height_start = int(
    screenHeight / 4 - mainmenu_select_mode_label_height / 2)
mainmenu_select_mode_label_height_end = int(
    screenHeight / 4 + mainmenu_select_mode_label_height / 2)
mainmenu_select_mode_label_trigger_pos_x = int(
    mainmenu_select_mode_label_width_start + mainmenu_select_mode_label_width / 2)
mainmenu_select_mode_label_trigger_pos_y = int(
    mainmenu_select_mode_label_height_start + mainmenu_select_mode_label_height / 2)

get_resource_battle_label_width = 130
get_resource_battle_label_width_start = int(
    screenWidth / 3 - get_resource_battle_label_width / 2)
get_resource_battle_label_width_end = int(
    screenWidth / 3 + get_resource_battle_label_width / 2)
get_resource_battle_label_height = 60
get_resource_battle_label_height_start = int(
    screenHeight / 1.37 - get_resource_battle_label_height / 2)
get_resource_battle_label_height_end = int(
    screenHeight / 1.37 + get_resource_battle_label_height / 2)
get_resource_battle_label_trigger_pos_x = int(
    get_resource_battle_label_width_start + get_resource_battle_label_width / 2)
get_resource_battle_label_trigger_pos_y = int(
    get_resource_battle_label_height_start + get_resource_battle_label_height / 2)

get_resource_patrol_battle_label_height_start = int(
    screenHeight / 1.3 - get_resource_battle_label_height / 2)
get_resource_patrol_battle_label_height_end = int(
    screenHeight / 1.3 + get_resource_battle_label_height / 2)
get_resource_patrol_battle_label_trigger_pos_x = int(
    get_resource_battle_label_width_start + get_resource_battle_label_width / 2)
get_resource_patrol_battle_label_trigger_pos_y = int(
    get_resource_patrol_battle_label_height_start + get_resource_battle_label_height / 2)

battle_type_title_label_width = 250
battle_type_title_label_width_start = int(
    screenWidth / 12 + 10 - battle_type_title_label_width / 2)
battle_type_title_label_width_end = int(
    screenWidth / 12 + 10 + battle_type_title_label_width / 2)
battle_type_title_label_height = 65
battle_type_title_label_height_start = int(
    screenHeight / 13.5 - battle_type_title_label_height / 2)
battle_type_title_label_height_end = int(
    screenHeight / 13.5 + battle_type_title_label_height / 2)
battle_type_title_label_trigger_pos_x = int(
    battle_type_title_label_width_start + battle_type_title_label_width / 2)
battle_type_title_label_trigger_pos_y = int(
    battle_type_title_label_height_start + battle_type_title_label_height / 2)

battle_map_name_label_width = 360
battle_map_name_label_width_start = int(
    screenWidth - 275 - battle_map_name_label_width / 2)
battle_map_name_label_width_end = int(
    screenWidth - 275 + battle_map_name_label_width / 2)
battle_map_name_label_height = 54
battle_map_name_label_height_start = int(82 - battle_map_name_label_height / 2)
battle_map_name_label_height_end = int(82 + battle_map_name_label_height / 2)
battle_map_name_label_trigger_pos_x = int(
    battle_map_name_label_width_start + battle_map_name_label_width / 2)
battle_map_name_label_trigger_pos_y = int(
    battle_map_name_label_height_start + battle_map_name_label_height / 2)

battle_victory_defeat_giant_width = 550
battle_victory_defeat_giant_width_start = int(
    screenWidth / 2 - battle_victory_defeat_giant_width / 2)
battle_victory_defeat_giant_width_end = int(
    screenWidth / 2 + battle_victory_defeat_giant_width / 2)
battle_victory_defeat_giant_width_height = 150
battle_victory_defeat_giant_width_height_start = int(
    screenHeight / 2.1 - battle_victory_defeat_giant_width_height / 2)
battle_victory_defeat_giant_width_height_end = int(
    screenHeight / 2.1 + battle_victory_defeat_giant_width_height / 2)
battle_victory_defeat_giant_width_trigger_pos_x = int(
    battle_victory_defeat_giant_width_start + battle_victory_defeat_giant_width / 2)
battle_victory_defeat_giant_width_trigger_pos_y = int(
    battle_victory_defeat_giant_width_height_start + battle_victory_defeat_giant_width_height / 2)


battle_lose_wait_width = 32
battle_lose_wait_width_start = int(
    screenWidth / 2 - 112 - battle_lose_wait_width / 2)
battle_lose_wait_width_end = int(
    screenWidth / 2 - 112 + battle_lose_wait_width / 2)
battle_lose_wait_height = 32
battle_lose_wait_height_start = int(
    screenHeight / 1.33 - battle_lose_wait_height / 2)
battle_lose_wait_height_end = int(
    screenHeight / 1.33 + battle_lose_wait_height / 2)
battle_lose_wait_trigger_pos_x = int(
    battle_lose_wait_width_start + battle_lose_wait_width / 2)
battle_lose_wait_trigger_pos_y = int(
    battle_lose_wait_height_start + battle_lose_wait_height / 2)

battle_lose_survivor_part_width = 240
battle_lose_survivor_part_width_start = int(
    screenWidth - battle_lose_survivor_part_width)
battle_lose_survivor_part_width_end = int(screenWidth)
battle_lose_survivor_part_height = 50
battle_lose_survivor_part_height_start = int(
    screenHeight / 2.4 - battle_lose_survivor_part_height / 2)
battle_lose_survivor_part_height_end = int(
    screenHeight / 2.4 + battle_lose_survivor_part_height / 2)
battle_lose_survivor_part_trigger_pos_x = int(
    battle_lose_survivor_part_width_start + battle_lose_survivor_part_width / 2)
battle_lose_survivor_part_trigger_pos_y = int(
    battle_lose_survivor_part_height_start + battle_lose_survivor_part_height / 2)


finish_battle_close_label_width = 120
finish_battle_close_label_width_start = int(
    screenWidth / 5 * 3.25 - finish_battle_close_label_width / 2) # 1188
finish_battle_close_label_width_end = int(
    screenWidth / 5 * 3.25 + finish_battle_close_label_width / 2) # 1308
finish_battle_close_label_height = 50
finish_battle_close_label_height_start = int(
    screenHeight / 13 * 12.1 - finish_battle_close_label_height / 2) # 955
finish_battle_close_label_height_end = int(
    screenHeight / 13 * 12.1 + finish_battle_close_label_height / 2) # 1055
finish_battle_close_label_trigger_pos_x = int(
    finish_battle_close_label_width_start + finish_battle_close_label_width / 2)
finish_battle_close_label_trigger_pos_y = int(
    finish_battle_close_label_height_start + finish_battle_close_label_height / 2)

finish_battle_battle_label_width = 140
finish_battle_battle_label_width_start = int(
    screenWidth / 5 * 4.1 - finish_battle_battle_label_width / 2)
finish_battle_battle_label_width_end = int(
    screenWidth / 5 * 4.1 + finish_battle_battle_label_width / 2)
finish_battle_battle_label_height = 50
finish_battle_battle_label_height_start = int(
    screenHeight / 13 * 12.1 - finish_battle_battle_label_height / 2)
finish_battle_battle_label_height_end = int(
    screenHeight / 13 * 12.1 + finish_battle_battle_label_height / 2)
finish_battle_battle_label_trigger_pos_x = int(
    finish_battle_battle_label_width_start + finish_battle_battle_label_width / 2)
finish_battle_battle_label_trigger_pos_y = int(
    finish_battle_battle_label_height_start + finish_battle_battle_label_height / 2)


mainmenu_challenge_complete_ok_width = 60
mainmenu_challenge_complete_ok_width_start = int(
    screenWidth / 2 + 110 - mainmenu_challenge_complete_ok_width / 2)
mainmenu_challenge_complete_ok_width_end = int(
    screenWidth / 2 + 110 + mainmenu_challenge_complete_ok_width / 2)
mainmenu_challenge_complete_ok_height = 40
mainmenu_challenge_complete_ok_height_start = int(
    screenHeight / 1.08 - mainmenu_challenge_complete_ok_height / 2)
mainmenu_challenge_complete_ok_height_end = int(
    screenHeight / 1.08 + mainmenu_challenge_complete_ok_height / 2)
mainmenu_challenge_complete_ok_trigger_pos_x = int(
    mainmenu_challenge_complete_ok_width_start + mainmenu_challenge_complete_ok_width / 2)
mainmenu_challenge_complete_ok_trigger_pos_y = int(
    mainmenu_challenge_complete_ok_height_start + mainmenu_challenge_complete_ok_height / 2)


in_battle_front_view_width = 720
in_battle_front_view_width_start = int(
    screenWidth / 2 - in_battle_front_view_width / 2)
in_battle_front_view_width_end = int(
    screenWidth / 2 + in_battle_front_view_width / 2)
in_battle_front_view_height = 260
in_battle_front_view_height_start = int(
    screenHeight / 2.2 - in_battle_front_view_height / 2)
in_battle_front_view_height_end = int(
    screenHeight / 2.2 + in_battle_front_view_height / 2)
in_battle_front_view_trigger_pos_x = int(
    in_battle_front_view_width_start + in_battle_front_view_width / 2)
in_battle_front_view_trigger_pos_y = int(
    in_battle_front_view_height_start + in_battle_front_view_height / 2)


in_battle_health_digit_width = 48
in_battle_health_digit_width_start = int(
    screenWidth / 2 - 59 - in_battle_health_digit_width / 2)
in_battle_health_digit_width_end = int(
    screenWidth / 2 - 59 + in_battle_health_digit_width / 2)
in_battle_health_digit_height = 24
in_battle_health_digit_height_start = int(
    screenHeight - 29 - in_battle_health_digit_height / 2)
in_battle_health_digit_height_end = int(
    screenHeight - 29 + in_battle_health_digit_height / 2)
in_battle_health_digit_trigger_pos_x = int(
    in_battle_health_digit_width_start + in_battle_health_digit_width / 2)
in_battle_health_digit_trigger_pos_y = int(
    in_battle_health_digit_height_start + in_battle_health_digit_height / 2)


in_battle_mini_map_width = 150
in_battle_mini_map_width_start = int(
    screenWidth - 209 - in_battle_mini_map_width / 2)
in_battle_mini_map_width_end = int(
    screenWidth - 209 + in_battle_mini_map_width / 2)
in_battle_mini_map_height = 150
in_battle_mini_map_height_start = int(
    screenHeight - 176 - in_battle_mini_map_height / 2)
in_battle_mini_map_height_end = int(
    screenHeight - 176 + in_battle_mini_map_height / 2)
in_battle_mini_map_trigger_pos_x = int(
    in_battle_mini_map_width_start + in_battle_mini_map_width / 2)
in_battle_mini_map_trigger_pos_y = int(
    in_battle_mini_map_height_start + in_battle_mini_map_height / 2)


in_battle_mini_map_arrow_width = 30
in_battle_mini_map_arrow_width_start = int(
    screenWidth - 209 - in_battle_mini_map_arrow_width / 2)
in_battle_mini_map_arrow_width_end = int(
    screenWidth - 209 + in_battle_mini_map_arrow_width / 2)
in_battle_mini_map_arrow_height = 30
in_battle_mini_map_arrow_height_start = int(
    screenHeight - 176 - in_battle_mini_map_arrow_height / 2)
in_battle_mini_map_arrow_height_end = int(
    screenHeight - 176 + in_battle_mini_map_arrow_height / 2)
in_battle_mini_map_arrow_trigger_pos_x = int(
    in_battle_mini_map_arrow_width_start + in_battle_mini_map_arrow_width / 2)
in_battle_mini_map_arrow_trigger_pos_y = int(
    in_battle_mini_map_arrow_height_start + in_battle_mini_map_arrow_height / 2)


co_pilot_upgrade_close_width = 54
co_pilot_upgrade_close_width_start = int(
    screenWidth / 2 + 8 - co_pilot_upgrade_close_width / 2)
co_pilot_upgrade_close_width_end = int(
    screenWidth / 2 + 8 + co_pilot_upgrade_close_width / 2)
co_pilot_upgrade_close_height = 22
co_pilot_upgrade_close_height_start = int(
    screenHeight / 1.527 - co_pilot_upgrade_close_height / 2)
co_pilot_upgrade_close_height_end = int(
    screenHeight / 1.527 + co_pilot_upgrade_close_height / 2)
co_pilot_upgrade_close_trigger_pos_x = int(
    co_pilot_upgrade_close_width_start + co_pilot_upgrade_close_width / 2)
co_pilot_upgrade_close_trigger_pos_y = int(
    co_pilot_upgrade_close_height_start + co_pilot_upgrade_close_height / 2)



frame_crops = {
    "login_exit_no_btn":
    DetectClickPair(
        "Exit No Button",
        Area(login_exit_no_width_start, login_exit_no_height_start,
                 login_exit_no_width_end, login_exit_no_height_end),
        True,
        Point(login_exit_no_trigger_pos_x,
              login_exit_no_trigger_pos_y),
        True,
        ["no"],
        2,
        2
    ),
    "mainmenu_escape_menu_return_button":
    DetectClickPair(
        "Escape Return Button",
        Area(esc_return_button_width_start, esc_return_button_height_start,
                 esc_return_button_width_end, esc_return_button_height_end),
        True,
        Point(esc_return_button_trigger_pos_x,
              esc_return_button_trigger_pos_y),
        True,
        ["return", "toate"],
        1,
        1
    ),
}


login_crops = [
    DetectClickPair(
        "Exit No Button",
        Area(login_exit_no_width_start, login_exit_no_height_start,
                 login_exit_no_width_end, login_exit_no_height_end),
        True,
        Point(login_exit_no_trigger_pos_x,
              login_exit_no_trigger_pos_y),
        True,
        ["no"],
        1,
        1
    ),
    DetectClickPair(
        "Escape Return Button",
        Area(esc_return_button_width_start, esc_return_button_height_start,
                 esc_return_button_width_end, esc_return_button_height_end),
        True,
        Point(esc_return_button_trigger_pos_x,
              esc_return_button_trigger_pos_y),
        True,
        ["return", "toate"],
        1,
        1
    ),

    DetectClickPair(
        "Login Button",
        Area(login_label_width_start, login_label_height_start,
                 login_label_width_end, login_label_height_end),
        True,
        Point(login_label_trigger_pos_x,
              login_label_trigger_pos_y),
        True,
        ["login", "log in", "log ln", "logln"],
        10,
        1
    )
]

welcome_crops = [
    DetectClickPair(
        "Welcome Promo Close Button",
        Area(welcome_promo_label_width_start, welcome_promo_label_height_start,
                 welcome_promo_label_width_end, welcome_promo_label_height_end),
        True,
        Point(welcome_promo_label_trigger_pos_x,
              welcome_promo_label_trigger_pos_y),
        True,
        ["close", "c1ose", "ciose"],
        2,
        1
    )
]

mainmenu_master_jack_crops = [
    DetectClickPair(
        "Mainmenu MasterJack Upgrade level Close",
        Area(co_pilot_upgrade_close_width_start, co_pilot_upgrade_close_height_start,
                 co_pilot_upgrade_close_width_end, co_pilot_upgrade_close_height_end),
        True,
        Point(co_pilot_upgrade_close_trigger_pos_x,
              co_pilot_upgrade_close_trigger_pos_x),
        True,
        ["close", "c1ose"],
        2,
        1
    )
]

mainmenu_challenge_crops = [
    DetectClickPair(
        "Mainmenu Challenge Complete OK Button",
        Area(mainmenu_challenge_complete_ok_width_start, mainmenu_challenge_complete_ok_height_start,
                 mainmenu_challenge_complete_ok_width_end, mainmenu_challenge_complete_ok_height_end),
        True,
        Point(mainmenu_challenge_complete_ok_trigger_pos_x,
              mainmenu_challenge_complete_ok_trigger_pos_y),
        True,
        ["ok", "0k"],
        2,
        1
    )
]

mainmenu_crops = [
    DetectClickPair(
        "Main Menu Battle Button",
        Area(mainmenu_battle_label_width_start, mainmenu_battle_label_height_start,
                 mainmenu_battle_label_width_end, mainmenu_battle_label_height_end),
        False,
        Point(mainmenu_battle_label_trigger_pos_x,
              mainmenu_battle_label_trigger_pos_y),
        False,
        ["battle", "batt1e"],
        1,
        1
    ),
    DetectClickPair(
        "Main Menu Select Mode Button",
        Area(mainmenu_select_mode_label_width_start, mainmenu_select_mode_label_height_start,
                 mainmenu_select_mode_label_width_end, mainmenu_select_mode_label_height_end),
        True,
        Point(mainmenu_select_mode_label_trigger_pos_x,
              mainmenu_select_mode_label_trigger_pos_y),
        True,
        ["select mode", "selectmode", "se1ect mode"],
        1,
        1
    ),
    DetectClickPair(
        "Escape Exit Button",
        Area(883, 658, 1029, 697),
        True,
        Point(955, 675),
        True,
        ["title screen", "titlescreen", "tit1e screen"],
        1,
        1
    ),
    DetectClickPair(
        "Exit to login yes button",
        Area(820, 610, 880, 626),
        True,
        Point(850, 620),
        True,
        ["yes", "ais"],
        5,
        1
    )
]

resource_prepare_crops = [
    DetectClickPair(
        "Scrap/Wire/Battery Prepare to Battle Button",
        Area(get_resource_battle_label_width_start, get_resource_battle_label_height_start,
                 get_resource_battle_label_width_end, get_resource_battle_label_height_end),
        True,
        Point(get_resource_battle_label_trigger_pos_x,
              get_resource_battle_label_trigger_pos_y),
        True,
        ["battle", "batt1e"],
        1,
        1
    ),
    DetectClickPair(
        "Patrol Mode Prepare to Battle Button",
        Area(get_resource_battle_label_width_start, get_resource_patrol_battle_label_height_start,
                 get_resource_battle_label_width_end, get_resource_patrol_battle_label_height_end),
        False,
        Point(get_resource_patrol_battle_label_trigger_pos_x,
              get_resource_patrol_battle_label_trigger_pos_y),
        False,
        ["battle", "batt1e"],
        1,
        1
    )
]

battle_preparation_crops = [
    DetectClickPair(
        "Prepare to Battle Summary Screen Title",
        Area(battle_type_title_label_width_start, battle_type_title_label_height_start,
                 battle_type_title_label_width_end, battle_type_title_label_height_end),
        True,
        Point(mainmenu_challenge_complete_ok_trigger_pos_x,
              mainmenu_challenge_complete_ok_trigger_pos_y),
        True,
        ["assault", "encounter", "domination"],
        1,
        1
    ),
    DetectClickPair(
        "Prepare to Battle Summary Screen Map Name",
        Area(battle_map_name_label_width_start, battle_map_name_label_height_start,
                 battle_map_name_label_width_end, battle_map_name_label_height_end),
        True,
        Point(battle_map_name_label_trigger_pos_x,
              battle_map_name_label_trigger_pos_y),
        True,
        list(map_mask_file_path.keys()),
        1,
        1
    )
]

# in_battle_crops = [
#     DetectClickPair(
#         "Defeat / Victory Screen",
#         Area(battle_lose_survivor_part_width_start,battle_lose_survivor_part_height_start,battle_lose_survivor_part_width_end,battle_lose_survivor_part_height_end),
#         False,
#         Point(battle_lose_survivor_part_trigger_pos_x,battle_lose_survivor_part_trigger_pos_y),
#         False,
#         ["survivor's parts", "survivors parts", "survivorsparts"],
#         1
#     ),
#     DetectClickPair(
#         "Survivor's Kit",
#         Area(battle_lose_survivor_part_width_start,battle_lose_survivor_part_height_start,battle_lose_survivor_part_width_end,battle_lose_survivor_part_height_end),
#         False,
#         Point(battle_lose_survivor_part_trigger_pos_x,battle_lose_survivor_part_trigger_pos_y),
#         False,
#         ["survivor's parts", "survivors parts", "survivorsparts"],
#         1
#     )
# ]

finish_battle_crops = [
    DetectClickPair(
        "Finish Battle Close Button",
        Area(finish_battle_close_label_width_start, finish_battle_close_label_height_start,
                 finish_battle_close_label_width_end, finish_battle_close_label_height_end),
        True,
        Point(finish_battle_close_label_trigger_pos_x,
              finish_battle_close_label_trigger_pos_y),
        True,
        ["close", "c1ose"],
        1,
        1
    ),
    DetectClickPair(
        "Finish Battle BATTLE Button",
        Area(finish_battle_battle_label_width_start, finish_battle_battle_label_height_start,
                 finish_battle_battle_label_width_end, finish_battle_battle_label_height_end),
        False,
        Point(finish_battle_battle_label_trigger_pos_x,
              finish_battle_battle_label_trigger_pos_y),
        False,
        ["battle", "batt1e"],
        1,
        1
    )
]
