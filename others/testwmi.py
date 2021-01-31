    
import sys
import os
import traceback
import win32con as wcon
import win32api as wapi
import win32gui as wgui
import win32process as wproc
    
        
import time

import wmi

def enum_windows_proc(wnd, param):
    pid = param.get("pid", None)
    data = param.get("data", None)
    if pid is None or wproc.GetWindowThreadProcessId(wnd)[1] == pid:
        text = wgui.GetWindowText(wnd)
        if text:
            style = wapi.GetWindowLong(wnd, wcon.GWL_STYLE)
            if style & wcon.WS_VISIBLE:
                if data is not None:
                    data.append((wnd, text))
                #else:
                    #print("%08X - %s" % (wnd, text))


def enum_process_windows(pid=None):
    data = []
    param = {
        "pid": pid,
        "data": data,
    }
    wgui.EnumWindows(enum_windows_proc, param)
    return data

if __name__ == "__main__":

    f = wmi.WMI()
    crossoutProcess = None
    for process in f.Win32_Process():
        if ('Crossout' in process.name):
            print(process.ProcessId)
            crossoutProcess = process
            break

    if crossoutProcess is not None:
        data = enum_process_windows(crossoutProcess.ProcessId)
        for handle, text in data:
            print(text)