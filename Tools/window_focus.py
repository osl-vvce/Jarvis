import sys
import os
import platform
import subprocess

_IS_LINUX = platform.system().lower() == "linux"

try:
    import win32gui
    import win32con
    import win32com.client
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

def focus_window(app_name: str) -> bool:
    """
    Attempts to find a window matching the app_name and bring it to foreground.
    Case insensitive partial match on window title. Cross-platform.
    """
    app_key = app_name.lower().strip()

    if _IS_LINUX:
        return _focus_window_linux(app_key)

    if not WIN32_AVAILABLE:
        return False

    return _focus_window_windows(app_key)


def _focus_window_linux(app_key: str) -> bool:
    """Focus a window on Linux using xdotool."""
    try:
        result = subprocess.run(
            ["xdotool", "search", "--name", app_key],
            capture_output=True, text=True
        )
        window_ids = result.stdout.strip().split('\n')
        if window_ids and window_ids[0]:
            subprocess.run(["xdotool", "windowactivate", window_ids[0]])
            return True
    except FileNotFoundError:
        # xdotool not installed — silent fail
        pass
    except Exception as e:
        print(f"[FOCUS] Error focusing window on Linux: {e}")
    return False


def _focus_window_windows(app_key: str) -> bool:
    """Focus a window on Windows using win32gui."""
    found_hwnd = None
    
    def callback(hwnd, extra):
        nonlocal found_hwnd
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd).lower()
            if app_key in title:
                # Prioritize windows that look like main app windows
                if found_hwnd is None:
                    found_hwnd = hwnd
                
    try:
        win32gui.EnumWindows(callback, None)
        
        if found_hwnd:
            # Restore if minimized
            win32gui.ShowWindow(found_hwnd, win32con.SW_RESTORE)
            
            # Bring to front safely
            try:
                shell = win32com.client.Dispatch("WScript.Shell")
                shell.SendKeys('%') # Dummy key to wake up input
                win32gui.SetForegroundWindow(found_hwnd)
            except Exception as e:
                print(f"Error focussing window: {e}")
                
            return True
            
    except Exception as e:
        print(f"Window enumeration error: {e}")
        
    return False
