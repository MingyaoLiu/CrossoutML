
import cv2
from threading import Thread
import Constants as const
from DCaptureClass import getDCapture
import time
import InputControl

class InCombatDeployWeaponThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.isRunning = True
        self.lastPulledOut = time.time()
        self.stuckTimer = None
        print("Weapon Deploy Thread Init")

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
            if len(movementStack) == 30:
                if ((movementStack[0].pos.x == movementStack[29].pos.x) and (movementStack[0].pos.y == movementStack[29].pos.y)):
                    if (self.stuckTimer is None):
                        self.stuckTimer = movementStack[0].time
                    elif (movementStack[0].time - self.stuckTimer > 5):
                        InputControl.kbDown('backspace')
                        time.sleep(5)
                        InputControl.kbUp('backspace')
                        time.sleep(0.1)
                        break
                    
                else:
                    self.stuckTimer = None
        print("Weapon Deploy Thread Exit")



    def __isEnemyNear(self, minimap_frame) -> bool:
        hsv_minimap_frame = cv2.cvtColor(minimap_frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_minimap_frame, (100, 200, 100), (120, 255, 255))
        if cv2.countNonZero(mask) > 10:
            return True
        return False

