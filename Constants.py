import operator


#######################################################
##                      Enums                        ##
#######################################################

import enum


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


class ScreenStep(enum.IntEnum):
    Login = 0
    WelcomeScreen = 1
    MasterJackUpgradeScreen = 2
    ChallengeCompleteScreen = 3
    MainMenu = 4
    SelectMode = 5
    GetResourceMenu = 6
    BattlePrepareScreen = 7
    InBattleNow = 8
    DeathWaiting = 9
    FinishBattleScreen = 10
    debug = 11

#######################################################
##                      tuples                       ##
#######################################################


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


#######################################################
##                      Dicts                        ##
#######################################################

map_mask_file_path = {
    "engineer garage": "./assets/maps_masks/garage_map_1_mask.png",
    "naukograd": "./assets/maps_masks/naukugrad_mask.png",
    "sandy gulf": "./assets/maps_masks/sandy_gulf_mask.png",
    "sector ex": "./assets/maps_masks/sector_ex_mask.png",
    "rock city": "./assets/maps_masks/rock_city_mask.png",
    "founders canyon": "./assets/maps_masks/founders_canyon_mask.png",
    "factory": "./assets/maps_masks/factory_mask.png",
    "bridge": "./assets/maps_masks/bridge_mask_2.png",
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

}


#######################################################
##                      Constants                    ##
#######################################################

screenWidth = 1920
screenHeight = 1080

topTitleBarHeight = 30


scrap_btn_width = 40
scrap_btn_height = 40
scrap_btn_trigger_pos_x = int(screenWidth / 2 - scrap_btn_width / 2)
scrap_btn_trigger_pos_y = int(screenHeight / 4 - scrap_btn_height / 2)

wire_btn_width = 30
wire_btn_height = 30
wire_btn_trigger_pos_x = int(screenWidth / 2 + 100 - wire_btn_width / 2)
wire_btn_trigger_pos_y = int(screenHeight / 4 - wire_btn_height / 2)

battery_btn_width = 30
battery_btn_height = 30
battery_btn_trigger_pos_x = int(screenWidth / 2 - 100 - battery_btn_width / 2)
battery_btn_trigger_pos_y = int(screenHeight / 4 - battery_btn_height / 2)

patrol_btn_width = 30
patrol_btn_height = 30
patrol_btn_trigger_pos_x = int(screenWidth / 2 - patrol_btn_width / 2)
patrol_btn_trigger_pos_y = int(screenHeight / 4 + 120 - patrol_btn_height / 2)

raven_path_btn_width = 30
raven_path_btn_height = 30
raven_path_btn_trigger_pos_x = int(
    screenWidth / 2 + 200 - raven_path_btn_width / 2)
raven_path_btn_trigger_pos_y = int(
    screenHeight / 4 - raven_path_btn_height / 2)

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

battle_map_name_label_width = 450
battle_map_name_label_width_start = int(
    screenWidth - 250 - battle_map_name_label_width / 2)
battle_map_name_label_width_end = int(
    screenWidth - 250 + battle_map_name_label_width / 2)
battle_map_name_label_height = 60
battle_map_name_label_height_start = int(
    screenHeight / 13.5 - battle_map_name_label_height / 2)
battle_map_name_label_height_end = int(
    screenHeight / 13.5 + battle_map_name_label_height / 2)
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
    screenWidth / 5 * 3.25 - finish_battle_close_label_width / 2)
finish_battle_close_label_width_end = int(
    screenWidth / 5 * 3.25 + finish_battle_close_label_width / 2)
finish_battle_close_label_height = 50
finish_battle_close_label_height_start = int(
    screenHeight / 13 * 12.1 - finish_battle_close_label_height / 2)
finish_battle_close_label_height_end = int(
    screenHeight / 13 * 12.1 + finish_battle_close_label_height / 2)
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
    screenWidth - 210 - in_battle_mini_map_width / 2)
