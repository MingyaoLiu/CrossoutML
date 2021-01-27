
import Constants as const
from threading import Thread
import time
import InputControl
import math
#
# Thread for controling the vehicle speed during battle.
# This thread will be blocking due to the nature of keyboard control.
#
class InCombatVehicleSpeedControlThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.isRunning = True
        print("In Combat Speed Control init")

    def run(self):

        while self.isRunning:
            movements = const.getVehicleMovementStack()
            if len(movements) > 10:
                
                speed = 0
                thisData = movements[0]
                lastData = movements[10]
                pixel_distance = self.__calcDistance(lastData.pos, thisData.pos)
                speed = pixel_distance / (time.time() - lastData.time) * 5 # speed may need multiplier to be more accurate
                
                if speed > 50:
                    InputControl.kbUp("w")
                    InputControl.kbDown("spacebar")
                elif speed > 40:
                    InputControl.kbUp("spacebar")
                    InputControl.kbUp("w")
                elif speed < 30:
                    InputControl.kbUp("spacebar")
                    InputControl.kbDown("w")
                else:
                    InputControl.kbUp("w")
                    InputControl.kbUp("spacebar")
                time.sleep(0.15)
        time.sleep(0.05)
        InputControl.kbUp("w")
        InputControl.kbUp("spacebar")
        print("In Combat Speed Control Exit")


    def __calcDistance(self, pos1: const.Point, pos2: const.Point) -> float:
        if (pos1 == pos2):
            return 0
        return math.sqrt((pos1.x - pos2.x) * (pos1.x - pos2.x) + (pos1.y - pos2.y) * (pos1.y - pos2.y))

