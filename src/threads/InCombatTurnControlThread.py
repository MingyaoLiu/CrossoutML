
import Constants as const
from threading import Thread
import time
import InputControl
import math
import cv2
from SettingsClass import getGlobalSetting
#
# Thread for controling the vehicle during battle.
# This thread will be blocking due to the nature of keyboard control.
#
class InCombatVehicleTurnControlThread(Thread):
    def __init__(self, mask):
        Thread.__init__(self)
        self.isRunning = True
        
        self.showMapTrackingDebug = getGlobalSetting().settings.showMapTrackingDebugWindow
        self.holdDuration = getGlobalSetting().settings.turnHoldDuration
        self.afterWait = getGlobalSetting().settings.turnAfterWaitDuration
        self.mask = mask
        self.debugMask = self.mask.copy()
        self.currentlyMakingATurn = 'no' # no / left / right
        self.detect_angle_rad = math.radians(getGlobalSetting().settings.frontDetectDegree)
        self.center_mid_distance = getGlobalSetting().settings.centerDetectDistance
        self.lr_low_detect_distance = getGlobalSetting().settings.lrDetectDistance

        print("In Combat Turn Control Exit")

    def run(self):

        while self.isRunning:
            movements = const.getVehicleMovementStack()
            if len(movements) > 0:
                self.__applyMovement(movements)

        time.sleep(0.15)
        InputControl.kbUp("a")
        InputControl.kbUp("s")
        InputControl.kbUp("d")
        if self.showMapTrackingDebug:
            cv2.destroyWindow("MaskMap")
        print("In Combat Turn Control Exit")

    def __applyMovement(self, datas: [const.VehicleMovementData]):

        data = datas[0]
        center_rad = data.rad
        current_pos = data.pos
        
        
        center_mid_dist_pos = self.__calcEndPoint( current_pos, center_rad, self.center_mid_distance)
        center_mid_pd = const.PointData(
            center_mid_dist_pos, self.__calcTooClose(center_mid_dist_pos))

        left_rad = center_rad + self.detect_angle_rad
        left_low_dist = self.__calcEndPoint(current_pos, left_rad, self.lr_low_detect_distance)
        left_low_pd = const.PointData(left_low_dist, self.__calcTooClose(left_low_dist))

        right_rad = center_rad - self.detect_angle_rad
        right_low_dist = self.__calcEndPoint(current_pos, right_rad, self.lr_low_detect_distance)
        right_low_pd = const.PointData(right_low_dist, self.__calcTooClose(right_low_dist))
        
        if self.showMapTrackingDebug:
            debugShowMap = self.debugMask.copy()
            cv2.circle(debugShowMap, (int(current_pos.x),
                                                int(current_pos.y)), 1, (0, 0, 255), 2)
            cv2.line(debugShowMap,
                            (int(current_pos.x),
                            int(current_pos.y)), (int(center_mid_dist_pos.x), int(center_mid_dist_pos.y)), (255, 0, 0), 2)
            cv2.line(debugShowMap,
                            (int(current_pos.x),
                            int(current_pos.y)), (int(left_low_pd.pos.x), int(left_low_pd.pos.y)), (255, 0, 0), 1)
            cv2.line(debugShowMap,
                            (int(current_pos.x),
                            int(current_pos.y)), (int(right_low_pd.pos.x), int(right_low_pd.pos.y)), (255, 0, 0), 1)
            cv2.imshow("MaskMap", debugShowMap)
            cv2.waitKey(1)


        if center_mid_pd.isOutside: # center mid is outside
                
            if left_low_pd.isOutside and right_low_pd.isOutside: # both left and right are outside
                if center_mid_pd.isOutside: # THIS WAS SET TO LOW
                    pass
                else:
                    if (self.currentlyMakingATurn == 'left'):
                        InputControl.kbDown("a")
                    elif (self.currentlyMakingATurn == 'right'):
                        InputControl.kbDown("d")

            elif left_low_pd.isOutside:
                self.currentlyMakingATurn = 'right'

                InputControl.kbDown("d")

            elif right_low_pd.isOutside:
                self.currentlyMakingATurn = 'left'
                
                InputControl.kbDown("a")
            else:
                self.currentlyMakingATurn = 'no'
        else:
            pass
        
        time.sleep(self.holdDuration)
        InputControl.kbUp("a")
        InputControl.kbUp("s")
        InputControl.kbUp("d")
        time.sleep(self.afterWait)

    # calculate distance between 2 points.
    def __calcDistance(self, pos1: const.Point, pos2: const.Point) -> float:
        if (pos1 == pos2):
            return 0
        return math.sqrt((pos1.x - pos2.x) * (pos1.x - pos2.x) + (pos1.y - pos2.y) * (pos1.y - pos2.y))

    # check if a point is on white / black on mask
    def __calcTooClose(self, pos: const.Point) -> bool:
        # cv2 coordinate is Reversed Here
        return False if self.mask[int(pos.y), int(pos.x)] == 0 else True
    
    # Calculate the detection point based on distance and rad.
    def __calcEndPoint(self, pos: const.Point, rad: float, distance: float) -> const.Point:
        pos_x = pos.x + distance * math.cos(rad)
        pos_y = pos.y - distance * math.sin(rad)
        return const.Point(pos_x, pos_y)
