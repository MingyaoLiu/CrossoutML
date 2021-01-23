
import time

from childproc import ChildProc

from multiprocessing import Value



procIsDone = Value('i', 0)

if __name__ == "__main__":

    
    
    # for i in range(1000):
    #     print(i)
    #     cp = ChildProc(procIsDone)
    #     cp.start()
    #     # cp.join()

    print(procIsDone.value)
    cp = ChildProc(procIsDone)
    cp.start()
    # cp.join()
    print(procIsDone.value)
    while (procIsDone.value == 0):
        print("A")
    
    print("B")