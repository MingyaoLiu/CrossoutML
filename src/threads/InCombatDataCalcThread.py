

import Constants as const
from Constants import Point
from threading import Thread
import time
import InputControl
import math
import cv2
from Utils import imgRotate, getCorrectPos
from DCaptureClass import getDCapture

#
# Thread for calculating speed, position, etc, in battle.
# This thread should be semi blocking due to ML image recognition, but generally non blocking.
#
class InCombatVehicleDataCalculationThread(Thread):
    def __init__(self, thisMap):
        Thread.__init__(self)
        self.isRunning = True
        self.thisMap = thisMap
        InputControl.mouseClick(getCorrectPos(Point(10, 10)))
        const.clearVehicleMovementStack()
        print("In Combat Data Calculation Thread Init")

    def run(self):

        while self.isRunning:

            frame = getDCapture().getFrame(0)
            thisMinimap = frame[const.BattleMiniMapArea.y:const.BattleMiniMapArea.ys, const.BattleMiniMapArea.x:const.BattleMiniMapArea.xs]
            # cv2.imwrite("mini.jpg", thisMinimap ) 
            pos = self.__getMiniMapReadLoc(self.thisMap, thisMinimap)
            if (pos):
                updateMap = cv2.circle(self.thisMap, (int(pos.x), int(pos.y)), 1, (0, 0, 255), 2)

            minimap_arrow_frame = frame[const.BattleMiniMapCenter.y - 15:const.BattleMiniMapCenter.y + 15, const.BattleMiniMapCenter.x - 15: const.BattleMiniMapCenter.x + 15] 
            # minimap_arrow_frame2 = frame[847:869, 1688: 1710] 
            # cv2.imshow("MiniArrow", minimap_arrow_frame2)
            center_rad = self.__calcRadWithContour(minimap_arrow_frame)
            if ((center_rad is not None) and (center_rad != 0)):
                cv2.putText(updateMap, str(center_rad * 180 / math.pi), (50, 50) , cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0) , 1, cv2.LINE_AA) 


            if (pos and center_rad):
                vehicleData = const.VehicleMovementData(time.time(), pos, center_rad)
                const.updateVehicleMovementStack(vehicleData)

        print("In Combat Data Calculation Thread Exit")




    def __getMiniMapReadLoc(self, src_map, minimap_frame) -> Point:
        new_width = int(minimap_frame.shape[1] * 1.0375) # For minimap at 2 scale and large, the map is 1.0375 larger in scale than minimap for some reason.
        new_height = int(minimap_frame.shape[0] * 1.0375)
        minimap_frame = cv2.resize(minimap_frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
        method = eval('cv2.TM_CCOEFF')
        res = cv2.matchTemplate(src_map, minimap_frame, method)
        _, _, min_loc, max_loc = cv2.minMaxLoc(res)
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        circle_center_x = top_left[0] + new_width / 2
        circle_center_y = top_left[1] + new_height / 2
        return Point(math.floor(circle_center_x), math.floor(circle_center_y))




    def __calcRadWithContour(self, minimap_arrow_frame) -> float:
        img = cv2.cvtColor(minimap_arrow_frame, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(img, 195, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_NONE )
        if len(contours) == 1:
            cnt = contours[0]
            [vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01)
            rad = math.atan(vy / vx)
            # - - | + -
            # ——————————
            # - + | + +
            img2 = img.copy()
            ret2, thresh2 = cv2.threshold(img2, 230, 255, cv2.THRESH_BINARY)
            cv2.drawContours(thresh2, [cnt], 0, (0,255,0), 1)
            cv2.fillPoly(thresh2, pts =[cnt], color=(255,255,255))

            newImg = imgRotate(thresh2, 90 - (rad * -180 / math.pi))
            upperImg = newImg[0:14,0:30]
            lowerImg = newImg[16:30,0:30]

            # sideBySideArrow = np.hstack((upperImg, lowerImg))
            # cv2.imshow("MiniArrow2", sideBySideArrow)

            if cv2.countNonZero(upperImg) < cv2.countNonZero(lowerImg):
                # print("Going through 1 and 4 Quadrant")
                return -1 * rad
            else:
                # print("going through 2, 3 quadrant")
                return math.pi + -1 * rad
        else:
            # print("CONTOUR IS Not 1")
            pass
        return None

