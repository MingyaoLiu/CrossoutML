import numpy as np
import ctypes
import time
import win32api
import win32con
import threading

from ctypes import windll

from Constants import Point

vk_key_dict = {
    "spacebar": 0x20,
    "esc": 0x1B,
    "backspace": 0x08
}


def char2key(c):
    if c in vk_key_dict:
        return vk_key_dict[c]
    elif len(str(c)) == 1:
        ord1 = ord(str(c))
        result = windll.User32.VkKeyScanW(ord1)
        shift_state = (result & 0xFF00) >> 8
        vk_key = result & 0xFF
        return vk_key
    else:
        print("Not in VK list and Not A Single Char")
        return vk_key_dict["esc"]


class KBPress:

    def __init__(self, key, duration=0.04):
        # print(key, duration)
        self.key = char2key(key)
        self.keyPressTimer = threading.Timer(float(duration), self.threadEnd)

    def threadEnd(self):
        self.keyPressTimer.cancel()
        win32api.keybd_event(self.key, 0, win32con.KEYEVENTF_KEYUP, 0)

    def start(self):
        win32api.keybd_event(self.key, 0, 0, 0)
        self.keyPressTimer.start()


def kbDown(key):
    win32api.keybd_event(char2key(key), 0, 0, 0)


def kbUp(key):
    win32api.keybd_event(char2key(key), 0, win32con.KEYEVENTF_KEYUP, 0)


class MouseMove:

    def __init__(self, orig_pos: Point, end_pos: Point, duration=1):
        self.orig_pos = orig_pos
        self.end_pos = end_pos
        self.duration = duration
        self.isComplete = False

    def start(self):
        setMousePos(self.orig_pos)
        m = (self.end_pos.y - self.orig_pos.y) / \
            (self.end_pos.x - self.orig_pos.x)

        for i in np.arange(self.orig_pos.x, self.end_pos.x, 1):
            setMousePos(Point(i, i * m))
            time.sleep(0.1)
        self.isComplete = True

    def isTimerActive(self):
        return self.isComplete


def mouseClick(pos: Point):
    setMousePos(pos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, pos.x, pos.y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, pos.x, pos.y, 0, 0)


def setMousePos(pos: Point):
    win32api.SetCursorPos((pos.x, pos.y))


def getMousePos():
    return win32api.GetCursorPos()
