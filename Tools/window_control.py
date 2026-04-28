import platform
import subprocess
import pyautogui

_IS_LINUX = platform.system().lower() == "linux"

try:
    import win32gui
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False


def _xdotool_available() -> bool:
    """Check if xdotool is installed on Linux."""
    try:
        subprocess.run(
            ["xdotool", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except FileNotFoundError:
        return False


def minimize_window(app_name: str) -> tuple[bool, str]:
    """Minimizes a window by app name. Cross-platform."""
    app_key = app_name.lower().strip()

    if _IS_LINUX:
        if not _xdotool_available():
            print("[WINDOW] xdotool not found. Install with: sudo dnf install xdotool")
            return False, "Window control requires xdotool on Linux."
        try:
            # Find window by name
            result = subprocess.run(
                ["xdotool", "search", "--name", app_key],
                capture_output=True, text=True
            )
            window_ids = result.stdout.strip().split('\n')
            if window_ids and window_ids[0]:
                subprocess.run(["xdotool", "windowminimize", window_ids[0]])
                return True, "Window minimized."
        except Exception as e:
            print(f"[WINDOW] Minimize error on Linux: {e}")
        return False, ""

    # Windows path
    if not WIN32_AVAILABLE:
        return False, "Not supported on this OS"
    found_hwnd = None
    
    def callback(hwnd, extra):
        nonlocal found_hwnd
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd).lower()
            if app_key in title:
                found_hwnd = hwnd
                
    try:
        win32gui.EnumWindows(callback, None)
        if found_hwnd:
            win32gui.ShowWindow(found_hwnd, win32con.SW_MINIMIZE)
            return True, "Window minimized."
    except Exception as e:
        print(f"[WINDOW] Minimize error: {e}")
    return False, ""


def minimize_active_window() -> tuple[bool, str]:
    """Minimizes the currently focused window. Cross-platform."""
    if _IS_LINUX:
        if not _xdotool_available():
            return False, "Window control requires xdotool on Linux."
        try:
            result = subprocess.run(
                ["xdotool", "getactivewindow"],
                capture_output=True, text=True
            )
            window_id = result.stdout.strip()
            if window_id:
                subprocess.run(["xdotool", "windowminimize", window_id])
                return True, "Window minimized."
        except Exception as e:
            print(f"[WINDOW] Minimize active error on Linux: {e}")
        return False, ""

    if not WIN32_AVAILABLE:
        return False, "Not supported on this OS"
    try:
        hwnd = win32gui.GetForegroundWindow()
        if hwnd:
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            return True, "Window minimized."
    except Exception as e:
        print(f"[WINDOW] Minimize active error: {e}")
    return False, ""


def show_all_windows() -> tuple[bool, str]:
    """Opens Task View / Activity Overview. Cross-platform."""
    try:
        if _IS_LINUX:
            # GNOME: Super key opens Activities overview
            pyautogui.hotkey('super')
        else:
            pyautogui.hotkey('win', 'tab')
        return True, "Showing all windows."
    except Exception as e:
        print(f"[WINDOW] Task view error: {e}")
    return False, ""


def open_start_menu() -> tuple[bool, str]:
    """Presses Super/Windows key. Cross-platform."""
    try:
        if _IS_LINUX:
            pyautogui.hotkey('super')
        else:
            pyautogui.press('win')
        return True, "Start menu opened."
    except Exception:
        pass
    return False, ""
