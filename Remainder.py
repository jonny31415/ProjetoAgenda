from win10toast_click import ToastNotifier
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
    
def run_agenda() -> None:
    subprocess.run(["cmd", "/c", f"start /B {FOLDER_PATH}/run_agenda.vbs"])

def show_toast(act: Activity, act_hand: ActivityHandler):
    if act.date.date() != datetime.today().date():
        return
    message = f"You have an activity at {datetime.strftime(act.time, '%H:%M')}"
    toast = ToastNotifier()
    toast.show_toast(TITLE, message, icon_path=ICON_PATH, duration=DURATION, threaded=THREADED, callback_on_click=run_agenda)
    return schedule.CancelJob

def main() -> None:

    save_pid()
    act_hand = ActivityHandler()
    act_list: list[(int, Activity)] = act_hand.get_activities()
    for act in act_list:
        if datetime.combine(act[1].date.date(), act[1].time.time()) < datetime.now():
            act_hand.delete_activity(act[0])
        remainder_time = act_hand.get_remainder_time(act[1])
        s = remainder_time.seconds
        hours, remainder = divmod(s, 3600)
        minutes, seconds = divmod(remainder, 60)
        schedule.every().day.at(f"{hours:02}:{minutes:02}:{seconds:02}").do(show_toast, act=act[1], act_hand=act_hand)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()