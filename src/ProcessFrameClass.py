
from multiprocessing import Process, Value
import time
from DCaptureClass import getDCapture
import pytesseract
from Constants import Area, Point, findStepById, Step, loadNewUser, Action, getPassword, getUsername, getRunningStepId, setRunningStepId
import Constants as const
import d3dshot

from Utils import getCorrectPos
from threading import Thread
import cv2
import InputControl
import math
from Utils import imgRotate
import numpy as np

#
# Thread for showing debug info in a cv2 window. 
# This thread is non blocking.
#
class DebugThread(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        self.isRunning = True
        self.mouseClickPos = None

    def monitorImageClick(self, event, x, y, p1, p2):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouseClickPos = 'x: ' + str(x) + ' y: ' + str(y)

    def run(self):
        while self.isRunning:
            np_frame = getDCapture().getFrame(0)
            thisStep = const.findStepById(getRunningStepId())
            if (thisStep.area):
                np_frame = cv2.rectangle(np_frame, (thisStep.area.x, thisStep.area.y), (thisStep.area.xs, thisStep.area.ys), (0,255,0), 5) 
            if (thisStep.point):
                np_frame = cv2.circle(np_frame, (thisStep.point.x, thisStep.point.y), radius=5, color=(0, 0, 255), thickness=-1)
            if (self.mouseClickPos):
                np_frame = cv2.putText(np_frame, self.mouseClickPos, (50, 50) , cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0) , 2, cv2.LINE_AA) 
            # enlargedFrameSize = (960, 540) # Choose the top left corner of the inner window.
            # resizedFrame = cv2.resize(np_frame, enlargedFrameSize, interpolation = cv2.INTER_AREA)
            # cv2.imshow("Capture" + self.name, resizedFrame)
            cv2.imshow("Capture" + self.name, np_frame)
            cv2.setMouseCallback("Capture" + self.name, self.monitorImageClick)
            cv2.waitKey(1)

import random