in_battle_mini_map_width_end = int(
    screenWidth - 210 + in_battle_mini_map_width / 2)
in_battle_mini_map_height = 150
in_battle_mini_map_height_start = int(
    screenHeight - 180 - in_battle_mini_map_height / 2)
in_battle_mini_map_height_end = int(
    screenHeight - 180 + in_battle_mini_map_height / 2)
in_battle_mini_map_trigger_pos_x = int(
    in_battle_mini_map_width_start + in_battle_mini_map_width / 2)
in_battle_mini_map_trigger_pos_y = int(
    in_battle_mini_map_height_start + in_battle_mini_map_height / 2)


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

login_crops = [
    CropProperty(
        "Exit No Button",
        CropArea(login_exit_no_width_start, login_exit_no_height_start,
                 login_exit_no_width_end, login_exit_no_height_end),
        True,
        Point(login_exit_no_trigger_pos_x,
              login_exit_no_trigger_pos_y),
        True,
        ["no"],
        1
    ),
    CropProperty(
        "Escape Return Button",
        CropArea(esc_return_button_width_start, esc_return_button_height_start,
                 esc_return_button_width_end, esc_return_button_height_end),
        True,
        Point(esc_return_button_trigger_pos_x,
              esc_return_button_trigger_pos_y),
        True,
        ["return", "toate"],
        1
    ),

    CropProperty(
        "Login Button",
        CropArea(login_label_width_start, login_label_height_start,
                 login_label_width_end, login_label_height_end),
        True,
        Point(login_label_trigger_pos_x,
              login_label_trigger_pos_y),
        True,
        ["login", "log in", "log ln", "logln"],
        10
    )
]

welcome_crops = [
    CropProperty(
        "Welcome Promo Close Button",
        CropArea(welcome_promo_label_width_start, welcome_promo_label_height_start,
                 welcome_promo_label_width_end, welcome_promo_label_height_end),
        True,
        Point(welcome_promo_label_trigger_pos_x,
              welcome_promo_label_trigger_pos_y),
        True,
        ["close", "c1ose", "ciose"],
        2
    )
]

mainmenu_master_jack_crops = [
    CropProperty(
        "Mainmenu MasterJack Upgrade level Close",
        CropArea(co_pilot_upgrade_close_width_start, co_pilot_upgrade_close_height_start,
                 co_pilot_upgrade_close_width_end, co_pilot_upgrade_close_height_end),
        True,
        Point(co_pilot_upgrade_close_trigger_pos_x,
              co_pilot_upgrade_close_trigger_pos_x),
        True,
        ["close", "c1ose"],
        2
    )
]

mainmenu_challenge_crops = [
    CropProperty(
        "Mainmenu Challenge Complete OK Button",
        CropArea(mainmenu_challenge_complete_ok_width_start, mainmenu_challenge_complete_ok_height_start,
                 mainmenu_challenge_complete_ok_width_end, mainmenu_challenge_complete_ok_height_end),
        True,
        Point(mainmenu_challenge_complete_ok_trigger_pos_x,
              mainmenu_challenge_complete_ok_trigger_pos_y),
        True,
        ["ok", "0k"],
        2
    )
]

mainmenu_crops = [
    CropProperty(
        "Main Menu Battle Button",
        CropArea(mainmenu_battle_label_width_start, mainmenu_battle_label_height_start,
                 mainmenu_battle_label_width_end, mainmenu_battle_label_height_end),
        False,
        Point(mainmenu_battle_label_trigger_pos_x,
              mainmenu_battle_label_trigger_pos_y),
        False,
        ["battle", "batt1e"],
        1
    ),
    CropProperty(
        "Main Menu Select Mode Button",
        CropArea(mainmenu_select_mode_label_width_start, mainmenu_select_mode_label_height_start,
                 mainmenu_select_mode_label_width_end, mainmenu_select_mode_label_height_end),
        True,
        Point(mainmenu_select_mode_label_trigger_pos_x,
              mainmenu_select_mode_label_trigger_pos_y),
        True,
        ["select mode", "selectmode", "se1ect mode"],
        1
    )
]

