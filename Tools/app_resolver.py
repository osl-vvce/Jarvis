import os
import platform
import subprocess
import shutil
from Tools.window_focus import focus_window

_IS_LINUX = platform.system().lower() == "linux"

# Standard Start Menu Paths (Windows only)
SHORTCUT_PATHS = []
if not _IS_LINUX:
    SHORTCUT_PATHS = [
        os.path.expandvars(r"%ProgramData%\Microsoft\Windows\Start Menu\Programs"),
        os.path.expandvars(r"%AppData%\Microsoft\Windows\Start Menu\Programs")
    ]

# Common Linux .desktop file locations
DESKTOP_PATHS = [
    "/usr/share/applications",
    "/usr/local/share/applications",
    os.path.expanduser("~/.local/share/applications"),
]


def _search_linux_desktop_files(app_name: str) -> str | None:
    """Search .desktop files on Linux for the app's Exec command."""
    app_key = app_name.lower()
    for base_path in DESKTOP_PATHS:
        if not os.path.isdir(base_path):
            continue
        for filename in os.listdir(base_path):
            if not filename.endswith(".desktop"):
                continue
            if app_key in filename.lower():
                desktop_file = os.path.join(base_path, filename)
                try:
                    with open(desktop_file, 'r') as f:
                        for line in f:
                            if line.startswith("Exec="):
                                # Extract command, strip field codes like %u %U %f
                                cmd = line.split("=", 1)[1].strip()
                                cmd = cmd.split("%")[0].strip()
                                # Remove quotes if present
                                cmd = cmd.strip('"').strip("'")
                                return cmd
                except Exception:
                    continue
    return None


def search_start_menu(app_name: str) -> str | None:
    """Recursively search for logical shortcuts in Start Menu (Windows)."""
    if _IS_LINUX:
        return None
    app_key = app_name.lower()
    
    for base_path in SHORTCUT_PATHS:
        if not os.path.isdir(base_path):
            continue
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file.lower().endswith(".lnk"):
                    name_without_ext = file.lower().replace(".lnk", "")
                    if app_key == name_without_ext or app_key in name_without_ext:
                        return os.path.join(root, file)
    return None


def resolve_and_launch(app_name: str) -> tuple[bool, str]:
    """
    Robust cross-platform discovery strategy:
    1. Check Running -> Focus
    2. Shell Direct (PATH apps)
    3. Linux: .desktop file search / Windows: Start Menu search
    """
    app_key = app_name.lower().strip()

    # Step 1: Running Process Check
    if focus_window(app_key):
        return True, f"{app_key} is already running."

    # Step 2: Shell Direct (PATH apps)
    if _IS_LINUX:
        binary = shutil.which(app_key)
        if binary:
            try:
                subprocess.Popen(
                    [binary],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True
                )
                return True, f"Opening {app_key}."
            except Exception as e:
                print(f"[RESOLVER] Error launching {binary}: {e}")
    else:
        try:
            result = subprocess.run(
                f"where {app_key}",
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=True
            )
            if result.returncode == 0:
                subprocess.Popen(app_key, shell=True)
                return True, f"Opening {app_key}."
        except Exception:
            pass

    # Step 3: Deep Search
    if _IS_LINUX:
        exec_cmd = _search_linux_desktop_files(app_key)
        if exec_cmd:
            try:
                subprocess.Popen(
                    exec_cmd.split(),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True
                )
                return True, f"Opening {app_key}."
            except Exception as e:
                print(f"[RESOLVER] Error launching from .desktop: {e}")
    else:
        shortcut = search_start_menu(app_key)
        if shortcut:
            try:
                os.startfile(shortcut)
                return True, f"Opening {app_key}."
            except Exception as e:
                print(f"[RESOLVER] Error launching shortcut: {e}")
            
    return False, ""  # Silent failure
