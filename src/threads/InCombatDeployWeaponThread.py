
import cv2
from threading import Thread
import Constants as const
from DCaptureClass import getDCapture
import time
import InputControl
import random
from SettingsClass import getGlobalSetting, setRunningStepId

class InCombatDeployWeaponThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.parentThread = None
        self.enemyDetectSizeModifier = getGlobalSetting().settings.enemyDetectionSizeMidifier # negative
        self.weaponKey = getGlobalSetting().settings.weaponKey
        self.selfExplodeKey = getGlobalSetting().settings.selfExplodeKey
        self.calloutKeys = getGlobalSetting().settings.calloutKeys.split(',')
        self.isRunning = True
        self.lastPulledOut = time.time()
        self.lastFlipTime = time.time()
        self.stuckTimer = None
        self.alreadyExplode = False
        self.doRandomCallout = False
        self.initTime = time.time()
        print("Weapon Deploy Thread Init")

    def run(self):
        while self.isRunning:
            
            currentTime = time.time()

            # Deploy weapon
            frame = getDCapture().getFrame(0)
            thisSmallerMinimap = frame[const.BattleMiniMapArea.y - self.enemyDetectSizeModifier:const.BattleMiniMapArea.ys + self.enemyDetectSizeModifier, const.BattleMiniMapArea.x - self.enemyDetectSizeModifier:const.BattleMiniMapArea.xs + self.enemyDetectSizeModifier]
            if (self.__isEnemyNear(thisSmallerMinimap) and (currentTime - self.lastPulledOut > 3)):
                self.lastPulledOut = currentTime
                InputControl.kbDown(self.weaponKey)
                time.sleep(0.02)
                InputControl.kbUp(self.weaponKey)

            # Check if need to call out in game
            if (self.doRandomCallout):
                self.doRandomCallout = False
                self.callout()

            # Check if need to flip car on interval
            if (currentTime - self.lastFlipTime > 5):
                self.lastFlipTime = currentTime
                InputControl.kbDown('r')
                time.sleep(0.02)
                InputControl.kbUp('r')

            # Check if stuck need to self explode
            movementStack = const.getVehicleMovementStack()
            if len(movementStack) == 30 and self.alreadyExplode == False:
                if ((movementStack[0].pos.x == movementStack[29].pos.x) and (movementStack[0].pos.y == movementStack[29].pos.y)):
                    if (self.stuckTimer is None):
                        self.stuckTimer = movementStack[0].time
                    elif (movementStack[0].time - self.stuckTimer > 5):
                        self.parentThread.gameEndedEarlierJustWaiting = True
                        InputControl.kbDown(self.selfExplodeKey)
                        time.sleep(5)
                        InputControl.kbUp(self.selfExplodeKey)
                        time.sleep(0.1)
                        self.alreadyExplode = True
                        if (currentTime - self.initTime < 40):
                            print("Early Return Initiated")
                            setRunningStepId('in_game_early_finish_esc_return_to_garage_label')
                        break
                    
                else:
                    self.stuckTimer = None

            # if game has already been X seconds, self explode.
            if (currentTime - self.initTime > 120):
                InputControl.kbDown(self.selfExplodeKey)
                time.sleep(4)
                InputControl.kbUp(self.selfExplodeKey)
                time.sleep(0.1)
                self.parentThread.gameEndedEarlierJustWaiting = True
                break
        time.sleep(0.1)
        InputControl.kbUp(self.weaponKey)
        InputControl.kbUp(self.selfExplodeKey)
        print("Weapon Deploy Thread Exit")

    def __isEnemyNear(self, minimap_frame) -> bool:
        hsv_minimap_frame = cv2.cvtColor(minimap_frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_minimap_frame, (100, 200, 100), (120, 255, 255))
        if cv2.countNonZero(mask) > 10:
            return True
        return False

    def callout(self):
        # b attack
        # x need help
        # z defend
        # j watch out
        # m thanks
        # k sorry
        callout = random.choice(list(self.calloutKeys))
        callout2 = random.choice(list(self.calloutKeys))
        InputControl.kbDown(callout)
        time.sleep(0.02)
        InputControl.kbUp(callout)
        time.sleep(1)
        InputControl.kbDown(callout2)
        time.sleep(0.02)
        InputControl.kbUp(callout2)