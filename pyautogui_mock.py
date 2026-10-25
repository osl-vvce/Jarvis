# Mock pyautogui to allow script to run in environment without it installed

FAILSAFE = True

def write(*args, **kwargs): pass
def press(*args, **kwargs): pass
def hotkey(*args, **kwargs): pass
def typewrite(*args, **kwargs): pass
def click(*args, **kwargs): pass
def doubleClick(*args, **kwargs): pass
def rightClick(*args, **kwargs): pass
def screenshot(*args, **kwargs):
    class MockImg:
        def save(self, *a, **k): pass
    return MockImg()
def locateCenterOnScreen(*args, **kwargs): return None
def locateOnScreen(*args, **kwargs): return None
def center(*args, **kwargs): return None
def scroll(*args, **kwargs): pass
def moveRel(*args, **kwargs): pass
def mouseDown(*args, **kwargs): pass
def mouseUp(*args, **kwargs): pass
def dragTo(*args, **kwargs): pass
