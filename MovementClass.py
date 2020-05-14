from Constants import MoveDirection
import threading
from InputControl import KBPress, kbDown, kbUp, MouseMove


class MoveManagement():

    def __init__(self, direction: MoveDirection, turnBlockTime):
        print("New turn event received")
        self.direction = direction
        self.turnBlockTime = turnBlockTime

    def calculateTurn():
        left_pos = self.tentacle_pos_lst[0]
        left_too_close = False if self.map_mask[left_pos[1],
                                                left_pos[0]] == 0 else True
        center_pos = self.tentacle_pos_lst[1]
        center_too_close = False if self.map_mask[center_pos[1],
                                                  center_pos[0]] == 0 else True
        right_pos = self.tentacle_pos_lst[2]
        right_too_close = False if self.map_mask[right_pos[1],
                                                 right_pos[0]] == 0 else True

        straight_block_time = 0
        minor_turn_block_time = 0
        right_angle_block_time = 1.2
        extra_turn_block_time = 2
        full_turn_block_time = 2.6

        direction = const.MoveDirection.front
        lastTurnCmd = const.MoveDirection.front
        if len(turnCommandStack) > 0:
            lastTurnCmd = turnCommandStack[0]

        if center_too_close:
            if left_too_close:
                if right_too_close:  # 1 1 1
                    if isInAllowedZone == False:
                        direction = const.MoveDirection.front
                        Move(
                            direction, straight_block_time).start()
                    else:
                        if lastTurnCmd == const.MoveDirection.frontRight or lastTurnCmd == const.MoveDirection.right:
                            direction = const.MoveDirection.backRight
                            Move(
                                direction, extra_turn_block_time).start()
                        elif lastTurnCmd == const.MoveDirection.frontLeft or lastTurnCmd == const.MoveDirection.left:
                            direction = const.MoveDirection.backLeft
                            Move(
                                direction, extra_turn_block_time).start()
                        else:
                            direction = const.MoveDirection.back
                            Move(
                                direction, full_turn_block_time).start()
                else:  # 1 1 0
                    direction = const.MoveDirection.right
                    Move(
                        direction, right_angle_block_time).start()
            else:
                if right_too_close:  # 0 1 1
                    direction = const.MoveDirection.left
                    Move(
                        direction, right_angle_block_time).start()
                else:  # 0 1 0
                    if lastTurnCmd == const.MoveDirection.frontRight or lastTurnCmd == const.MoveDirection.right:
                        direction = const.MoveDirection.right
                        Move(
                            direction, right_angle_block_time).start()
                    elif lastTurnCmd == const.MoveDirection.frontLeft or lastTurnCmd == const.MoveDirection.left:
                        direction = const.MoveDirection.left
                        Move(
                            direction, right_angle_block_time).start()
        else:
            isInAllowedZone = True
            if left_too_close:
                if right_too_close:  # 1 0 1
                    direction = const.MoveDirection.front
                    Move(
                        direction, straight_block_time).start()
                else:  # 1 0 0
                    direction = const.MoveDirection.frontRight
                    Move(
                        direction, minor_turn_block_time).start()
            else:
                if right_too_close:  # 0 0 1
                    direction = const.MoveDirection.frontLeft
                    Move(
                        direction, minor_turn_block_time).start()
                else:  # 0 0 0
                    if lastTurnCmd == const.MoveDirection.frontRight or lastTurnCmd == const.MoveDirection.right:
                        direction = const.MoveDirection.frontLeft
                        Move(
                            direction, right_angle_block_time).start()
                    elif lastTurnCmd == const.MoveDirection.frontLeft or lastTurnCmd == const.MoveDirection.left:
                        direction = const.MoveDirection.frontRight
                        Move(
                            direction, right_angle_block_time).start()
        print(direction)
        turnCommandStack.insert(0, direction)
        if len(turnCommandStack) >= 5:
            turnCommandStack.pop()


class Move():

    def __init__(self, direction: MoveDirection, turnBlockTime):
        print("New turn event received")
        self.direction = direction
        self.turnBlockTime = turnBlockTime

    def end(self):
        global isAlreadyExecutingTurn
        isAlreadyExecutingTurn = False

    def releaseAllButton(self):
        kbUp("w")
        kbUp("a")
        kbUp("s")
        kbUp("d")

    def around(self):
        kbDown("s")
        KBPress("a", 2).start()
        self.endTimer = threading.Timer(3, self.end)
        self.endTimer.start()

    def turn(self):
        kbUp("spacebar")
        # Hold direction for time divided by turn around time

        if self.direction == MoveDirection.left:
            kbDown("w")
            KBPress("a", 1).start()
            self.endTimer = threading.Timer(2, self.end)
            self.endTimer.start()
        elif self.direction == MoveDirection.right:
            kbDown("w")
            KBPress("d", 1).start()
            self.endTimer = threading.Timer(2, self.end)
            self.endTimer.start()
        elif self.direction == MoveDirection.backLeft:
            kbDown("w")
            KBPress("a", 1.5).start()
            self.endTimer = threading.Timer(2.5, self.end)
            self.endTimer.start()
        elif self.direction == MoveDirection.backRight:
            kbDown("w")
            KBPress("d", 1.5).start()
            self.endTimer = threading.Timer(2.5, self.end)
            self.endTimer.start()

        elif self.direction == MoveDirection.back:
            kbDown("w")
            KBPress("a", 2).start()
            self.endTimer = threading.Timer(3, self.end)
            self.endTimer.start()
        else:
            print("WHAT IS THIS")

    def stop(self):
        kbDown("spacebar")
        self.turnTimer = threading.Timer(1.1, self.turn)
        self.turnTimer.start()

    def back(self, time=1):
        kbUp("spacebar")
        KBPress("s", 1).start()
        self.stopTimer = threading.Timer(1.1, self.stop)
        self.stopTimer.start()

    def start(self):
        global isAlreadyExecutingTurn
        # isAlreadyExecutingTurn = True
        if self.direction == MoveDirection.frontLeft:
            kbUp("d")
            kbDown("w")
            kbDown("a")
            isAlreadyExecutingTurn = False
        elif self.direction == MoveDirection.frontRight:
            kbUp("a")
            kbDown("w")
            kbDown("d")
            isAlreadyExecutingTurn = False
        elif self.direction == MoveDirection.front:
            kbDown("w")
            isAlreadyExecutingTurn = False
            pass
        else:
            isAlreadyExecutingTurn = True

            # release all button
            self.releaseAllButton()
            # Hold Full Stop
            kbDown("spacebar")
            self.startTurnTimer = threading.Timer(1.5, self.back)
            self.startTurnTimer.start()

        # kbDown("w")
        # if self.direction == MoveDirection.backLeft:
        #     kbDown("a")
        # elif self.direction == MoveDirection.left:
        #     kbDown("a")
        # elif self.direction == MoveDirection.frontLeft:
        #     kbDown("a")
        # elif self.direction == MoveDirection.front:
        #     pass
        # elif self.direction == MoveDirection.frontRight:
        #     kbDown("d")
        # elif self.direction == MoveDirection.right:
        #     kbDown("d")
        # elif self.direction == MoveDirection.backRight:
        #     kbDown("d")
        # elif self.direction == MoveDirection.back:
        #     kbDown("d")
