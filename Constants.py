


import enum


screenWidth = 1920
screenHeight = 1080

class BattleMode(enum.IntEnum):
    scrap = 0
    wire = 1
    battery = 2
    # patrol = 3

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


class ScreenStep(enum.IntEnum):
    Login = 0
    WelcomeScreen = 1
    ChallengeCompleteScreen = 2
    MainMenu = 3
    SelectMode = 4
    GetResourceMenu = 5
    BattlePrepareScreen = 6
    InBattleNow = 7
    DeathWaiting = 8
    FinishBattleScreen = 9
    debug = 10



login_label_width = 70
login_label_width_start = int(screenWidth / 7.5 - login_label_width / 2)
login_label_width_end = int(screenWidth / 7.5 + login_label_width / 2)
login_label_height = 40
login_label_height_start = int(screenHeight / 2 - login_label_height / 2)
login_label_height_end = int(screenHeight / 2 + login_label_height / 2)
login_label_trigger_pos_x = int(login_label_width_start + login_label_width / 2)
login_label_trigger_pos_y = int(login_label_height_start + login_label_height / 2)

welcome_promo_label_width = 70
welcome_promo_label_width_start = int(screenWidth / 1.5 - welcome_promo_label_width / 2)
welcome_promo_label_width_end = int(screenWidth / 1.5 + welcome_promo_label_width / 2)
welcome_promo_label_height = 40
welcome_promo_label_height_start = int(screenHeight / 1.5 - welcome_promo_label_height / 2)
welcome_promo_label_height_end = int(screenHeight / 1.5 + welcome_promo_label_height / 2)
welcome_promo_label_trigger_pos_x = int(welcome_promo_label_width_start + welcome_promo_label_width / 2)
welcome_promo_label_trigger_pos_y = int(welcome_promo_label_height_start + welcome_promo_label_height / 2)

mainmenu_battle_label_width = 140
mainmenu_battle_label_width_start = int(screenWidth / 2 - mainmenu_battle_label_width / 2)
mainmenu_battle_label_width_end = int(screenWidth / 2 + mainmenu_battle_label_width / 2)
mainmenu_battle_label_height = 50
mainmenu_battle_label_height_start = int(screenHeight / 5.65 - mainmenu_battle_label_height / 2)
mainmenu_battle_label_height_end = int(screenHeight / 5.65 + mainmenu_battle_label_height / 2)
mainmenu_battle_label_trigger_pos_x = int(mainmenu_battle_label_width_start + mainmenu_battle_label_width / 2)
mainmenu_battle_label_trigger_pos_y = int(mainmenu_battle_label_height_start + mainmenu_battle_label_height / 2)

mainmenu_select_mode_label_width = 130
mainmenu_select_mode_label_width_start = int(screenWidth / 2 - mainmenu_select_mode_label_width / 2)
mainmenu_select_mode_label_width_end = int(screenWidth / 2 + mainmenu_select_mode_label_width / 2)
mainmenu_select_mode_label_height = 60
mainmenu_select_mode_label_height_start = int(screenHeight / 4 - mainmenu_select_mode_label_height / 2)
mainmenu_select_mode_label_height_end = int(screenHeight / 4 + mainmenu_select_mode_label_height / 2)
mainmenu_select_mode_label_trigger_pos_x = int(mainmenu_select_mode_label_width_start + mainmenu_select_mode_label_width / 2)
mainmenu_select_mode_label_trigger_pos_y = int(mainmenu_select_mode_label_height_start + mainmenu_select_mode_label_height / 2)

get_resource_battle_label_width = 130
get_resource_battle_label_width_start = int(screenWidth / 3 - get_resource_battle_label_width / 2)
get_resource_battle_label_width_end = int(screenWidth / 3 + get_resource_battle_label_width / 2)
get_resource_battle_label_height = 60
get_resource_battle_label_height_start = int(screenHeight / 1.37 - get_resource_battle_label_height / 2)
get_resource_battle_label_height_end = int(screenHeight / 1.37 + get_resource_battle_label_height / 2)
get_resource_battle_label_trigger_pos_x = int(get_resource_battle_label_width_start + get_resource_battle_label_width / 2)
get_resource_battle_label_trigger_pos_y = int(get_resource_battle_label_height_start + get_resource_battle_label_height / 2)

