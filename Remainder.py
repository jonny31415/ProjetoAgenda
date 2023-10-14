from win10toast import ToastNotifier
import schedule
from datetime import datetime
import time
from pathlib import Path
import sys
import os
import subprocess
from Activity import Activity, ActivityHandler

FOLDER_PATH =  str(Path(Path(__file__).parent.absolute()))
sys.path.insert(0, FOLDER_PATH)

TITLE = "MyTaskNotes"
DURATION = 10
ICON_PATH = FOLDER_PATH+"\\UI_images\\icon.ico"
THREADED = True

PID_FILE = FOLDER_PATH+"\\pid.bin"

def update_remainder() -> None:
    subprocess.run(["cmd", "/c", "taskkill", "/F", "/PID", str(read_pid())]) # Kill remainder.py process 
    subprocess.run(["cmd", "/c", f"start /B {FOLDER_PATH}/run_remainder.vbs"]) # Run remainder.py again to update schedule

def save_pid() -> None:
    with open(PID_FILE, "wb") as file:
        file.write(os.getpid().to_bytes(4, "little"))

def read_pid() -> int:
    with open(PID_FILE, "rb") as file:
        return int.from_bytes(file.read(), "little")

def show_toast(id: int, act: Activity, act_hand: ActivityHandler) -> None:
    if act.date.date() != datetime.today().date():
        return
    message = f"You have an activity at {datetime.strftime(act.time, '%H:%M')}"
    toast = ToastNotifier()
    toast.show_toast(TITLE, message, icon_path=ICON_PATH, duration=DURATION, threaded=THREADED)
    act_hand.delete_activity(id)
    return schedule.CancelJob

def main() -> None:

    save_pid()
    act_hand = ActivityHandler()
    act_list: list[(int, Activity)] = act_hand.get_activities()
    print(act_list)
    for act in act_list:
        remainder_time = act_hand.get_remainder_time(act[1])
        schedule.every().day.at(str(remainder_time)).do(show_toast, id=act[0], act=act[1], act_hand=act_hand)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()