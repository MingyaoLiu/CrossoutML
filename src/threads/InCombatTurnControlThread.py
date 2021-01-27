
import Constants as const
from threading import Thread
import time
import InputControl
import math
import cv2
#
# Thread for controling the vehicle during battle.
# This thread will be blocking due to the nature of keyboard control.
#
class InCombatVehicleTurnControlThread(Thread):
    def __init__(self, mask):
        Thread.__init__(self)
        self.isRunning = True
        self.mask = mask
        self.debugMask = self.mask.copy()
        self.currentlyMakingATurn = 'no' # no / left / right
        print("In Combat Turn Control Exit")

    def run(self):

        while self.isRunning:
            movements = const.getVehicleMovementStack()
            if len(movements) > 0:
                self.__applyMovement(movements)


        
            cv2.waitKey(1)
        time.sleep(0.15)
        InputControl.kbUp("a")
        InputControl.kbUp("s")
        InputControl.kbUp("d")
        cv2.destroyWindow("MaskMap")
        print("In Combat Turn Control Exit")

    def __applyMovement(self, datas: [const.VehicleMovementData]):

        data = datas[0]
        center_rad = data.rad
        current_pos = data.pos
        
        detect_angle_rad = math.radians(35)
        lr_low_detect_distance = 20
        lr_mid_detect_distance = 50
        center_low_distance = 25
        center_mid_distance = 40
        center_far_distance = 60 # not used

        left_rad = center_rad + detect_angle_rad
        right_rad = center_rad - detect_angle_rad
        pos_data = const.PointData(current_pos, self.__calcTooClose(current_pos))
        center_low_dist_pos = self.__calcEndPoint( current_pos, center_rad, center_low_distance)
        center_mid_dist_pos = self.__calcEndPoint( current_pos, center_rad, center_mid_distance)
        center_far_dist_pos = self.__calcEndPoint( current_pos, center_rad, center_far_distance)

        left_mid_dist = self.__calcEndPoint(
            current_pos, left_rad, lr_mid_detect_distance)
        right_mid_dist = self.__calcEndPoint(
            current_pos, right_rad, lr_mid_detect_distance)
        left_low_dist = self.__calcEndPoint(
            current_pos, left_rad, lr_low_detect_distance)
        right_low_dist = self.__calcEndPoint(
            current_pos, right_rad, lr_low_detect_distance)


        center_low_pd = const.PointData(
            center_low_dist_pos, self.__calcTooClose(center_low_dist_pos))
        center_mid_pd = const.PointData(
            center_mid_dist_pos, self.__calcTooClose(center_mid_dist_pos))
        center_far_pd = const.PointData(
            center_far_dist_pos, self.__calcTooClose(center_far_dist_pos))

        center_data = const.CenterData(center_low_pd, center_mid_pd, center_far_pd)

        left_low_pd = const.PointData(
            left_low_dist, self.__calcTooClose(left_low_dist))
        right_low_pd = const.PointData(
            right_low_dist, self.__calcTooClose(right_low_dist))
        
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

        # Calculation Done

        if center_data.mid.isOutside: # center mid is outside
                
            if left_low_pd.isOutside and right_low_pd.isOutside: # both left and right are outside

                if center_data.low.isOutside:
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
        
        time.sleep(0.12)
        InputControl.kbUp("a")
        InputControl.kbUp("s")
        InputControl.kbUp("d")
        time.sleep(0.25)


        # if center_data.far.isOutside or center_data.mid.isOutside or center_data.low.isOutside or left_low_pd.isOutside or right_low_pd.isOutside:

            
        #     InputControl.kbUp("a")
        #     InputControl.kbUp("s")
        #     InputControl.kbUp("d")

        #     time.sleep(0.05)

            # if center_data.far.isOutside:
            #     if center_data.mid.isOutside or center_data.low.isOutside: # currently consider low mid to be same detection algorithm
                    
            #         if left_low_pd.isOutside and right_low_pd.isOutside: # there is no save for this now

            #             if current_pos.x < 376 and current_pos.y < 376: # 2
            #                 if (center_rad * 180 / math.pi) > -45 and (center_rad * 180 / math.pi) < 135:
            #                     InputControl.kbDown("d")
            #                 else:
            #                     InputControl.kbDown("a")

            #             elif current_pos.x >= 376 and current_pos.y < 376: # 1
            #                 if (center_rad * 180 / math.pi) > 45 and (center_rad * 180 / math.pi) < 225:
            #                     InputControl.kbDown("a")
            #                 else:
            #                     InputControl.kbDown("d")
            #             elif current_pos.x >= 376 and current_pos.y >= 376: # 4
            #                 if (center_rad * 180 / math.pi) > -45 and (center_rad * 180 / math.pi) < 135:
            #                     InputControl.kbDown("a")
            #                 else:
            #                     InputControl.kbDown("d")
            #             elif current_pos.x < 376 and current_pos.y >= 376: # 3

            #                 if (center_rad * 180 / math.pi) > 45 and (center_rad * 180 / math.pi) < 225:
            #                     InputControl.kbDown("d")
            #                 else:
            #                     InputControl.kbDown("a")
            #             else:
            #                 InputControl.kbDown("d")
            #         elif left_low_pd.isOutside:

            #             InputControl.kbDown("d")
            #         elif right_low_pd.isOutside:

            #             InputControl.kbDown("a")
            #         else: # choose a diretion to turn.
            #             pass
            #             # if current_pos.x < 376 and current_pos.y < 376: # 2
            #             #     if (center_rad * 180 / math.pi) > -45 and (center_rad * 180 / math.pi) < 135:
            #             #         InputControl.kbDown("d")
            #             #     else:
            #             #         InputControl.kbDown("a")

            #             # elif current_pos.x >= 376 and current_pos.y < 376: # 1
            #             #     if (center_rad * 180 / math.pi) > 45 and (center_rad * 180 / math.pi) < 225:
            #             #         InputControl.kbDown("a")
            #             #     else:
            #             #         InputControl.kbDown("d")
            #             # elif current_pos.x >= 376 and current_pos.y >= 376: # 4
            #             #     if (center_rad * 180 / math.pi) > -45 and (center_rad * 180 / math.pi) < 135:
            #             #         InputControl.kbDown("a")
            #             #     else:
            #             #         InputControl.kbDown("d")
            #             # elif current_pos.x < 376 and current_pos.y >= 376: # 3

            #             #     if (center_rad * 180 / math.pi) > 45 and (center_rad * 180 / math.pi) < 225:
            #             #         InputControl.kbDown("d")
            #             #     else:
            #             #         InputControl.kbDown("a")
            #             # else:
            #             #     InputControl.kbDown("d")
            #             # InputControl.kbDown("spacebar")

            #     else: # this means close up its still pretty far, don't need to slow down.
            #         pass



            #             # if current_pos.x < 376 and current_pos.y < 376: # 2
            #             #     if (center_rad * 180 / math.pi) > -45 and (center_rad * 180 / math.pi) < 135:
            #             #         InputControl.kbDown("d")
            #             #     else:
            #             #         InputControl.kbDown("a")

            #             # elif current_pos.x >= 376 and current_pos.y < 376: # 1
            #             #     if (center_rad * 180 / math.pi) > 45 and (center_rad * 180 / math.pi) < 225:
            #             #         InputControl.kbDown("a")
            #             #     else:
            #             #         InputControl.kbDown("d")
            #             # elif current_pos.x >= 376 and current_pos.y >= 376: # 4
            #             #     if (center_rad * 180 / math.pi) > -45 and (center_rad * 180 / math.pi) < 135:
            #             #         InputControl.kbDown("a")
            #             #     else:
            #             #         InputControl.kbDown("d")
            #             # elif current_pos.x < 376 and current_pos.y >= 376: # 3

            #             #     if (center_rad * 180 / math.pi) > 45 and (center_rad * 180 / math.pi) < 225:
            #             #         InputControl.kbDown("d")
            #             #     else:
            #             #         InputControl.kbDown("a")
            #             # else:
            #             #     InputControl.kbDown("d")
            
        #     else:
        #         pass

        #     time.sleep(0.1)
        # else:
        #     InputControl.kbUp("a")
        #     InputControl.kbUp("s")
        #     InputControl.kbUp("d")

        #     time.sleep(0.1)


    def __calcDistance(self, pos1: const.Point, pos2: const.Point) -> float:
        if (pos1 == pos2):
            return 0
        return math.sqrt((pos1.x - pos2.x) * (pos1.x - pos2.x) + (pos1.y - pos2.y) * (pos1.y - pos2.y))


    # check if a point is on white / black on mask
    def __calcTooClose(self, pos: const.Point) -> bool:
        # Coordinate is Reversed Here
        return False if self.mask[int(pos.y), int(pos.x)] == 0 else True
    
    # Calculate the detection point.
    def __calcEndPoint(self, pos: const.Point, rad: float, distance: float) -> const.Point:
        pos_x = pos.x + distance * math.cos(rad)
        pos_y = pos.y - distance * math.sin(rad)
        return const.Point(pos_x, pos_y)