get_resource_patrol_battle_label_height_start = int(screenHeight / 1.3 - get_resource_battle_label_height / 2)
get_resource_patrol_battle_label_height_end = int(screenHeight / 1.3 + get_resource_battle_label_height / 2)
get_resource_patrol_battle_label_trigger_pos_x = int(get_resource_battle_label_width_start + get_resource_battle_label_width / 2)
get_resource_patrol_battle_label_trigger_pos_y = int(get_resource_patrol_battle_label_height_start + get_resource_battle_label_height / 2)

battle_type_title_label_width = 250
battle_type_title_label_width_start = int(screenWidth / 12 + 10 - battle_type_title_label_width / 2)
battle_type_title_label_width_end = int(screenWidth / 12 + 10 + battle_type_title_label_width / 2)
battle_type_title_label_height = 60
battle_type_title_label_height_start = int(screenHeight / 13.5 - battle_type_title_label_height / 2)
battle_type_title_label_height_end = int(screenHeight / 13.5 + battle_type_title_label_height / 2)
battle_type_title_label_trigger_pos_x = int(battle_type_title_label_width_start + battle_type_title_label_width / 2)
battle_type_title_label_trigger_pos_y = int(battle_type_title_label_height_start + battle_type_title_label_height / 2)


battle_victory_defeat_giant_width = 550
battle_victory_defeat_giant_width_start = int(screenWidth / 2 - battle_victory_defeat_giant_width / 2)
battle_victory_defeat_giant_width_end = int(screenWidth / 2 + battle_victory_defeat_giant_width / 2)
battle_victory_defeat_giant_width_height = 150
battle_victory_defeat_giant_width_height_start = int(screenHeight / 2.1 - battle_victory_defeat_giant_width_height / 2)
battle_victory_defeat_giant_width_height_end = int(screenHeight / 2.1 + battle_victory_defeat_giant_width_height / 2)
battle_victory_defeat_giant_width_trigger_pos_x = int(battle_victory_defeat_giant_width_start + battle_victory_defeat_giant_width / 2)
battle_victory_defeat_giant_width_trigger_pos_y = int(battle_victory_defeat_giant_width_height_start + battle_victory_defeat_giant_width_height / 2)


battle_lose_wait_width = 32
battle_lose_wait_width_start = int(screenWidth / 2 - 112 - battle_lose_wait_width / 2)
battle_lose_wait_width_end = int(screenWidth / 2 - 112 + battle_lose_wait_width / 2)
battle_lose_wait_height = 32
battle_lose_wait_height_start = int(screenHeight / 1.33 - battle_lose_wait_height / 2)
battle_lose_wait_height_end = int(screenHeight / 1.33 + battle_lose_wait_height / 2)
battle_lose_wait_trigger_pos_x = int(battle_lose_wait_width_start + battle_lose_wait_width / 2)
battle_lose_wait_trigger_pos_y = int(battle_lose_wait_height_start + battle_lose_wait_height / 2)

battle_lose_survivor_part_width = 240
battle_lose_survivor_part_width_start = int(screenWidth- battle_lose_survivor_part_width)
battle_lose_survivor_part_width_end = int(screenWidth)
battle_lose_survivor_part_height = 50
battle_lose_survivor_part_height_start = int(screenHeight / 2.4 - battle_lose_survivor_part_height / 2)
battle_lose_survivor_part_height_end = int(screenHeight / 2.4 + battle_lose_survivor_part_height / 2)
battle_lose_survivor_part_trigger_pos_x = int(battle_lose_survivor_part_width_start + battle_lose_survivor_part_width / 2)
battle_lose_survivor_part_trigger_pos_y = int(battle_lose_survivor_part_height_start + battle_lose_survivor_part_height / 2)


finish_battle_close_label_width = 120
finish_battle_close_label_width_start = int(screenWidth / 5 * 3.25 - finish_battle_close_label_width / 2)
finish_battle_close_label_width_end = int(screenWidth / 5 * 3.25 + finish_battle_close_label_width / 2)
finish_battle_close_label_height = 50
finish_battle_close_label_height_start = int(screenHeight / 13 * 12.1 - finish_battle_close_label_height / 2)
finish_battle_close_label_height_end = int(screenHeight / 13 * 12.1 + finish_battle_close_label_height / 2)
finish_battle_close_label_trigger_pos_x = int(finish_battle_close_label_width_start + finish_battle_close_label_width / 2)
finish_battle_close_label_trigger_pos_y = int(finish_battle_close_label_height_start + finish_battle_close_label_height / 2)

