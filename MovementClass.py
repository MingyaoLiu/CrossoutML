from Constants import MoveDirection
import threading
from InputControl import KBPress, kbDown, kbUp, MouseMove


class Move():

    def __init__(self, direction: MoveDirection, turnBlockTime):
        print("New turn event received")
        self.direction = direction
        self.turnBlockTime = turnBlockTime

    def end(self):

        global isAlreadyExecutingTurn

        isAlreadyExecutingTurn = False

        # kbUp("w")
        # kbUp("a")
        # kbUp("s")
        # kbUp("d")

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
