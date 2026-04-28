import os
import time
import threading
from Alert import Alert
from Brain.personality import jarvis_speak
from Time_Operations.brain import input_manage
from os import getcwd

# ─────────────────────────────────────────────
#  SAFE FILE HELPERS
#  Auto-create data files if they don't exist.
#  Ensures the polling loops NEVER crash on first run.
# ─────────────────────────────────────────────

def _ensure_file_exists(file_path: str) -> None:
    """Create the file (and parent dirs) if it doesn't already exist."""
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write("")
        print(f"[INIT] Created missing data file: {file_path}")


def load_schedule(file_path):
    schedule = {}
    _ensure_file_exists(file_path)
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if '=' in line:
                    line_time, activity = line.strip().split(' = ', 1)
                    schedule[line_time.strip()] = activity.strip()
    except Exception as e:
        print(f"[SCHEDULE] Error loading schedule: {e}")
    return schedule

def check_schedule(file_path):
    _ensure_file_exists(file_path)
    last_modified = 0
    schedule = {}
    while True:
        current_time = time.strftime("%I:%M%p")
        try:
            # Check file modification time
            modified = os.path.getmtime(file_path)
            if modified != last_modified:
                last_modified = modified
                schedule = load_schedule(file_path)
            
            if current_time in schedule:
                text = schedule[current_time]
                t1 = threading.Thread(target=Alert, args=(text,))
                t2 = threading.Thread(target=jarvis_speak, args=(text,))
                t1.start()
                t2.start()
                t1.join()
                t2.join()
        
        except Exception as e:
            print(f"[SCHEDULE] Error: {e}")
        
        time.sleep(60)


def load_AlamTime(file_path):
    schedule = ""
    _ensure_file_exists(file_path)
    try:
        with open(file_path, 'r') as file:
            schedule = file.read()
    except Exception as e:
        print(f"[ALARM] Error loading alarm data: {e}")
    return schedule


def check_Alam(Alam_path):
    _ensure_file_exists(Alam_path)
    last_modified = 0
    schedule = ""
    while True:
        current_time = time.strftime("%I:%M%p")
        try:
            # Check file modification time
            modified = os.path.getmtime(Alam_path)
            if modified != last_modified:
                last_modified = modified
                schedule = load_AlamTime(Alam_path)
            
            if current_time in schedule:
                text = "This is Alarm"
                t1 = threading.Thread(target=Alert, args=(text,))
                t2 = threading.Thread(target=jarvis_speak, args=(text,))
                t1.start()
                t2.start()
                t1.join()
                t2.join()
        
        except Exception as e:
            print(f"[ALARM] Error: {e}")
        
        time.sleep(10)
