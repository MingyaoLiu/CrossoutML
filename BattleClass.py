import cv2
import math
import numpy as np
import Constants as const
from MovementClass import MoveManagement, Move
from InputControl import KBPress, kbUp, kbDown
from Constants import CropProperty, Point, PointData, CenterData, BattleFrame
import threading
import random
from SettingsClass import getGlobalSetting
import time
from DebugClass import getDebugger


class BattleManagement():

    def __init__(self):

        self.speedMultiplier = 4.25

        self.anakinIsKilling = False

        self.low_speed_top_limit = 50

        self.battleFrameStack = []
        self.currentBattleFrame = None

        self.delayTime = 4

        self.acceptNewFrame = True
        self.isBattleAlreadyActive = False

        self.moveMgm = MoveManagement()

        self.currentStuckTimerCount = 0
        self.stuckDetermineCount = getGlobalSetting().settings.checkStuckFrameCount or 20

        self.detect_front_degree = getGlobalSetting().settings.frontDetectDegree or 45

        self.detect_angle_rad = math.radians(self.detect_front_degree)

        self.center_far_distance = getGlobalSetting().settings.centerFarDetectDistance or 30
        self.lr_detect_distance = getGlobalSetting().settings.lrDetectDistance or 10

        self.center_low_distance = getGlobalSetting().settings.centerLowDetectDistance
        self.center_mid_distance = self.center_low_distance + (
            self.center_far_distance - self.center_low_distance) / 2

        self.frameDetectionInterval = 0 if getGlobalSetting(
        ).settings.detectionFPS == 0 else 1000 / getGlobalSetting().settings.detectionFPS

    def start(self):
        self.isBattleAlreadyActive = True

    def moveForwardBeforeStart(self):
        KBPress("b").start()
        kbUp("s")
        kbDown("w")
        moveForwardBeforeStartTimer = threading.Timer(2, self.start)
        moveForwardBeforeStartTimer.start()

    def delayStart(self):
        if self.isBattleAlreadyActive:
            pass
        else:
            kbDown("s")
            battleIsInDelayTimer = threading.Timer(
                self.delayTime - 2, self.moveForwardBeforeStart)
            battleIsInDelayTimer.start()

    def stop(self):
        print("stop")

    def __anakinRest(self):
        self.anakinIsKilling = False

    def __executeOrder66(self):
        if self.anakinIsKilling:
            pass
        else:
            self.anakinIsKilling = True
            KBPress("1").start()
            killTimer = threading.Timer(2, self.__anakinRest)
            killTimer.start()

    def __calcFrame(self, minimap_frame):

        if self.grey_src_map is None or minimap_frame is None:
            raise Exception("No Src Map or minimap Loaded")

        if self.currentStuckTimerCount > self.stuckDetermineCount:
            if self.currentStuckTimerCount > 2 * self.stuckDetermineCount:
                # print("STUCK MOFO")
                KBPress("r")
                # self.moveMgm.forceToBack()
                self.currentStuckTimerCount = 0
            else:
                # print("PRE STUCK MOFO")
                if self.moveMgm.forcingBack:
                    pass
                else:
                    kbUp("spacebar")
                    kbDown("w")

        # Check if enemy is near, fire if near
        if self.__isEnemyNear(minimap_frame):
            self.__executeOrder66()

        # generate current battle frame
        proc_time = time.perf_counter()
        currentBattleFrame = self.__calcBattleFrame(
            proc_time, self.grey_src_map, minimap_frame)

        if currentBattleFrame and currentBattleFrame.record:
            self.battleFrameStack.insert(0, currentBattleFrame)
            if len(self.battleFrameStack) >= 11:
                self.battleFrameStack.pop()

        if currentBattleFrame and currentBattleFrame.center and currentBattleFrame.left and currentBattleFrame.right:
            self.moveMgm.loadNewBF(currentBattleFrame)

        if getGlobalSetting().settings.showDebugWindow and currentBattleFrame:
            if currentBattleFrame.posData.pos:
                cv2.circle(self.debugMask, (int(currentBattleFrame.posData.pos.x),
                                            int(currentBattleFrame.posData.pos.y)), 1, (0, 0, 255), 2)
            debug_test_mask = self.debugMask.copy()

            if currentBattleFrame.center:
                cv2.line(debug_test_mask,
                         (int(currentBattleFrame.center.far_rev.pos.x),
                          int(currentBattleFrame.center.far_rev.pos.y)), (int(currentBattleFrame.center.far.pos.x), int(currentBattleFrame.center.far.pos.y)), (255, 0, 0), 2)
            if currentBattleFrame.posData.pos and currentBattleFrame.center and currentBattleFrame.left and currentBattleFrame.right:
                pass
                # cv2.line(debug_test_mask,
                #          (int(currentBattleFrame.posData.pos.x),
                #           int(currentBattleFrame.posData.pos.y)), (int(currentBattleFrame.left.pos.x), int(currentBattleFrame.left.pos.y)), (255, 0, 0), 1)
                # cv2.line(debug_test_mask,
                #          (int(currentBattleFrame.posData.pos.x),
                #           int(currentBattleFrame.posData.pos.y)), (int(currentBattleFrame.right.pos.x), int(currentBattleFrame.right.pos.y)), (255, 0, 0), 1)
            getDebugger().debugDisplay(debug_test_mask)

    def __acceptNewFrame(self):
        if self.frameDetectionInterval:
            self.acceptNewFrame = True

    def loadFrame(self, frame):
        # print("load frame")
        if self.isBattleAlreadyActive is False or self.acceptNewFrame is False:
            # print("Frame is Wasted")
            return
        else:
            # print("Good Frame")
            if self.frameDetectionInterval:
                self.acceptNewFrame = False
                acceptNewFrameTimer = threading.Timer(
                    self.frameDetectionInterval, self.__acceptNewFrame)
                acceptNewFrameTimer.start()

            minimap_frame = frame[const.in_battle_mini_map_height_start:const.in_battle_mini_map_height_end,
                                  const.in_battle_mini_map_width_start: const.in_battle_mini_map_width_end]
            self.__calcFrame(minimap_frame)

    def loadMapMask(self, mapImg, mask):
        self.grey_src_map = cv2.cvtColor(mapImg, cv2.COLOR_RGB2GRAY)
        self.mask = mask
        self.debugMask = self.mask.copy()
        self.debugMask = cv2.cvtColor(self.debugMask, cv2.COLOR_GRAY2RGB)

    def __calcDistance(self, pos1: Point, pos2: Point) -> float:
        if (pos1 == pos2):
            return 0
        return math.sqrt((pos1.x - pos2.x) * (pos1.x - pos2.x) + (pos1.y - pos2.y) * (pos1.y - pos2.y))

    def __calcBattleFrame(self, time, src_map, minimap_frame) -> BattleFrame:
        current_pos = self.__getMiniMapReadLoc(src_map,
                                               minimap_frame)
        minimap_frame_height,minimap_frame_width = minimap_frame.shape[:2]
        arrow_frame_width = 30
        arrow_frame_height = 30
        arrow_frame_height_start = int((minimap_frame_height - arrow_frame_height) / 2)
        arrow_frame_width_start = int((minimap_frame_width - arrow_frame_width) / 2)
        minimap_arrow_frame = minimap_frame[arrow_frame_height_start:arrow_frame_height_start + arrow_frame_height, arrow_frame_width_start: arrow_frame_width_start + arrow_frame_width] 

        if len(self.battleFrameStack) == 0:
            pos_data = PointData(current_pos, self.__calcTooClose(current_pos))
            return BattleFrame(True, time, 0, 0, pos_data, None, None, None, None)
        elif len(self.battleFrameStack) < 10: 
            prev_bf = self.battleFrameStack[0]
            pos_data = PointData(current_pos, self.__calcTooClose(current_pos))
            pixel_distance = self.__calcDistance(
                prev_bf.posData.pos, current_pos)
            return BattleFrame(True, time, pixel_distance, 0, pos_data, None, None, None, None)



        prev_bf = self.battleFrameStack[5]
        pixel_distance = self.__calcDistance(prev_bf.posData.pos, current_pos)

        # if pixel_distance < 4:
        #     print("PIXEL", pixel_distance)
        #     if pixel_distance == 0:
        #         self.currentStuckTimerCount += 1
        #         return None
        #     else:
        #         i = 0
        #         while i < len(self.battleFrameStack):
        #             total_distance = self.__calcDistance(
        #                 self.battleFrameStack[i].posData.pos, current_pos)
        #             if total_distance > 4:
        #                 prev_bf = self.battleFrameStack[i]
        #                 break
        #             i += 1
        #         if total_distance < 4:
        #             return None


        print(self.__calcRadWithContour(minimap_arrow_frame))


        # self.currentStuckTimerCount = 0

        # if self.battleFrameStack[0].centerRad:
            

        center_rad = self.__calcRad(prev_bf.posData.pos, current_pos, minimap_arrow_frame)

        # if center_rad:
        #     pass
        # else:
        if center_rad is None:
            return None
            

        speed = pixel_distance / (time - prev_bf.time) * self.speedMultiplier


        left_rad = center_rad + self.detect_angle_rad
        right_rad = center_rad - self.detect_angle_rad

        pos_data = PointData(current_pos, self.__calcTooClose(current_pos))

        center_low_dist_pos = self.__calcEndPoint(
            current_pos, center_rad, self.center_low_distance)
        center_mid_dist_pos = self.__calcEndPoint(
            current_pos, center_rad, self.center_mid_distance)
        center_far_dist_pos = self.__calcEndPoint(
            current_pos, center_rad, self.center_far_distance)
        left_low_dist = self.__calcEndPoint(
            current_pos, left_rad, self.lr_detect_distance)
        right_low_dist = self.__calcEndPoint(
            current_pos, right_rad, self.lr_detect_distance)

        center_low_pd = PointData(
            center_low_dist_pos, self.__calcTooClose(center_low_dist_pos))
        center_mid_pd = PointData(
            center_mid_dist_pos, self.__calcTooClose(center_mid_dist_pos))
        center_far_pd = PointData(
            center_far_dist_pos, self.__calcTooClose(center_far_dist_pos))



        center_low_dist_rev_pos = self.__calcEndPoint(
            current_pos, math.pi + center_rad, self.center_low_distance)
        center_mid_dist_rev_pos = self.__calcEndPoint(
            current_pos, math.pi + center_rad, self.center_mid_distance)
        center_far_dist_rev_pos = self.__calcEndPoint(
            current_pos, math.pi + center_rad, self.center_far_distance)
    
        center_low_rev_pd = PointData(
            center_low_dist_rev_pos, self.__calcTooClose(center_low_dist_rev_pos))
        center_mid_rev_pd = PointData(
            center_mid_dist_rev_pos, self.__calcTooClose(center_mid_dist_rev_pos))
        center_far_rev_pd = PointData(
            center_far_dist_rev_pos, self.__calcTooClose(center_far_dist_rev_pos))

        center_data = CenterData(center_low_pd, center_mid_pd, center_far_pd, center_low_rev_pd, center_mid_rev_pd, center_far_rev_pd)

        left_low_pd = PointData(
            left_low_dist, self.__calcTooClose(left_low_dist))
        right_low_pd = PointData(
            right_low_dist, self.__calcTooClose(right_low_dist))

        return BattleFrame(True, time, pixel_distance, speed, pos_data, center_rad, center_data, left_low_pd, right_low_pd)

    def __getMiniMapReadLoc(self, src_map, minimap_frame) -> Point:
        grey_minimap_frame = cv2.cvtColor(minimap_frame, cv2.COLOR_RGB2GRAY)
        
        scale_percent = 80
        new_width = int(grey_minimap_frame.shape[1] * scale_percent / 100)
        new_height = int(grey_minimap_frame.shape[0] * scale_percent / 100)
        grey_minimap_frame = cv2.resize(
            grey_minimap_frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
        method = eval('cv2.TM_CCOEFF')
        res = cv2.matchTemplate(src_map, grey_minimap_frame, method)
        _, _, min_loc, max_loc = cv2.minMaxLoc(res)
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        circle_center_x = top_left[0] + new_width / 2
        circle_center_y = top_left[1] + new_height / 2
        return Point(circle_center_x, circle_center_y)

    def __calcTooClose(self, pos: Point) -> bool:
        # Coordinate is Reversed Here
        return False if self.mask[int(pos.y), int(pos.x)] == 0 else True

    def __calcPixelAdvanced(self, pos1, pos2) -> int:
        return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)


    def __calcRadWithContour(self, minimap_arrow_frame) -> float:
        img = cv2.cvtColor(minimap_arrow_frame, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(img, 195, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_NONE )
        if len(contours) >= 1:
            cnt = contours[0]
            [vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01)
            # print(math.atan(vy,vx))
            return -1 * math.atan(vy / vx)
        else:
            print("CONTOUR IS 0")
        return None

    def __calcRad(self, start_pos: Point, end_pos: Point, minimap_arrow_frame) -> float:

        contour_rad = self.__calcRadWithContour(minimap_arrow_frame)
        if contour_rad:
            # if end_pos.x > start_pos.x:
            #     if end_pos.y > start_pos.y:                 # BotRight
            #         return -1 * abs(contour_rad) 
            #     else:                                       # TopRight
            #         return abs(contour_rad) 
            # else:
            #     if end_pos.y > start_pos.y:                 # BotLeft
            #         return math.pi + abs(contour_rad) 
            #     else:                                       # TopLeft
            #         return math.pi - abs(contour_rad) 
            print(contour_rad)
            return contour_rad
        else:
            return None


        # if end_pos.x == start_pos.x:
        #     if end_pos.y > start_pos.y:
        #         return -1 * contour_rad if contour_rad else -1 * math.pi / 2
        #     else:
        #         return contour_rad if contour_rad else math.pi / 2
        # else:
        #     center_tan = abs((end_pos.y - start_pos.y) /
        #                      (end_pos.x - start_pos.x))
        #     center_rad = math.atan(center_tan)

        #     print(center_rad, contour_rad)
            

        #     if end_pos.x > start_pos.x:
        #         if end_pos.y > start_pos.y:                 # BotRight
                    
        #             return -1 * contour_rad if contour_rad else -1 * center_rad
        #         else:                                       # TopRight
        #             return contour_rad if contour_rad else center_rad
        #     else:
        #         if end_pos.y > start_pos.y:                 # BotLeft
        #             return math.pi + contour_rad if contour_rad else math.pi + center_rad
        #         else:                                       # TopLeft
        #             return math.pi - contour_rad if contour_rad else math.pi - center_rad

    def __calcEndPoint(self, start_pos: Point, rad: float, distance: float) -> Point:

        
        if rad > 0 and rad <= math.pi / 2:
            pos_x = start_pos.x + \
                distance * abs(math.cos(rad))
            pos_y = start_pos.y - \
                distance * abs(math.sin(rad))
            return Point(pos_x, pos_y)
        elif rad > math.pi / 2 and rad <= math.pi:
            pos_x = start_pos.x - \
                distance * abs(math.cos(rad))
            pos_y = start_pos.y - \
                distance * abs(math.sin(rad))
            return Point(pos_x, pos_y)
        elif (rad > math.pi and rad <= math.pi / 2 * 3) or (rad <= -1 * math.pi / 2):
            pos_x = start_pos.x - \
                distance * abs(math.cos(rad))
            pos_y = start_pos.y + \
                distance * abs(math.sin(rad))
            return Point(pos_x, pos_y)
        elif (rad >= -1 * math.pi / 2 and rad <= 0) or (rad > math.pi / 2 * 3 and rad <= math.pi * 2):
            pos_x = start_pos.x + \
                distance * abs(math.cos(rad))
            pos_y = start_pos.y + \
                distance * abs(math.sin(rad))
            return Point(pos_x, pos_y)
        else:
            print(rad)
            raise Exception("Check Rad Failed")

    def __isEnemyNear(self, minimap_frame) -> bool:
        hsv_minimap_frame = cv2.cvtColor(minimap_frame, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 180, 180])
        upper_red = np.array([10, 255, 255])
        mask = cv2.inRange(hsv_minimap_frame, lower_red, upper_red)
        if cv2.countNonZero(mask) > 10:
            return True
        return False

    def __calllOut(self):
        calloutLst = ["b", "c", "x", "z"]
        callout = random.choice(list(calloutLst))
        KBPress(callout).start()

    def __carJack(self):
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
