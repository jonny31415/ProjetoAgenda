from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import sqlite3

SAVE_PATH = "Activities/"

class ActionTypes(Enum):
    CHANGE_DATE = 1
    ADD_ACT = 2
    EDIT_ACT = 3
    DELETE_ACT = 4

@dataclass
class Activity:
    date: datetime  # Date and time of activity
    time: datetime  # Time of activity
    remainder: datetime # Remainder time before activity
    message: str

class ActivityHandler:
    def __init__(self) -> None:
        self.table_name = "activities"
        self.connection = sqlite3.connect("activities.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"create table if not exists {self.table_name}\
                             (id integer primary key autoincrement, date datetime, time datetime, remainder integer, message text)")
    
    def add_activity(self, act: Activity) -> None:
        self.cursor.execute(f"insert into {self.table_name} values (?,?,?,?,?)", (None, act.date, act. time, act.remainder, act.message))
        self.connection.commit()
    
    def edit_activity(self, id: int, act: Activity) -> None:
        self.cursor.execute(f"update {self.table_name} set date=?, time=?, remainder=?, message=? where id=?", (act.date, act.time, act.remainder, act.message, id))
        self.connection.commit() 
    
    def delete_activity(self, id: int) -> None:
        self.cursor.execute(f"delete from {self.table_name} where id = ?", (id,))
        self.connection.commit()
    
    def get_activities(self) -> list[tuple, Activity]:
        activities: list[tuple[int, Activity]] = []
        for row in self.cursor.execute(f"select id, date, time, remainder, message from {self.table_name}"):
            act = Activity(row[1], row[2], row[3])
            activities.append((row[0], act))    # TODO: Correct id problem
        return activities

    def get_day_activities(self, date: datetime) -> list[tuple, Activity]:
        activities: list[tuple[int, Activity]] = []
        for row in self.cursor.execute(f"select id, time, remainder, message from {self.table_name} where date = ?", (date,)):
            act = Activity(date, row[1], row[2], row[3])
            activities.append((row[0], act))    # TODO: Correct id problem
        return activities