
import cv2
from threading import Thread
import Constants as const
from DCaptureClass import getDCapture
import time
import InputControl
import random

class InCombatDeployWeaponThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.parentThread = None
        self.isRunning = True
        self.lastPulledOut = time.time()
        self.stuckTimer = None
        self.alreadyExplode = False
        self.doRandomCallout = False
        self.initTime = time.time()
        print("Weapon Deploy Thread Init")

    def run(self):
        while self.isRunning:
            if (self.doRandomCallout):
                self.doRandomCallout = False
                self.callout()

            frame = getDCapture().getFrame(0)
            thisSmallerMinimap = frame[const.BattleMiniMapArea.y + 35:const.BattleMiniMapArea.ys - 35, const.BattleMiniMapArea.x + 35:const.BattleMiniMapArea.xs - 35]
            if (self.__isEnemyNear(thisSmallerMinimap) and (time.time() - self.lastPulledOut > 5)):
                self.lastPulledOut = time.time()
                InputControl.kbDown('1')
                time.sleep(0.1)
                InputControl.kbUp('1')

            movementStack = const.getVehicleMovementStack()
            if len(movementStack) == 30 and self.alreadyExplode == False:
                if ((movementStack[0].pos.x == movementStack[29].pos.x) and (movementStack[0].pos.y == movementStack[29].pos.y)):
                    if (self.stuckTimer is None):
                        self.stuckTimer = movementStack[0].time
                    elif (movementStack[0].time - self.stuckTimer > 5):
                        self.parentThread.gameEndedEarlierJustWaiting = True
                        InputControl.kbDown('backspace')
                        time.sleep(5)
                        InputControl.kbUp('backspace')
                        time.sleep(0.1)
                        self.alreadyExplode = True
                        if (time.time() - self.initTime < 30):
                            const.setRunningStepId('in_game_early_finish_esc_return_to_garage_label')
                        break
                    
                else:
                    self.stuckTimer = None

            if (time.time() - self.initTime > 120):
                InputControl.kbDown('backspace')
                time.sleep(5)
                InputControl.kbUp('backspace')
                time.sleep(0.1)
                self.parentThread.gameEndedEarlierJustWaiting = True
                break
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
        calloutLst = ["b", "x", "z", "j", "m", "k"]
        callout = random.choice(list(calloutLst))
        callout2 = random.choice(list(calloutLst))
        InputControl.kbDown(callout)
        time.sleep(0.05)
        InputControl.kbUp(callout)
        time.sleep(0.1)
        InputControl.kbDown(callout2)
        time.sleep(0.05)
        InputControl.kbUp(callout2)