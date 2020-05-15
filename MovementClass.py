from Constants import MoveDirection
import threading
from InputControl import KBPress, kbDown, kbUp, MouseMove


class MoveManagement():

    def __init__(self):
        print("INIT Move Manager")
        self.turnCommandStack = []
        self.isInAllowedZone = False
        self.isAlreadyTurning = False

    def loadTooClose(self, tooCloseTuple):
        if self.isAlreadyTurning:
            pass
        else:
            self.isAlreadyTurning = True
            self.tooCloseTuple = tooCloseTuple
            self.calculateTurn()

    def __finishedMove(self):
        self.isAlreadyTurning = False

    def sendMoveCmd(self, direction, duration):
        print(direction)
        self.turnCommandStack.insert(0, direction)
        if len(self.turnCommandStack) >= 5:
            self.turnCommandStack.pop()
        Move(direction).start()
        move_block_timer = threading.Timer(2, self.__finishedMove)
        move_block_timer.start()

    def calculateTurn(self):

        left_too_close = self.tooCloseTuple[0]
        center_too_close = self.tooCloseTuple[1]
        right_too_close = self.tooCloseTuple[2]

        lastTurnCmd = MoveDirection.front
        if len(self.turnCommandStack) > 0:
            lastTurnCmd = self.turnCommandStack[0]

        if center_too_close:
            if left_too_close:
                if right_too_close:  # 1 1 1
                    if self.isInAllowedZone == False:
                        self.sendMoveCmd(MoveDirection.front, 0.5)
                    else:
                        if lastTurnCmd == MoveDirection.frontRight or lastTurnCmd == MoveDirection.right:
                            self.sendMoveCmd(MoveDirection.backRight, 0.5)
                        elif lastTurnCmd == MoveDirection.frontLeft or lastTurnCmd == MoveDirection.left:
                            self.sendMoveCmd(MoveDirection.backLeft, 0.5)
                        else:
                            self.sendMoveCmd(MoveDirection.back, 0.5)
                else:  # 1 1 0
                    self.sendMoveCmd(MoveDirection.right, 0.5)
            else:
                if right_too_close:  # 0 1 1
                    self.sendMoveCmd(MoveDirection.left, 0.5)
                else:  # 0 1 0
                    if lastTurnCmd == MoveDirection.frontRight or lastTurnCmd == MoveDirection.right:
                        self.sendMoveCmd(MoveDirection.right, 0.5)
                    elif lastTurnCmd == MoveDirection.frontLeft or lastTurnCmd == MoveDirection.left:
                        self.sendMoveCmd(MoveDirection.left, 0.5)
        else:
            self.isInAllowedZone = True
            if left_too_close:
                if right_too_close:  # 1 0 1
                    self.sendMoveCmd(MoveDirection.front, 0.5)
                else:  # 1 0 0
                    self.sendMoveCmd(MoveDirection.frontRight, 0.5)
            else:
                if right_too_close:  # 0 0 1
                    self.sendMoveCmd(MoveDirection.frontLeft, 0.5)
                else:  # 0 0 0
                    if lastTurnCmd == MoveDirection.frontRight or lastTurnCmd == MoveDirection.right:
                        self.sendMoveCmd(MoveDirection.frontLeft, 0.5)
                    elif lastTurnCmd == MoveDirection.frontLeft or lastTurnCmd == MoveDirection.left:
                        self.sendMoveCmd(MoveDirection.frontRight, 0.5)


class Move():

    def __init__(self, direction: MoveDirection):
        self.direction = direction

    def releaseAllButton(self):
        kbUp("w")
        kbUp("a")
        kbUp("s")
        kbUp("d")

    def end(self):
        print("end")

    def around(self):
        kbDown("s")
        KBPress("a", 2).start()

    def turn(self):
        kbUp("spacebar")
        if self.direction == MoveDirection.left:
            kbDown("w")
            KBPress("a", 1).start()
        elif self.direction == MoveDirection.right:
            kbDown("w")
            KBPress("d", 1).start()
        elif self.direction == MoveDirection.backLeft:
            kbDown("w")
            KBPress("a", 1.5).start()
        elif self.direction == MoveDirection.backRight:
            kbDown("w")
            KBPress("d", 1.5).start()
        elif self.direction == MoveDirection.back:
            kbDown("w")
            KBPress("a", 2).start()
        else:
            print("WHAT IS THIS:", self.direction)

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
        if self.direction == MoveDirection.frontLeft:
            kbUp("d")
            kbDown("w")
            kbDown("a")
        elif self.direction == MoveDirection.frontRight:
            kbUp("a")
            kbDown("w")
            kbDown("d")
        elif self.direction == MoveDirection.front:
            kbDown("w")
        else:
            self.releaseAllButton()
            kbDown("spacebar")
            self.startTurnTimer = threading.Timer(1.5, self.back)
            self.startTurnTimer.start()
