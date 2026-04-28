import os
import platform
import subprocess
from Brain.personality import jarvis_speak

# ─────────────────────────────────────────────
#  CROSS-PLATFORM PROCESS MAP
#  Maps friendly names → process names per OS.
# ─────────────────────────────────────────────
_IS_LINUX = platform.system().lower() == "linux"

PROCESS_MAP_WINDOWS = {
    "calculator": ["CalculatorApp.exe", "calc.exe"],
    "notepad": ["notepad.exe"],
    "chrome": ["chrome.exe"],
    "google chrome": ["chrome.exe"],
    "vs code": ["Code.exe"],
    "code": ["Code.exe"],
    "spotify": ["Spotify.exe"],
    "task manager": ["Taskmgr.exe"],
    "settings": ["SystemSettings.exe"],
    "camera": ["WindowsCamera.exe"]
}

PROCESS_MAP_LINUX = {
    "calculator": ["gnome-calculator", "kcalc", "galculator"],
    "notepad": ["gedit", "gnome-text-editor", "xed", "kate", "nano"],
    "chrome": ["chrome", "chromium", "google-chrome"],
    "google chrome": ["chrome", "chromium", "google-chrome"],
    "vs code": ["code"],
    "code": ["code"],
    "spotify": ["spotify"],
    "file manager": ["nautilus", "dolphin", "thunar", "nemo"],
    "files": ["nautilus", "dolphin", "thunar", "nemo"],
    "camera": ["cheese", "gnome-camera"],
    "firefox": ["firefox"],
    "terminal": ["gnome-terminal", "konsole", "xfce4-terminal"],
}

PROCESS_MAP = PROCESS_MAP_LINUX if _IS_LINUX else PROCESS_MAP_WINDOWS


def _kill_process_linux(process_name: str) -> bool:
    """Kill a process by name on Linux using pkill."""
    try:
        result = subprocess.run(
            ["pkill", "-f", process_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception as e:
        print(f"[CLOSER] Error killing {process_name} on Linux: {e}")
        return False


def _kill_process_windows(process_name: str) -> bool:
    """Kill a process by name on Windows using taskkill."""
    try:
        result = os.system(f"taskkill /F /IM {process_name} /T >nul 2>&1")
        return result == 0
    except Exception as e:
        print(f"[CLOSER] Error killing {process_name} on Windows: {e}")
        return False


def close_app(app_name: str) -> tuple[bool, str]:
    """
    Terminates an application by name. Cross-platform.
    """
    app_key = app_name.lower().strip()
    
    if app_key in PROCESS_MAP:
        targets = PROCESS_MAP[app_key]
        killed_any = False
        
        for process in targets:
            if _IS_LINUX:
                if _kill_process_linux(process):
                    killed_any = True
            else:
                if _kill_process_windows(process):
                    killed_any = True

        if killed_any:
            return True, f"Closing {app_key}."
        else:
            return True, f"Closing {app_key}."  # Optimistic confirmation
            
    else:
        # Fallback: try killing by name directly
        if _IS_LINUX:
            if _kill_process_linux(app_key):
                return True, f"Closing {app_key}."
        return False, f"I cannot close {app_key} because I don't know its process name."
