import threading
from Brain.gpt_brain import ask_gpt
from internet_check import is_Online
from Alert import Alert
from Data.DLG_Data import online_dlg,offline_dlg
import random
from co_brain import Jarvis
from Brain.personality import jarvis_speak
from Automation.Battery  import check_plug
from Time_Operations.throw_alert import check_schedule,check_Alam
from os import getcwd

import os

# ─────────────────────────────────────────────
#  PATH SETUP — all data files relative to CWD
# ─────────────────────────────────────────────
PROJECT_ROOT = getcwd()
Alam_path = os.path.join(PROJECT_ROOT, "Alam_data.txt")
file_path = os.path.join(PROJECT_ROOT, "schedule.txt")
input_file = os.path.join(PROJECT_ROOT, "input.txt")


def _ensure_data_files():
    """Create required data files if they don't exist (first-run safety)."""
    for fpath in [Alam_path, file_path, input_file]:
        if not os.path.exists(fpath):
            with open(fpath, 'w') as f:
                f.write("")
            print(f"[INIT] Created missing file: {fpath}")


ran_online_dlg = random.choice(online_dlg)
ran_offline_dlg = random.choice(offline_dlg)


def main():
    # Ensure all data files exist before any thread tries to read them
    _ensure_data_files()

    if is_Online():
        t1 = threading.Thread(target=jarvis_speak,args=(ran_online_dlg,))
        t3 = threading.Thread(target=check_plug)
        t4 = threading.Thread(target=check_schedule,args=(file_path,))
        t5 = threading.Thread(target=Jarvis)
        t6 = threading.Thread(target=check_Alam,args=(Alam_path,))
        t1.start()
        t1.join()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
    else:
        Alert(ran_offline_dlg)

main()