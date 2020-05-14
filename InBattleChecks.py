import cv2
import math
import numpy as np
import Constants as const
from MovementClass import Move
from InputControl import KBPress
from Constants import CropProperty, Point


class BattleFrame():
    def __init__(self, frame, prev_frame, detectedMap, map_mask):
        self.map_mask = map_mask
        self.frame = frame
        self.prev_frame = prev_frame

        self.grey_src_map = cv2.cvtColor(detectedMap, cv2.COLOR_RGB2GRAY)
        self.minimap_frame = frame[const.in_battle_mini_map_height_start:const.in_battle_mini_map_height_end,
                                   const.in_battle_mini_map_width_start: const.in_battle_mini_map_width_end]
        self.prev_1_minimap_frame = prev_frame[const.in_battle_mini_map_height_start:const.in_battle_mini_map_height_end,
                                               const.in_battle_mini_map_width_start: const.in_battle_mini_map_width_end]

        self.detect_angle_rad = math.radians(45)
        self.detect_distance = 10
        self.tentacle_pos_lst = []

    def __getMiniMapReadLoc(self, minimap_frame) -> Point:
        grey_minimap_frame = minimap_frame.copy()
        grey_minimap_frame = cv2.cvtColor(
            grey_minimap_frame, cv2.COLOR_RGB2GRAY)
        scale_percent = 80
        new_width = int(grey_minimap_frame.shape[1] * scale_percent / 100)
        new_height = int(grey_minimap_frame.shape[0] * scale_percent / 100)
        grey_minimap_frame = cv2.resize(
            grey_minimap_frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
        method = eval('cv2.TM_CCOEFF')
        res = cv2.matchTemplate(self.grey_src_map, grey_minimap_frame, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        circle_center_x = int(top_left[0] + new_width / 2)
        circle_center_y = int(top_left[1] + new_height / 2)
        return Point(circle_center_x, circle_center_y)

    def calculateTentacle(self) -> [Point]:
        current_pos = self.__getMiniMapReadLoc(self.minimap_frame)
        prev_pos = self.__getMiniMapReadLoc(self.prev_1_minimap_frame)
        center_rad = 0
        if current_pos.x == prev_pos.x:
            if current_pos.y > prev_pos.y:
                center_rad = -1 * math.pi / 2
            else:
                center_rad = math.pi / 2
        else:
            center_tan = abs(
                (current_pos.y - prev_pos.y) / (current_pos.x - prev_pos.x))
            if current_pos.x > prev_pos:

                if current_pos.y > prev_pos.y:  # BotRight
                    center_rad = -1 * math.atan(center_tan)
                else:  # TopRight
                    center_rad = math.atan(center_tan)

            else:
                if current_pos.y > prev_pos.y:  # BotLeft
                    center_rad = math.pi + \
                        math.atan(center_tan)
                else:  # TopLeft
                    center_rad = math.pi - \
                        math.atan(center_tan)

        left_rad = center_rad + self.detect_angle_rad
        right_rad = center_rad - self.detect_angle_rad
        rad_list = [left_rad, center_rad, right_rad]
        self.tentacle_pos_lst = []

        for rad in rad_list:
            if rad > 0 and rad <= math.pi / 2:
                pos_x = current_pos.x + \
                    self.detect_distance * abs(math.cos(rad))
                pos_y = current_pos.y - \
                    self.detect_distance * abs(math.sin(rad))
                self.tentacle_pos_lst.append(Point(int(pos_x), int(pos_y)))
            elif rad > math.pi / 2 and rad <= math.pi:
                pos_x = current_pos.x - \
                    self.detect_distance * abs(math.cos(rad))
                pos_y = current_pos.y - \
                    self.detect_distance * abs(math.sin(rad))
                self.tentacle_pos_lst.append(Point(int(pos_x), int(pos_y)))
            elif (rad > math.pi and rad <= math.pi / 2 * 3) or (rad <= -1 * math.pi / 2):
                pos_x = current_pos.x - \
                    self.detect_distance * abs(math.cos(rad))
                pos_y = current_pos.y + \
                    self.detect_distance * abs(math.sin(rad))
                self.tentacle_pos_lst.append(Point(int(pos_x), int(pos_y)))
            elif (rad > -1 * math.pi / 2 and rad <= 0) or (rad > math.pi / 2 * 3 and rad <= math.pi * 2):
                pos_x = current_pos.x + \
                    self.detect_distance * abs(math.cos(rad))
                pos_y = current_pos.y + \
                    self.detect_distance * abs(math.sin(rad))
                self.tentacle_pos_lst.append(Point(int(pos_x), int(pos_y)))
            else:
                print("Check Rad Failed")
                return []

        return self.tentacle_pos_lst

    def isEnemyNear(self) -> bool:
        hsv_minimap_frame = cv2.cvtColor(self.minimap_frame, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 180, 180])
        upper_red = np.array([10, 255, 255])
        mask = cv2.inRange(hsv_minimap_frame, lower_red, upper_red)
        if cv2.countNonZero(mask) > 10:
            return True
        return False

    def calculateTurn(self) -> bool:
        left_pos = self.tentacle_pos_lst[0]
        left_too_close = False if self.map_mask[left_pos[1],
                                                left_pos[0]] == 0 else True
        center_pos = self.tentacle_pos_lst[1]
        center_too_close = False if self.map_mask[center_pos[1],
                                                  center_pos[0]] == 0 else True
        right_pos = self.tentacle_pos_lst[2]
        right_too_close = False if self.map_mask[right_pos[1],
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
                        Move(
                            direction, straight_block_time).start()
                    else:
                        if lastTurnCmd == const.MoveDirection.frontRight or lastTurnCmd == const.MoveDirection.right:
                            direction = const.MoveDirection.backRight
                            Move(
                                direction, extra_turn_block_time).start()
                        elif lastTurnCmd == const.MoveDirection.frontLeft or lastTurnCmd == const.MoveDirection.left:
                            direction = const.MoveDirection.backLeft
                            Move(
                                direction, extra_turn_block_time).start()
                        else:
                            direction = const.MoveDirection.back
                            Move(
                                direction, full_turn_block_time).start()
                else:  # 1 1 0
                    direction = const.MoveDirection.right
                    Move(
                        direction, right_angle_block_time).start()
            else:
                if right_too_close:  # 0 1 1
                    direction = const.MoveDirection.left
                    Move(
                        direction, right_angle_block_time).start()
                else:  # 0 1 0
                    if lastTurnCmd == const.MoveDirection.frontRight or lastTurnCmd == const.MoveDirection.right:
                        direction = const.MoveDirection.right
                        Move(
                            direction, right_angle_block_time).start()
                    elif lastTurnCmd == const.MoveDirection.frontLeft or lastTurnCmd == const.MoveDirection.left:
                        direction = const.MoveDirection.left
                        Move(
                            direction, right_angle_block_time).start()
        else:
            isInAllowedZone = True
            if left_too_close:
                if right_too_close:  # 1 0 1
                    direction = const.MoveDirection.front
                    Move(
                        direction, straight_block_time).start()
                else:  # 1 0 0
                    direction = const.MoveDirection.frontRight
                    Move(
                        direction, minor_turn_block_time).start()
            else:
                if right_too_close:  # 0 0 1
                    direction = const.MoveDirection.frontLeft
                    Move(
                        direction, minor_turn_block_time).start()
                else:  # 0 0 0
                    if lastTurnCmd == const.MoveDirection.frontRight or lastTurnCmd == const.MoveDirection.right:
                        direction = const.MoveDirection.frontLeft
                        Move(
                            direction, right_angle_block_time).start()
                    elif lastTurnCmd == const.MoveDirection.frontLeft or lastTurnCmd == const.MoveDirection.left:
                        direction = const.MoveDirection.frontRight
                        Move(
                            direction, right_angle_block_time).start()
        print(direction)
        turnCommandStack.insert(0, direction)
        if len(turnCommandStack) >= 5:
            turnCommandStack.pop()

    ########## MINIMAP TRACK ENEMY COUNT #############

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
