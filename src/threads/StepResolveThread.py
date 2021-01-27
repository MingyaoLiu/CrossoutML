
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
import random
from threads.InCombatSpeedControlThread import InCombatVehicleSpeedControlThread
from threads.InCombatTurnControlThread import InCombatVehicleTurnControlThread
from threads.InCombatDeployWeaponThread import InCombatDeployWeaponThread
from threads.InCombatDataCalcThread import InCombatVehicleDataCalculationThread


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
        self.speedControlThread = None
        self.turnControlThread = None
        self.weaponFirethread = None
        self.thisMap = None
        self.thisMask = None
        self.thisMapName = '' # this is used to save the filename with map name

        self.lastLoginTime = time.time()

        InputControl.mouseClick(getCorrectPos(Point(10, 10)))
        print("Step Resolve Thread Init")


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

        self.terminateAllThreads()
        print("Step Resolve Thread Exit")

    def terminateAllThreads(self):
        if (self.battleVehicleCalcThread):
            self.battleVehicleCalcThread.isRunning = False
            self.battleVehicleCalcThread.join()
            self.battleVehicleCalcThread = None
        if (self.turnControlThread):
            self.turnControlThread.isRunning = False
            self.turnControlThread.join()
            self.turnControlThread = None
        if (self.speedControlThread):
            self.speedControlThread.isRunning = False
            self.speedControlThread.join()
            self.speedControlThread = None
        if (self.weaponFirethread):
            self.weaponFirethread.isRunning = False
            self.weaponFirethread.join()
            self.weaponFirethread = None

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

                # frame = getDCapture().getFrame(0)
                # minimap = frame[const.BattleMiniMapArea.y:const.BattleMiniMapArea.ys, const.BattleMiniMapArea.x:const.BattleMiniMapArea.xs]
                # cv2.imwrite("map-" + str(self.thisMapName) + "-minimap-" + str(time.time()) + ".jpg", minimap ) 

                self.battleVehicleCalcThread = InCombatVehicleDataCalculationThread(self.thisMap)
                self.battleVehicleCalcThread.start()
                self.turnControlThread = InCombatVehicleTurnControlThread(self.thisMask)
                self.turnControlThread.start()
                self.speedControlThread = InCombatVehicleSpeedControlThread()
                self.speedControlThread.start()
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
                self.terminateAllThreads()
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
        
