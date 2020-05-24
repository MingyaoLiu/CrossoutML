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

        ## Left Right initial trigger record
        self.initTooCloseDirection = None

        self.globalDelayFrameCount = 5

        self.globalConfirmTurnDoneFrameCount = 30
        self.currentConfirmFrameCount = 0


    def forceBackComplate(self):
        self.forcingBack = False

    def forceBackStage2(self):
        kbUp("s")
        kbDown("w")
        forceBack2Timer = threading.Timer(1, self.forceBackComplate)
        forceBack2Timer.start()

    def forceToBack(self):
        print("force back")
        if self.forcingBack:
            return
        self.forcingBack = True
        kbUp("w")
        kbUp("a")
        kbUp("s")
        kbUp("d")
        kbUp("spacebar")
        # self.sendMoveCmd(MoveDirection.back, 5)
        # KBPress("spacebar", 1).start()
        kbDown("s")
        KBPress("d", 1.75).start()
        forceBack1Timer = threading.Timer(4, self.forceBackStage2)
        forceBack1Timer.start()

    def loadNewBF(self, bf: BattleFrame):
        print(bf.speed)

        if self.forcingBack:
            return

        if bf.posData.isOutside:
            if self.isInAllowedZone is False:
                kbDown("w")
                pass
            else:
                print("It's Fked")
                self.forceToBack()
        else:
            self.isInAllowedZone = True
        

        if bf.center.far.isOutside or bf.center.mid.isOutside or bf.center.low.isOutside or bf.left.isOutside or bf.right.isOutside:
            # Determine Forward Speed
            if bf.speed > 70:
                kbUp("w")
                kbDown("spacebar")
            elif bf.speed > 30:
                kbUp("spacebar")
                kbUp("w")
            elif bf.speed < 15:
                kbUp("spacebar")
                kbDown("w")
            else:
                kbUp("spacebar")
                kbDown("w")
            # Determine Turn

            if self.initTooCloseDirection == "LEFT":
                print("Init Turning is LEFT")
                kbUp("a")
                if bf.left.isOutside:
                    if bf.center.low.isOutside:
                        kbDown("d")
                        self.currentConfirmFrameCount = 0
                    else:
                        kbUp("d")
                        if self.currentConfirmFrameCount > self.globalConfirmTurnDoneFrameCount:
                            self.initTooCloseDirection = None
                            self.currentConfirmFrameCount = 0
                        else:
                            self.currentConfirmFrameCount += 1
                else:
                    print("LEFT is completely inside zone, turning is too far.")
                    kbUp("d")
                    self.initTooCloseDirection = None
                    self.currentConfirmFrameCount = 0

            elif self.initTooCloseDirection == "RIGHT":
                print("Init Turning is RIGHT")
                kbUp("d")
                if bf.right.isOutside:
                    if bf.center.low.isOutside:
                        kbDown("a")
                        self.currentConfirmFrameCount = 0
                    else:
                        kbUp("a")
                        if self.currentConfirmFrameCount > self.globalConfirmTurnDoneFrameCount:
                            self.initTooCloseDirection = None
                            self.currentConfirmFrameCount = 0
                        else:
                            self.currentConfirmFrameCount += 1
                else:
                    print("LEFT is completely inside zone, turning is too far.")
                    kbUp("a")
                    self.initTooCloseDirection = None
                    self.currentConfirmFrameCount = 0
                
            else:
                print("No Init Turning Direction, Could be turning not yet set, or not turning, or left and right enter turning at the same time.")
                kbUp("a")
                kbUp("d")

                if bf.left.isOutside and bf.right.isOutside:
                    if bf.posData.isOutside:
                        print("CAR IS OUTSIDE")
                        self.forceToBack()
                    else:
                        print("Both Tentacle Outside, No Init")

                elif bf.right.isOutside:
                    if bf.center.mid.isOutside or bf.center.low.isOutside:
                        self.initTooCloseDirection = "RIGHT"
                        kbDown("a")
                    else:
                        print("RIGHT but still have distance to go.")

                elif bf.left.isOutside:
                    if bf.center.mid.isOutside or bf.center.low.isOutside:
                        self.initTooCloseDirection = "LEFT"
                        kbDown("d")
                    else:
                        print("LEFT but still have distance to go.")
                else:
                    pass

        else:
            kbUp("spacebar")
            kbUp("a")
            kbUp("d")

            kbDown("w")
            print("Nothing is detected, go straight forward")

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
