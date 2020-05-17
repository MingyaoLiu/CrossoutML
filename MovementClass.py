from Constants import MoveDirection, BattleFrame, Point, PointData
import threading
from InputControl import KBPress, kbDown, kbUp, MouseMove
from Utils import atLeastTwoTrue


class MoveManagement():

    def __init__(self):
        print("INIT Move Manager")
        self.tooCloseStack = []
        self.turnCommandStack = []
        self.isInAllowedZone = False
        self.isAlreadyTurning = False
        self.move_block_timer = None
        self.forcingBack = False

    def forceToBack(self):
        self.forcingBack = True
        self.sendMoveCmd(MoveDirection.back, 5)

    def loadNewBF(self, bf: BattleFrame):
        print(bf.speed)

        if bf.center.far.isOutside or bf.center.mid.isOutside or bf.center.low.isOutside or bf.left.isOutside or bf.right.isOutside:
            if bf.speed > 70:
                kbUp("w")
                kbDown("spacebar")
            elif bf.speed > 40:
                kbUp("spacebar")
                kbUp("w")
            elif bf.speed < 20:
                kbUp("spacebar")
                kbDown("w")
            else:
                kbUp("spacebar")
                kbDown("w")
            if bf.left.isOutside and bf.right.isOutside:
                if bf.center.low.isOutside:
                    print("It's Fked")
                    kbUp("d")
                    kbDown("a")
                else:
                    print("Waiting for anything to change")
                    kbUp("a")
                    kbUp("d")
            elif bf.right.isOutside:
                kbUp("d")
                if bf.center.low.isOutside:
                    kbDown("a")
                else:
                    kbUp("a")
            elif bf.left.isOutside:
                kbUp("a")
                if bf.center.low.isOutside:
                    kbDown("d")
                else:
                    kbUp("d")
            else:
                kbUp("a")
                kbUp("d")

        else:
            kbUp("spacebar")
            kbUp("a")
            kbUp("d")

            kbDown("w")
            print("Nothing is detected, go straight forward")

    def loadTooClose(self, tooCloseTuple):
        if (self.forcingBack is False) and self.isAlreadyTurning and len(self.tooCloseStack):

            if (tooCloseTuple[0] != self.tooCloseStack[0][0] or tooCloseTuple[2] != self.tooCloseStack[0][2]):

                if self.move_block_timer:
                    self.move_block_timer.cancel()
                self.tooCloseTuple = tooCloseTuple
                self.calculateTurn()
            else:
                pass
        elif self.forcingBack:
            pass
        else:
            self.tooCloseStack.insert(0, tooCloseTuple)
            if len(self.tooCloseStack) >= 5:
                self.tooCloseStack.pop()
            self.isAlreadyTurning = True
            self.tooCloseTuple = tooCloseTuple
            self.calculateTurn()

    def __finishedMove(self):
        self.isAlreadyTurning = False
        self.move_block_timer = None
        self.forcingBack = False

    def sendMoveCmd(self, direction, duration):
        print(direction)
        self.turnCommandStack.insert(0, direction)
        if len(self.turnCommandStack) >= 5:
            self.turnCommandStack.pop()
        Move(direction).start()
        self.move_block_timer = threading.Timer(duration, self.__finishedMove)
        self.move_block_timer.start()

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
                        self.sendMoveCmd(MoveDirection.front, 0.1)
                    else:
                        self.sendMoveCmd(MoveDirection.left, 1)
                        # if lastTurnCmd == MoveDirection.frontRight or lastTurnCmd == MoveDirection.right:
                        #     self.sendMoveCmd(MoveDirection.backRight, 4)
                        # elif lastTurnCmd == MoveDirection.frontLeft or lastTurnCmd == MoveDirection.left:
                        #     self.sendMoveCmd(MoveDirection.backLeft, 4)
                        # else:
                        #     self.sendMoveCmd(MoveDirection.back, 5)
                else:  # 1 1 0
                    self.sendMoveCmd(MoveDirection.right, 3)
            else:
                if right_too_close:  # 0 1 1
                    self.sendMoveCmd(MoveDirection.left, 3)
                else:  # 0 1 0
                    if lastTurnCmd == MoveDirection.frontRight or lastTurnCmd == MoveDirection.right:
                        self.sendMoveCmd(MoveDirection.frontRight, 0.35)
                    elif lastTurnCmd == MoveDirection.frontLeft or lastTurnCmd == MoveDirection.left:
                        self.sendMoveCmd(MoveDirection.frontLeft, 0.35)
                    else:
                        self.sendMoveCmd(MoveDirection.back, 5)
        else:
            self.isInAllowedZone = True
            if left_too_close:
                if right_too_close:  # 1 0 1
                    self.sendMoveCmd(MoveDirection.front, 0.1)
                else:  # 1 0 0
                    self.sendMoveCmd(MoveDirection.frontRight, 0.35)
            else:
                if right_too_close:  # 0 0 1
                    self.sendMoveCmd(MoveDirection.frontLeft, 0.35)
                else:  # 0 0 0
                    self.sendMoveCmd(MoveDirection.front, 0.1)
                    # if lastTurnCmd == MoveDirection.frontRight or lastTurnCmd == MoveDirection.right:
                    #     self.sendMoveCmd(MoveDirection.frontLeft, 0.5)
                    # elif lastTurnCmd == MoveDirection.frontLeft or lastTurnCmd == MoveDirection.left:
                    #     self.sendMoveCmd(MoveDirection.frontRight, 0.5)


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

        if self.direction == MoveDirection.backLeft:
            kbDown("w")
            KBPress("a", 2.5).start()
        elif self.direction == MoveDirection.backRight:
            kbDown("w")
            KBPress("d", 2.5).start()
        elif self.direction == MoveDirection.back:
            kbDown("w")
            KBPress("a", 3).start()
        else:
            print("WHAT IS THIS:", self.direction)

    def stop(self):
        kbDown("w")

    def back(self):
        kbUp("spacebar")
        KBPress("s", 1.9).start()
        KBPress("a", 1.9).start()
        self.stopTimer = threading.Timer(2, self.stop)
        self.stopTimer.start()

    def start(self):
        self.releaseAllButton()
        if self.direction == MoveDirection.frontLeft:
            kbDown("w")
            KBPress("a", 0.1).start()
        elif self.direction == MoveDirection.frontRight:
            kbDown("w")
            KBPress("d", 0.1).start()
        elif self.direction == MoveDirection.left:
            kbDown("w")
            KBPress("a", 0.65).start()
        elif self.direction == MoveDirection.right:
            kbDown("w")
            KBPress("d", 0.65).start()
        elif self.direction == MoveDirection.front:
            kbDown("w")
        elif self.direction == MoveDirection.backLeft:
            kbDown("w")
            KBPress("a", 2.5).start()
        elif self.direction == MoveDirection.backRight:
            kbDown("w")
            KBPress("d", 2.5).start()
        elif self.direction == MoveDirection.back:
            kbDown("spacebar")
            self.startTurnTimer = threading.Timer(1, self.back)
            self.startTurnTimer.start()
        else:
            print("WHAT COMMAND IS THIS", self.direction)
            kbDown("w")
            KBPress("d", 3).start()
            # kbDown("spacebar")
            # self.startTurnTimer = threading.Timer(1.5, self.back)
            # self.startTurnTimer.start()
