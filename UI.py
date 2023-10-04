from typing import Protocol
from datetime import datetime
import calendar
import customtkinter

from Activity import Activity


class UI(Protocol):
    def render_calendar(self) -> None:
        NotImplementedError()

    def render_activities(self, day: int) -> None:
        NotImplementedError()

    def render_activity_options(self) -> int:
        NotImplementedError()

    def render_change_date(self) -> None:
        NotImplementedError()

    def render_add_activity(self) -> tuple[int, int, str]:
        NotImplementedError()

    def render_edit_activity(self) -> tuple[int, int, int, str]:
        NotImplementedError()

    def render_delete_activity(self) -> int:
        NotImplementedError()

class CLI:
    def __init__(self):
        self.month = datetime.now().month
        self.year = datetime.now().year

    def render_calendar(self) -> None:
        print(f"\n{calendar.month(self.year,self.month)}")

    def render_activities(self, act_list: list[tuple[int, Activity]]) -> None:
        print("Available activities:")
        for act in act_list:
            print(f"{act[0]}:\nDate: {act[1].date}\nRemainder: {act[1].remainder}\nMessage: {act[1].message}\n")

    def render_activity_options(self) -> int:
        print("What would you like to do?")
        print("1. Change Month/Year")
        print("2. Add activity")
        print("3. Edit activity")
        print("4. Delete activity")
        option = int(input("Option:"))
        return option
    
    def render_change_date(self) -> None:
        print("Choose month and year:")
        self.month = int(input("Month:"))
        self.year = int(input("Year:"))
    
    def render_add_activity(self) -> tuple[int, int, str]:
        day = int(input("Day of your activity:"))
        remainder = int(input("Time for the remainder (in hours): "))
        message = input("Message or name of the activity:")
        date = datetime(self.year, self.month, day)
        print("\nSuccessfully added activity!")
        return date, remainder, message
    
    def render_edit_activity(self, act_list: list[tuple[int, Activity]]) -> tuple[int, int, int, str]:
        self.render_activities(act_list)
        print("Which activity do you want to edit?")
        id = input("Insert activity id:")
        day = int(input("Day of your activity:"))
        remainder = int(input("Time for the remainder (in hours): "))
        message = input("Message or name of the activity:")
        date = datetime(self.year, self.month, day)
        print("\nSuccessfully edited activity!")
        return id, date, remainder, message

    def render_delete_activity(self, act_list: list[tuple[int, Activity]]) -> int:
        self.render_activities(act_list)
        print("Which activity do you want to remove?")
        id = input("Insert activity id:")
        print("\nSuccessfully deleted activity!")
        return id

class GUI:
    pass