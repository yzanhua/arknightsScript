import win32api, win32gui, win32con, time, ctypes
from ctypes import windll
from utils import debugPrint, debugSleep, KEYBOARDMAP, runOnce


@runOnce
def setDPI():
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

def getCurrentCursorPos():
    setDPI()
    x, y = win32gui.GetCursorPos()
    debugPrint("CurPos: ", (x, y))
    return x, y

def sleep(t):
    time.sleep(t)


def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def moveCursorPos(x, y):
    setDPI()
    windll.user32.SetCursorPos(x, y)


def typeString(s, timeInterval=0.1):
    '''
    Type the string s. Wait timeInterval secs between each char.
    String s should only contains lower english letters and digits.
    length of s should <= 30.
    '''
    if len(s) > 30:
        debugPrint("Error in typeString(s) @cur.py: \n \t len of s > 30 \n")

    if not all(c.isdigit() or c.islower() for c in s):
        debugPrint("Error in typeString(s) @cur.py: \n \t s should only contains lower english letters and digits.\n")
    
    for c in s:
        typeChr(c, timeInterval)


def typeChr(c, timeInterval=0.1):
    win32api.keybd_event(KEYBOARDMAP[c], 0,0,0)
    time.sleep(.05)
    win32api.keybd_event(KEYBOARDMAP[c],0 ,win32con.KEYEVENTF_KEYUP ,0)
    time.sleep(timeInterval)