finish_battle_battle_label_width = 140
finish_battle_battle_label_width_start = int(screenWidth / 5 * 4.1 - finish_battle_battle_label_width / 2)
finish_battle_battle_label_width_end = int(screenWidth / 5 * 4.1 + finish_battle_battle_label_width / 2)
finish_battle_battle_label_height = 50
finish_battle_battle_label_height_start = int(screenHeight / 13 * 12.1 - finish_battle_battle_label_height / 2)
finish_battle_battle_label_height_end = int(screenHeight / 13 * 12.1 + finish_battle_battle_label_height / 2)
finish_battle_battle_label_trigger_pos_x = int(finish_battle_battle_label_width_start + finish_battle_battle_label_width / 2)
finish_battle_battle_label_trigger_pos_y = int(finish_battle_battle_label_height_start + finish_battle_battle_label_height / 2)


mainmenu_challenge_complete_ok_width = 60
mainmenu_challenge_complete_ok_width_start = int(screenWidth / 2 + 110 - mainmenu_challenge_complete_ok_width / 2)
mainmenu_challenge_complete_ok_width_end = int(screenWidth / 2 + 110 + mainmenu_challenge_complete_ok_width / 2)
mainmenu_challenge_complete_ok_height = 40
mainmenu_challenge_complete_ok_height_start = int(screenHeight / 1.08 - mainmenu_challenge_complete_ok_height / 2)
mainmenu_challenge_complete_ok_height_end = int(screenHeight / 1.08 + mainmenu_challenge_complete_ok_height / 2)
mainmenu_challenge_complete_ok_trigger_pos_x = int(mainmenu_challenge_complete_ok_width_start + mainmenu_challenge_complete_ok_width / 2)
mainmenu_challenge_complete_ok_trigger_pos_y = int(mainmenu_challenge_complete_ok_height_start + mainmenu_challenge_complete_ok_height / 2)


in_battle_front_view_width = 720
in_battle_front_view_width_start = int(screenWidth / 2 - in_battle_front_view_width / 2)
in_battle_front_view_width_end = int(screenWidth / 2 + in_battle_front_view_width / 2)
in_battle_front_view_height = 260
in_battle_front_view_height_start = int(screenHeight / 2.2 - in_battle_front_view_height / 2)
in_battle_front_view_height_end = int(screenHeight / 2.2 + in_battle_front_view_height / 2)
in_battle_front_view_trigger_pos_x = int(in_battle_front_view_width_start + in_battle_front_view_width / 2)
in_battle_front_view_trigger_pos_y = int(in_battle_front_view_height_start + in_battle_front_view_height / 2)


in_battle_health_digit_width = 46
in_battle_health_digit_width_start = int(screenWidth / 2 - 58 - in_battle_health_digit_width / 2)
in_battle_health_digit_width_end = int(screenWidth / 2 - 58 + in_battle_health_digit_width / 2)
in_battle_health_digit_height = 22
in_battle_health_digit_height_start = int(screenHeight - 28 - in_battle_health_digit_height / 2)
in_battle_health_digit_height_end = int(screenHeight - 28 + in_battle_health_digit_height / 2)
in_battle_health_digit_trigger_pos_x = int(in_battle_health_digit_width_start + in_battle_health_digit_width / 2)
in_battle_health_digit_trigger_pos_y = int(in_battle_health_digit_height_start + in_battle_health_digit_height / 2)


in_battle_mini_map_width = 150
in_battle_mini_map_width_start = int(screenWidth - 210 - in_battle_mini_map_width / 2)
in_battle_mini_map_width_end = int(screenWidth - 210 + in_battle_mini_map_width / 2)
in_battle_mini_map_height = 150
in_battle_mini_map_height_start = int(screenHeight - 180 - in_battle_mini_map_height / 2)
in_battle_mini_map_height_end = int(screenHeight - 180 + in_battle_mini_map_height / 2)
in_battle_mini_map_trigger_pos_x = int(in_battle_mini_map_width_start + in_battle_mini_map_width / 2)
in_battle_mini_map_trigger_pos_y = int(in_battle_mini_map_height_start + in_battle_mini_map_height / 2)

