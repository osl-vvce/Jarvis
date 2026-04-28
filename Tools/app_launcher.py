import os
import platform
import subprocess
import shutil
from Tools.app_resolver import resolve_and_launch

_IS_LINUX = platform.system().lower() == "linux"

# ─────────────────────────────────────────────
#  CROSS-PLATFORM APP WHITELIST
# ─────────────────────────────────────────────
ALLOWED_APPS_WINDOWS = {
    "chrome": "chrome",
    "google chrome": "chrome",
    "notepad": "notepad",
    "calculator": "calc",
    "command prompt": "cmd",
    "terminal": "powershell",
    "vs code": "code",
    "code": "code",
    "spotify": "spotify",
    "file explorer": "explorer",
    "settings": "start ms-settings:",
    "word": "winword",
    "excel": "excel",
    "powerpoint": "powerpnt",
    "task manager": "taskmgr",
    "camera": "start microsoft.windows.camera:",
}

ALLOWED_APPS_LINUX = {
    "chrome": "google-chrome",
    "google chrome": "google-chrome",
    "chromium": "chromium",
    "notepad": "gedit",
    "text editor": "gedit",
    "calculator": "gnome-calculator",
    "terminal": "gnome-terminal",
    "vs code": "code",
    "code": "code",
    "spotify": "spotify",
    "file manager": "nautilus",
    "files": "nautilus",
    "settings": "gnome-control-center",
    "camera": "cheese",
    "firefox": "firefox",
    "file explorer": "nautilus",
}

ALLOWED_APPS = ALLOWED_APPS_LINUX if _IS_LINUX else ALLOWED_APPS_WINDOWS


def _launch_linux(command: str) -> bool:
    """Launch an app on Linux, searching PATH for the binary."""
    # Try the exact command first
    binary = shutil.which(command)
    if binary:
        try:
            subprocess.Popen(
                [binary],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True  # Detach from Jarvis's terminal
            )
            return True
        except Exception as e:
            print(f"[LAUNCHER] Failed to launch {binary}: {e}")
    return False


def _launch_windows(command: str) -> bool:
    """Launch an app on Windows."""
    try:
        if command.startswith("start "):
            os.system(command)
        else:
            subprocess.Popen(command, shell=True)
        return True
    except Exception as e:
        print(f"[LAUNCHER] Failed to launch {command}: {e}")
        return False


def open_app(app_name: str) -> tuple[bool, str]:
    """
    Safely launches an application. Cross-platform.
    Prioritizes Whitelist -> Dynamic Discovery -> Fallback.
    """
    app_key = app_name.lower().strip()
    
    # 1. Whitelist Check (Fast & Known Good)
    if app_key in ALLOWED_APPS:
        command = ALLOWED_APPS[app_key]

        if _IS_LINUX:
            if _launch_linux(command):
                return True, f"Opening {app_key} now, sir."
            # On Linux, try common alternatives
            # e.g. "google-chrome" failed → try "chromium"
            alternatives = {
                "google-chrome": ["chromium", "chromium-browser"],
                "gedit": ["gnome-text-editor", "xed", "kate", "mousepad"],
                "gnome-calculator": ["kcalc", "galculator"],
                "gnome-terminal": ["konsole", "xfce4-terminal", "xterm"],
                "nautilus": ["dolphin", "thunar", "nemo", "pcmanfm"],
                "cheese": ["gnome-camera"],
            }
            for alt in alternatives.get(command, []):
                if _launch_linux(alt):
                    return True, f"Opening {app_key} now, sir."
            return False, f"I couldn't find {app_key} installed on this system."
        else:
            if _launch_windows(command):
                return True, f"Opening {app_key} now, sir."
            return False, f"I attempted to open {app_key}, but encountered an error."

    # 2. Dynamic Resolution (Process Check -> Shell -> Start Menu)
    success, msg = resolve_and_launch(app_name)
    if success:
        return True, msg
        
    # 3. Final Silent Failure
    return False, ""
