import cv2
import math
import numpy as np
import Constants as const
from MovementClass import MoveManagement, Move
from InputControl import KBPress, kbUp, kbDown
from Constants import CropProperty, Point
import threading
import random


class BattleManagement():

    def __init__(self):

        self.debug_window_name = "DebugWindow"
        cv2.namedWindow(self.debug_window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.debug_window_name, 1280, 720)
        self.detect_angle_rad = math.radians(45)
        self.detect_distance = 10

        self.battleIsInDelay = True
        self.acceptNewFrame = True
        self.isBattleAlreadyActive = False

        self.moveMgm = MoveManagement()

        self.tentacle_pos_lst = None
        self.tooCloseTuple = None

    def start(self):
        self.isBattleAlreadyActive = True
        self.battleIsInDelay = False
        kbUp("s")
        kbDown("w")

    def delayStart(self):
        if self.isBattleAlreadyActive:
            pass
        else:
            self.isBattleAlreadyActive = True
            kbDown("s")
            battleIsInDelayTimer = threading.Timer(15, self.start)
            battleIsInDelayTimer.start()

    def stop(self):
        print("stop")

    def __calcFrame(self):
        if self.__isEnemyNear():
            KBPress("1").start()

        self.__calculateTentacle()
        self.__determineTooClose()

        if self.tooCloseTuple is None:
            pass
        else:
            self.moveMgm.loadTooClose(self.tooCloseTuple)

            cv2.circle(self.debugMask, self.current_pos, 1, (255, 0, 0), 1)
            debug_test_mask = self.debugMask.copy()
            for pos in self.tentacle_pos_lst:
                cv2.line(debug_test_mask,
                         self.current_pos, pos, (255, 255, 0), 1)

            cv2.imshow(self.debug_window_name, debug_test_mask)

    def __acceptNewFrame(self):
        self.acceptNewFrame = True

    def loadFrame(self, frame):
        if (self.isBattleAlreadyActive is False) or self.battleIsInDelay or (self.acceptNewFrame is False):
            print("Frame is Wasted")
            print("battle start", self.isBattleAlreadyActive)
            print("battle is in delay", self.battleIsInDelay)
            print("processing frame", self.acceptNewFrame)
            pass
        else:
            self.acceptNewFrame = False
            acceptNewFrameTimer = threading.Timer(0.05, self.__acceptNewFrame)
            acceptNewFrameTimer.start()

            self.minimap_frame = frame[const.in_battle_mini_map_height_start:const.in_battle_mini_map_height_end,
                                       const.in_battle_mini_map_width_start: const.in_battle_mini_map_width_end]
            self.__calcFrame()

    def loadMapMask(self, mapImg, mask):
        self.grey_src_map = cv2.cvtColor(mapImg, cv2.COLOR_RGB2GRAY)
        self.mask = mask
        self.debugMask = self.mask.copy()
        self.debugMask = cv2.cvtColor(self.debugMask, cv2.COLOR_GRAY2RGB)

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

    def __determineTooClose(self):
        if self.tentacle_pos_lst is None:
            return
        else:
            left_pos = self.tentacle_pos_lst[0]
            left_too_close = False if self.mask[left_pos[1],
                                                left_pos[0]] == 0 else True
            center_pos = self.tentacle_pos_lst[1]
            center_too_close = False if self.mask[center_pos[1],
                                                  center_pos[0]] == 0 else True
            right_pos = self.tentacle_pos_lst[2]
            right_too_close = False if self.mask[right_pos[1],
                                                 right_pos[0]] == 0 else True
            self.tooCloseTuple = (
                left_too_close, center_too_close, right_too_close)

    def __calculateTentacle(self):
        self.prev_pos = self.current_pos
        self.current_pos = self.__getMiniMapReadLoc()

        self.pixelAdvanced = abs(self.current_pos.x - self.prev_pos.x) + \
            abs(self.current_pos.y - self.prev_pos.y)

        if self.pixelAdvanced <= 2:
            print("Position Too Close", self.pixelAdvanced)
            return

        center_rad = 0
        if self.current_pos.x == self.prev_pos.x:
            if self.current_pos.y > self.prev_pos.y:
                center_rad = -1 * math.pi / 2
            else:
                center_rad = math.pi / 2
        else:
            center_tan = abs(
                (self.current_pos.y - self.prev_pos.y) / (self.current_pos.x - self.prev_pos.x))
            if self.current_pos.x > self.prev_pos.x:

                if self.current_pos.y > self.prev_pos.y:  # BotRight
                    center_rad = -1 * math.atan(center_tan)
                else:  # TopRight
                    center_rad = math.atan(center_tan)

            else:
                if self.current_pos.y > self.prev_pos.y:  # BotLeft
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
                pos_x = self.current_pos.x + \
                    self.detect_distance * abs(math.cos(rad))
                pos_y = self.current_pos.y - \
                    self.detect_distance * abs(math.sin(rad))
                self.tentacle_pos_lst.append(Point(int(pos_x), int(pos_y)))
            elif rad > math.pi / 2 and rad <= math.pi:
                pos_x = self.current_pos.x - \
                    self.detect_distance * abs(math.cos(rad))
                pos_y = self.current_pos.y - \
                    self.detect_distance * abs(math.sin(rad))
                self.tentacle_pos_lst.append(Point(int(pos_x), int(pos_y)))
            elif (rad > math.pi and rad <= math.pi / 2 * 3) or (rad <= -1 * math.pi / 2):
                pos_x = self.current_pos.x - \
                    self.detect_distance * abs(math.cos(rad))
                pos_y = self.current_pos.y + \
                    self.detect_distance * abs(math.sin(rad))
                self.tentacle_pos_lst.append(Point(int(pos_x), int(pos_y)))
            elif (rad > -1 * math.pi / 2 and rad <= 0) or (rad > math.pi / 2 * 3 and rad <= math.pi * 2):
                pos_x = self.current_pos.x + \
                    self.detect_distance * abs(math.cos(rad))
                pos_y = self.current_pos.y + \
                    self.detect_distance * abs(math.sin(rad))
                self.tentacle_pos_lst.append(Point(int(pos_x), int(pos_y)))
            else:
                print("Check Rad Failed")

    def __isEnemyNear(self) -> bool:
        hsv_minimap_frame = cv2.cvtColor(self.minimap_frame, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 180, 180])
        upper_red = np.array([10, 255, 255])
        mask = cv2.inRange(hsv_minimap_frame, lower_red, upper_red)
        if cv2.countNonZero(mask) > 10:
            return True
        return False

    def calllOut(self):
        calloutLst = ["b", "c", "x", "z"]
        callout = random.choice(list(calloutLst))
        KBPress(callout).start()

    def carJack(self):
        KBPress("r").start()

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
