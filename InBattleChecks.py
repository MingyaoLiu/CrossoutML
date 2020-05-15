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

        self.stuckDetermineCount = 20
        self.stuckTimerCount = 0

        self.delayTime = 15

        self.frameDetectionInterval = 0.2

        self.base_detect_front_degree = 60
        self.detect_front_degree = self.base_detect_front_degree

        self.detect_angle_rad = math.radians(self.detect_front_degree)
        self.base_detect_distance = 10
        self.detect_distance = self.base_detect_distance

        self.battleIsInDelay = True
        self.acceptNewFrame = True
        self.isBattleAlreadyActive = False

        self.moveMgm = MoveManagement()

        self.tentacle_pos_lst = None
        self.tooCloseTuple = None
        self.current_pos = None
        self.prev_pos = None

        self.debug_window_name = "DebugWindow"
        cv2.namedWindow(self.debug_window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.debug_window_name, 1280, 720)

    def start(self):
        self.isBattleAlreadyActive = True
        self.battleIsInDelay = False

    def moveForwardBeforeStart(self):
        KBPress("b").start()
        kbUp("s")
        kbDown("w")
        moveForwardBeforeStartTimer = threading.Timer(2, self.start())
        moveForwardBeforeStartTimer.start()

    def delayStart(self):
        if self.isBattleAlreadyActive:
            pass
        else:
            self.isBattleAlreadyActive = True
            kbDown("s")
            battleIsInDelayTimer = threading.Timer(
                self.delayTime - 2, self.moveForwardBeforeStart)
            battleIsInDelayTimer.start()

    def stop(self):
        print("stop")

    def __calcFrame(self):

        if self.prev_pos is None:
            self.current_pos = self.__getMiniMapReadLoc()
            self.prev_pos = self.current_pos
            return

        if self.__isEnemyNear():
            KBPress("1").start()

        self.prev_pos = self.current_pos
        self.current_pos = self.__getMiniMapReadLoc()
        # self.pixelAdvanced = math.sqrt((self.current_pos.x - self.prev_pos.x) * (self.current_pos.x - self.prev_pos.x) + (
        #     self.current_pos.y - self.prev_pos.y) * (self.current_pos.y - self.prev_pos.y)) if self.prev_pos is not None else 0
        # print(self.pixelAdvanced)
        if abs(self.current_pos.x - self.prev_pos.x) + abs(self.current_pos.y - self.prev_pos.y) <= 1 and self.tentacle_pos_lst is not None and self.tooCloseTuple is not None:
            # print("Position Too Close ", self.pixelAdvanced," Using Previous tentacle points")
            self.stuckTimerCount += 1
            pass
        else:
            self.stuckTimerCount = 0
            self.tentacle_pos_lst = self.__calculateTentacle()
            self.tooCloseTuple = self.__calculateTooClose()

        if self.stuckTimerCount >= self.stuckDetermineCount:
            self.moveMgm.forceToBack()
        self.moveMgm.loadTooClose(self.tooCloseTuple)
        cv2.circle(self.debugMask, (int(self.current_pos.x),
                                    int(self.current_pos.y)), 1, (0, 0, 255), 1)
        debug_test_mask = self.debugMask.copy()
        for pos in self.tentacle_pos_lst:
            cv2.line(debug_test_mask,
                     (int(self.current_pos.x),
                      int(self.current_pos.y)), (int(pos.x), int(pos.y)), (255, 0, 0), 1)
        print(self.tooCloseTuple)
        cv2.imshow(self.debug_window_name, debug_test_mask)

    def __acceptNewFrame(self):
        self.acceptNewFrame = True

    def loadFrame(self, frame):
        if (self.isBattleAlreadyActive is False) or self.battleIsInDelay or (self.acceptNewFrame is False):
            # print("Frame is Wasted")
            pass
        else:
            self.acceptNewFrame = False
            acceptNewFrameTimer = threading.Timer(
                self.frameDetectionInterval, self.__acceptNewFrame)
            acceptNewFrameTimer.start()

            self.minimap_frame = frame[const.in_battle_mini_map_height_start:const.in_battle_mini_map_height_end,
                                       const.in_battle_mini_map_width_start: const.in_battle_mini_map_width_end]
            self.__calcFrame()

    def loadMapMask(self, mapImg, mask):
        self.grey_src_map = cv2.cvtColor(mapImg, cv2.COLOR_RGB2GRAY)
        self.mask = mask
        self.debugMask = self.mask.copy()
        self.debugMask = cv2.cvtColor(self.debugMask, cv2.COLOR_GRAY2RGB)

    def __getMiniMapReadLoc(self) -> Point:
        grey_minimap_frame = cv2.cvtColor(
            self.minimap_frame, cv2.COLOR_RGB2GRAY)
        scale_percent = 80
        new_width = int(grey_minimap_frame.shape[1] * scale_percent / 100)
        new_height = int(grey_minimap_frame.shape[0] * scale_percent / 100)
        grey_minimap_frame = cv2.resize(
            grey_minimap_frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
        method = eval('cv2.TM_CCOEFF')
        res = cv2.matchTemplate(self.grey_src_map, grey_minimap_frame, method)
        _, _, min_loc, max_loc = cv2.minMaxLoc(res)
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        circle_center_x = top_left[0] + new_width / 2
        circle_center_y = top_left[1] + new_height / 2
        return Point(circle_center_x, circle_center_y)

    def __calculateTooClose(self) -> (bool, bool, bool):
        left_pos = self.tentacle_pos_lst[0]
        left_too_close = False if self.mask[int(left_pos[1]),
                                            int(left_pos[0])] == 0 else True
        center_pos = self.tentacle_pos_lst[1]
        center_too_close = False if self.mask[int(center_pos[1]),
                                              int(center_pos[0])] == 0 else True
        right_pos = self.tentacle_pos_lst[2]
        right_too_close = False if self.mask[int(right_pos[1]),
                                             int(right_pos[0])] == 0 else True
        return (left_too_close, center_too_close, right_too_close)

    def __calculateTentacle(self) -> [Point]:

        # self.detect_distance = self.base_detect_distance if self.pixelAdvanced < 1 else self.base_detect_distance * \
        #     self.pixelAdvanced / 1.5

        # self.detect_front_degree = self.base_detect_front_degree if self.pixelAdvanced < 1 else self.base_detect_front_degree
        # self.detect_angle_rad = math.radians(self.detect_front_degree)

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
        pos_lst = []

        for rad in rad_list:
            if rad > 0 and rad <= math.pi / 2:
                pos_x = self.current_pos.x + \
                    self.detect_distance * abs(math.cos(rad))
                pos_y = self.current_pos.y - \
                    self.detect_distance * abs(math.sin(rad))
                pos_lst.append(Point(pos_x, pos_y))
            elif rad > math.pi / 2 and rad <= math.pi:
                pos_x = self.current_pos.x - \
                    self.detect_distance * abs(math.cos(rad))
                pos_y = self.current_pos.y - \
                    self.detect_distance * abs(math.sin(rad))
                pos_lst.append(Point(pos_x, pos_y))
            elif (rad > math.pi and rad <= math.pi / 2 * 3) or (rad <= -1 * math.pi / 2):
                pos_x = self.current_pos.x - \
                    self.detect_distance * abs(math.cos(rad))
                pos_y = self.current_pos.y + \
                    self.detect_distance * abs(math.sin(rad))
                pos_lst.append(Point(pos_x, pos_y))
            elif (rad > -1 * math.pi / 2 and rad <= 0) or (rad > math.pi / 2 * 3 and rad <= math.pi * 2):
                pos_x = self.current_pos.x + \
                    self.detect_distance * abs(math.cos(rad))
                pos_y = self.current_pos.y + \
                    self.detect_distance * abs(math.sin(rad))
                pos_lst.append(Point(pos_x, pos_y))
            else:
                raise Exception("Check Rad Failed")
        return pos_lst

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