#
# Thread for deciding which step it is at and execute detection accordingly. 
# This thread is blocking.
#
class DetectClickThread(Thread):


    def __init__(self):
        Thread.__init__(self)

        self.disableProcessing = False
        # self.disableProcessing = True # For debug
        self.isRunning = True
        self.isProcessingFrameIndication = False
        self.retryCount = 0
        self.battleVehicleCalcThread = None
        self.battleControlThread = None
        self.weaponFirethread = None
        self.thisMap = None
        self.thisMask = None
        self.thisMapName = '' # this is used to save the filename with map name

        self.lastLoginTime = time.time()

        InputControl.mouseClick(getCorrectPos(Point(10, 10)))


    def run(self):
        while self.isRunning:
            if (self.isProcessingFrameIndication == False and self.disableProcessing == False):
                frame = getDCapture().getFrame(0)
                self.isProcessingFrameIndication = True
                step = findStepById(getRunningStepId())
                if (getRunningStepId() == 'in_game_map_name_label'):
                    InputControl.kbUp('tab')
                    time.sleep(1)
                    InputControl.kbDown('tab')
                    time.sleep(2)
                isSuccess = self.processThisFrame(frame, step, isFirst = self.retryCount == 0, randomizeData = self.retryCount > 5)
                
                
                if (isSuccess):
                    self.retryCount = 0
                    if (getRunningStepId() == 'in_game_map_name_label'): # update map frame for in battle use
                        self.thisMap = frame[const.BattleFullMap.y:const.BattleFullMap.ys, const.BattleFullMap.x:const.BattleFullMap.xs]
                        cv2.imwrite("map-" + str(self.thisMapName) + "-fullmap-" + str(time.time()) + ".jpg", self.thisMap ) 
                    self.goToNextStep(isSuccess)
                else:
                    self.retryCount += 1
                    if (self.retryCount > 20):
                        self.retryCount = 0
                        self.goToNextStep(isSuccess)
                self.isProcessingFrameIndication = False

        if (self.battleVehicleCalcThread):
            self.battleVehicleCalcThread.isRunning = False
            self.battleVehicleCalcThread = None
        if (self.battleControlThread):
            self.battleControlThread.isRunning = False
            self.battleControlThread = None


    def processThisFrame(self, frame, step: Step, isFirst: bool, randomizeData: bool) -> bool:
        if (step.waitBefore > 0 and isFirst == True): # wait before timer will not trigger for subsequential retries.
            time.sleep(step.waitBefore)
        if (step.action == Action.textDetect):
            textMatch = None

            if (randomizeData == True):
                pixelMoveAround = [3,2,1,0,-1,-2,-3]
                randomizedArea = Area(
                    step.area.x + random.choice(pixelMoveAround),
                    step.area.y + random.choice(pixelMoveAround),
                    step.area.xs + random.choice(pixelMoveAround),
                    step.area.ys + random.choice(pixelMoveAround),
                )
                print('using randomized area:')
                print(randomizedArea)
                textMatch = self.__checkTextDetectionMatchString(frame, randomizedArea, step.strings)

            else:
                textMatch = self.__checkTextDetectionMatchString(frame, step.area, step.strings)

            if (textMatch is None):
                return False
            
            if (getRunningStepId() == 'in_game_map_name_label'):
                self.thisMapName = textMatch
                self.thisMask = cv2.imread( const.map_mask_file_path[textMatch], 0)


                        

            print("text detection executed")

        elif (step.action == Action.mouseClick):
            InputControl.mouseClick(getCorrectPos(step.point))
            time.sleep(0.01)
            InputControl.setMousePos(getCorrectPos(Point(10,10)))
            print("Mouse Click Action executed")

        elif (step.action == Action.textInput):
            if getRunningStepId() == 'login_username_input':
                InputControl.fillInputWithString(const.getUsername())
            elif getRunningStepId() == 'login_password_input':
                InputControl.fillInputWithString(const.getPassword())
            else:
                InputControl.fillInputWithString(random.choice(step.strings))
            print("text input executed")

        if (step.waitAfter > 0):
            time.sleep(step.waitAfter)
        return True

    def __checkTextDetectionMatchString(self, frame, area: Area, expStrs: [str]) -> str:
        crop_frame = frame[area.y:area.ys, area.x:area.xs]
        txt = pytesseract.image_to_string(crop_frame, lang='eng').lower()
        print(txt)
        for string in expStrs:
            if ((txt in string) or (string in txt)):
                print('text detection matched')
                return string
        print('text match failed')
        return None

    def goToNextStep(self, thisStepResult: bool):
        step = getRunningStepId()
        print('current step is ' + step)
        
        if step == 'login_disconnect_btn_text':
            setRunningStepId('login_disconnect_click')
        elif step == 'login_disconnect_click':
            setRunningStepId('login_button')
        elif step == 'login_button':
            if thisStepResult == True:
                setRunningStepId('login_username_click')
            else:
                setRunningStepId('login_button_steam')
        elif step == 'login_button_steam':
            if thisStepResult == True:
                setRunningStepId('login_username_click')
            else:
                setRunningStepId('login_btn_click')


        elif step == 'login_username_click':
            setRunningStepId('login_username_input')
        elif step == 'login_username_input':
            setRunningStepId('login_password_click')
        elif step == 'login_password_click':
            setRunningStepId('login_password_input')
        elif step == 'login_password_input':
            setRunningStepId('login_btn_click')
        elif step == 'login_btn_click':
            setRunningStepId('login_btn_steam_click')
        elif step == 'login_btn_steam_click':
                        
            self.lastLoginTime = time.time()
            InputControl.kbDown('esc')
            time.sleep(0.01)
            InputControl.kbUp('esc')
            time.sleep(0.5)
            InputControl.kbDown('esc')
            time.sleep(0.01)
            InputControl.kbUp('esc')
            time.sleep(0.5)
            InputControl.kbDown('esc')
            time.sleep(0.01)
            InputControl.kbUp('esc')
            time.sleep(0.5)
            InputControl.kbDown('esc')
            time.sleep(0.01)
            InputControl.kbUp('esc')
            time.sleep(0.5)
            InputControl.kbDown('esc')
            time.sleep(0.01)
            InputControl.kbUp('esc')
            time.sleep(0.5)
            setRunningStepId('mainmenu_esc_return_btn_label')

        elif step == 'mainmenu_esc_return_btn_label':
            if thisStepResult == True:
                

                if (time.time() - self.lastLoginTime > 3600):
                    const.loadNewUser()
                    setRunningStepId('mainmenu_esc_titlescreen_btn_click')
                else:
                    InputControl.kbDown('esc')
                    time.sleep(0.01)
                    InputControl.kbUp('esc')
                    time.sleep(0.5)
            
        
            if (time.time() - self.lastLoginTime > 3600):
                const.loadNewUser()
                InputControl.kbDown('esc')
                time.sleep(0.01)
                InputControl.kbUp('esc')
                time.sleep(0.5)
                setRunningStepId('mainmenu_esc_titlescreen_btn_click')
            else:
                InputControl.mouseClick(getCorrectPos(Point(120,41)) )
                setRunningStepId('mainmenu_battle_label')

        elif step == 'mainmenu_esc_titlescreen_btn_click':
            setRunningStepId('mainmenu_esc_titlescreen_confirm_btn_click')

        elif step == 'mainmenu_esc_titlescreen_confirm_btn_click':
            setRunningStepId('login_username_click')
        
        elif step == 'mainmenu_battle_label':
            if thisStepResult == True:
                setRunningStepId('mainmenu_select_click')

        elif step == 'mainmenu_select_click':
            modes = ['battle_select_scrap_click', 'battle_select_battery_click', 'battle_select_wire_click']
            setRunningStepId(random.choice(modes))
        
        elif (step == 'battle_select_scrap_click' or step == 'battle_select_battery_click' or step == 'battle_select_wire_click'):
            setRunningStepId('battle_select_battle_start_click')
        
        elif step == 'battle_select_battle_start_click':
                setRunningStepId('before_game_wait')


        elif step == 'before_game_wait':
                setRunningStepId('in_game_map_name_label')

        elif step == 'in_game_map_name_label':
            if thisStepResult == True:
                
                InputControl.kbUp('tab')
                time.sleep(10)

                frame = getDCapture().getFrame(0)
                minimap = frame[const.BattleMiniMapArea.y:const.BattleMiniMapArea.ys, const.BattleMiniMapArea.x:const.BattleMiniMapArea.xs]
                cv2.imwrite("map-" + str(self.thisMapName) + "-minimap-" + str(time.time()) + ".jpg", minimap ) 
                        
                self.battleVehicleCalcThread = InCombatVehicleDataCalculationThread(self.thisMap)
                self.battleVehicleCalcThread.start()

                self.battleControlThread = InCombatVehicleControlThread(self.thisMask)
                self.battleControlThread.start()

                self.weaponFirethread = InCombatDeployWeaponThread()
                self.weaponFirethread.start()
                
                setRunningStepId('in_game_wait_for_finish')
            else: # If no battle close button has  been detected, go back to wait for 30 seconds.
                setRunningStepId('before_game_wait')


        elif step == "in_game_wait_for_finish":
            setRunningStepId('finish_battle_close_btn_label')
        
        elif step == 'finish_battle_close_btn_label':
            if thisStepResult == True:
                
                InputControl.kbUp("a")
                InputControl.kbUp("s")
                InputControl.kbUp("d")
                InputControl.kbUp("w")
                InputControl.kbUp("spacebar")
                time.sleep(0.01)
                if self.battleVehicleCalcThread:
                    self.battleVehicleCalcThread.isRunning = False
                    self.battleVehicleCalcThread = None
                if self.battleControlThread:
                    self.battleControlThread.isRunning = False
                    self.battleControlThread = None
                if self.weaponFirethread:
                    self.weaponFirethread.isRunning = False
                    self.weaponFirethread = None
                self.thisMap = None
                self.thisMask = None

                setRunningStepId('finish_battle_close_btn_click')
            else: # If no battle close button has  been detected, go back to wait for 30 seconds.
                setRunningStepId('in_game_wait_for_finish')

        elif step == "finish_battle_close_btn_click":
            InputControl.kbDown('esc')
            time.sleep(0.01)
            InputControl.kbUp('esc')
            time.sleep(0.5)
            InputControl.kbDown('esc')
            time.sleep(0.01)
            InputControl.kbUp('esc')
            time.sleep(0.5)
            InputControl.kbDown('esc')
            time.sleep(0.01)
            InputControl.kbUp('esc')
            time.sleep(0.5)
            InputControl.kbDown('esc')
            time.sleep(0.01)
            InputControl.kbUp('esc')
            time.sleep(0.5)
            InputControl.kbDown('esc')
            time.sleep(0.01)
            InputControl.kbUp('esc')
            time.sleep(0.5)
            setRunningStepId('mainmenu_esc_return_btn_label')
        


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


class InCombatDeployWeaponThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.isRunning = True
        self.lastPulledOut = time.time()
        self.stuckTimer = None

    def run(self):
        while self.isRunning:
            frame = getDCapture().getFrame(0)
            thisMinimap = frame[const.BattleMiniMapArea.y + 20:const.BattleMiniMapArea.ys - 20, const.BattleMiniMapArea.x + 20:const.BattleMiniMapArea.xs - 20]
            if (self.__isEnemyNear(thisMinimap) and (time.time() - self.lastPulledOut > 5)):
            # if self.__isEnemyNear(thisMinimap):
                print("shoot")
                self.lastPulledOut = time.time()
                InputControl.kbDown('1')
                time.sleep(0.2)
                InputControl.kbUp('1')
                time.sleep(1)

            movementStack = const.getVehicleMovementStack()
            if len(movementStack) == 50:
                if ((movementStack[0].pos.x == movementStack[49].pos.x) and (movementStack[0].pos.y == movementStack[49].pos.y)):
                    if (self.stuckTimer is None):
                        self.stuckTimer = movementStack[0].time
                    elif (movementStack[0].time - self.stuckTimer > 10):
                        InputControl.kbDown('backspace')
                        time.sleep(5)
                        InputControl.kbUp('backspace')
                        self.isRunning = False
                    
                else:
                    self.stuckTimer = None



    def __isEnemyNear(self, minimap_frame) -> bool:
        hsv_minimap_frame = cv2.cvtColor(minimap_frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_minimap_frame, (100, 200, 100), (120, 255, 255))
        if cv2.countNonZero(mask) > 10:
            return True
        return False