resource_prepare_crops = [
    CropProperty(
        "Scrap/Wire/Battery Prepare to Battle Button",
        CropArea(get_resource_battle_label_width_start, get_resource_battle_label_height_start,
                 get_resource_battle_label_width_end, get_resource_battle_label_height_end),
        True,
        Point(get_resource_battle_label_trigger_pos_x,
              get_resource_battle_label_trigger_pos_y),
        True,
        ["battle", "batt1e"],
        1
    ),
    CropProperty(
        "Patrol Mode Prepare to Battle Button",
        CropArea(get_resource_battle_label_width_start, get_resource_patrol_battle_label_height_start,
                 get_resource_battle_label_width_end, get_resource_patrol_battle_label_height_end),
        False,
        Point(get_resource_patrol_battle_label_trigger_pos_x,
              get_resource_patrol_battle_label_trigger_pos_y),
        False,
        ["battle", "batt1e"],
        1
    )
]

battle_preparation_crops = [
    CropProperty(
        "Prepare to Battle Summary Screen Title",
        CropArea(battle_type_title_label_width_start, battle_type_title_label_height_start,
                 battle_type_title_label_width_end, battle_type_title_label_height_end),
        True,
        Point(mainmenu_challenge_complete_ok_trigger_pos_x,
              mainmenu_challenge_complete_ok_trigger_pos_y),
        True,
        ["assault", "encounter", "domination"],
        1
    ),
    CropProperty(
        "Prepare to Battle Summary Screen Map Name",
        CropArea(battle_map_name_label_width_start, battle_map_name_label_height_start,
                 battle_map_name_label_width_end, battle_map_name_label_height_end),
        True,
        Point(battle_map_name_label_trigger_pos_x,
              battle_map_name_label_trigger_pos_y),
        True,
        list(map_mask_file_path.keys()),
        1
    )
]

# in_battle_crops = [
#     CropProperty(
#         "Defeat / Victory Screen",
#         CropArea(battle_lose_survivor_part_width_start,battle_lose_survivor_part_height_start,battle_lose_survivor_part_width_end,battle_lose_survivor_part_height_end),
#         False,
#         Point(battle_lose_survivor_part_trigger_pos_x,battle_lose_survivor_part_trigger_pos_y),
#         False,
#         ["survivor's parts", "survivors parts", "survivorsparts"],
#         1
#     ),
#     CropProperty(
#         "Survivor's Kit",
#         CropArea(battle_lose_survivor_part_width_start,battle_lose_survivor_part_height_start,battle_lose_survivor_part_width_end,battle_lose_survivor_part_height_end),
#         False,
#         Point(battle_lose_survivor_part_trigger_pos_x,battle_lose_survivor_part_trigger_pos_y),
#         False,
#         ["survivor's parts", "survivors parts", "survivorsparts"],
#         1
#     )
# ]

finish_battle_crops = [
    CropProperty(
        "Finish Battle Close Button",
        CropArea(finish_battle_close_label_width_start, finish_battle_close_label_height_start,
                 finish_battle_close_label_width_end, finish_battle_close_label_height_end),
        True,
        Point(finish_battle_close_label_trigger_pos_x,
              finish_battle_close_label_trigger_pos_y),
        True,
        ["close", "c1ose"],
        1
    ),
    CropProperty(
        "Finish Battle BATTLE Button",
        CropArea(finish_battle_battle_label_width_start, finish_battle_battle_label_height_start,
                 finish_battle_battle_label_width_end, finish_battle_battle_label_height_end),
        False,
        Point(finish_battle_battle_label_trigger_pos_x,
              finish_battle_battle_label_trigger_pos_y),
        False,
        ["battle", "batt1e"],
        1
    )
]
