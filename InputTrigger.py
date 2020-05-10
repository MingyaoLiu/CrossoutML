# CODE CITATION:
# Inspired from this post
# https://stackoverflow.com/questions/11906925/python-simulate-keydown

import ctypes
import time
import win32api
import win32con
import threading

from ctypes import windll

def char2key(c):
    result = windll.User32.VkKeyScanW(ord(str(c)))
    shift_state = (result & 0xFF00) >> 8
    vk_key = result & 0xFF

    return vk_key

# Actuals Functions


class KeyPress:

    def __init__(self, key, duration = 0.04):
        # print(key, duration)
        self.key = char2key(key)
        self.keyPressTimer = threading.Timer(float(duration), self.threadEnd)


    def threadEnd(self):
        self.keyPressTimer.cancel()
        win32api.keybd_event(self.key, 0, win32con.KEYEVENTF_KEYUP, 0)

    def start(self):
        win32api.keybd_event(self.key, 0,0,0)
        self.keyPressTimer.start()


def keyHold(key):
    win32api.keybd_event(char2key(key), 0,0,0)
    
def keyRelease(key):
    win32api.keybd_event(char2key(key), 0, win32con.KEYEVENTF_KEYUP, 0)
    


def mouseClick(pos):
    win32api.SetCursorPos(pos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, pos[0], pos[1], 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, pos[0], pos[1], 0, 0)

def setMousePos(pos):
    win32api.SetCursorPos(pos)

def getMousePos():
    return win32api.GetCursorPos()