#
# Thread for controling the vehicle during battle.
# This thread will be blocking due to the nature of keyboard control.
#
class InCombatVehicleControlThread(Thread):
    def __init__(self, mask):
        Thread.__init__(self)
        self.isRunning = True
        self.mask = mask
        self.debugMask = self.mask.copy()
        self.currentlyMakingATurn = 'no' # no / left / right

    def run(self):

        while self.isRunning:
            movements = const.getVehicleMovementStack()
            if len(movements) > 0:
                self.__applyMovement(movements)


        
            cv2.waitKey(1)
        cv2.destroyWindow("MaskMap")

    def __applyMovement(self, datas: [const.VehicleMovementData]):

        data = datas[0]
        center_rad = data.rad
        current_pos = data.pos
        
        detect_angle_rad = math.radians(30)
        lr_low_detect_distance = 15
        lr_mid_detect_distance = 50
        center_low_distance = 15
        center_mid_distance = 40
        center_far_distance = 60 # not used

        speed = 0
        if len(datas) > 10:
            lastData = datas[10]
            pixel_distance = self.__calcDistance(lastData.pos, current_pos)
            speed = pixel_distance / (time.time() - lastData.time) * 5 # speed may need multiplier to be more accurate

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
                          int(current_pos.y)), (int(center_far_dist_pos.x), int(center_far_dist_pos.y)), (255, 0, 0), 2)
        cv2.line(debugShowMap,
                         (int(current_pos.x),
                          int(current_pos.y)), (int(left_low_pd.pos.x), int(left_low_pd.pos.y)), (255, 0, 0), 1)
        cv2.line(debugShowMap,
                         (int(current_pos.x),
                          int(current_pos.y)), (int(right_low_pd.pos.x), int(right_low_pd.pos.y)), (255, 0, 0), 1)

        cv2.imshow("MaskMap", debugShowMap)

        # Calculation Done


        if speed > 60:
            InputControl.kbUp("w")
            InputControl.kbDown("spacebar")
        elif speed > 40:
            InputControl.kbUp("spacebar")
            InputControl.kbUp("w")
        elif speed < 20:
            InputControl.kbUp("spacebar")
            InputControl.kbDown("w")
        else:
            InputControl.kbUp("w")
            InputControl.kbUp("spacebar")



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
        
        time.sleep(0.15)
        InputControl.kbUp("w")
        InputControl.kbUp("a")
        InputControl.kbUp("s")
        InputControl.kbUp("d")
        InputControl.kbUp("spacebar")
        time.sleep(0.2)


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


    def __calcDistance(self, pos1: Point, pos2: Point) -> float:
        if (pos1 == pos2):
            return 0
        return math.sqrt((pos1.x - pos2.x) * (pos1.x - pos2.x) + (pos1.y - pos2.y) * (pos1.y - pos2.y))


    # check if a point is on white / black on mask
    def __calcTooClose(self, pos: Point) -> bool:
        # Coordinate is Reversed Here
        return False if self.mask[int(pos.y), int(pos.x)] == 0 else True
    
    # Calculate the detection point.
    def __calcEndPoint(self, pos: Point, rad: float, distance: float) -> Point:
        pos_x = pos.x + distance * math.cos(rad)
        pos_y = pos.y - distance * math.sin(rad)
        return Point(pos_x, pos_y)
