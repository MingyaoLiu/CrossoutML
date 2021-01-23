
from multiprocessing import Process
import time

class ChildProc(Process):
    def __init__(self, procIsDone):
        super(ChildProc, self).__init__()
        self.procDone = procIsDone
    def run(self):
        time.sleep(5)
        self.procDone.value = 1
        print('hello')
