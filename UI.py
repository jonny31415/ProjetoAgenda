from typing import Callable
from datetime import datetime
import calendar
import customtkinter
from tkcalendar import Calendar
import tkinter as tk
import os
from PIL import Image
from pathlib import Path
import sys

from Activity import Activity, ActivityHandler
from Remainder import update_remainder

FOLDER_PATH =  str(Path(Path(__file__).parent.absolute()))
sys.path.insert(0, FOLDER_PATH)

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

class GUI(customtkinter.CTk):
    def __init__(self, activity_handler: ActivityHandler):
        super().__init__()

        self.activity_handler = activity_handler
        self.create_ui()
    
    def create_ui(self) -> None:
        self.title("MyTaskNotes Beta")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.callbacks = {}

        self.home_frame = HomeFrame(self)
        self.calendar_frame = CalendarFrame(self)
        self.activities_frame = ActivitiesFrame(self)
        self.day_frame = DayFrame(self)
        self.navigation_frame = NavigationFrame(self)
    
    def day_frame_update(self, day=None):
        self.day_frame = DayFrame(self.master, date=day)
        self.navigation_frame.select_frame_by_name("day_frame")



class NavigationFrame(customtkinter.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)
    
        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "UI_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.calendar_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "calendar_dark2.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "calendar_light2.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        

        # Create navigation frame
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self, text="  MyTaskNotes", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.calendar_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Calendar",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.calendar_image, anchor="w", command=self.calendar_button_event)
        self.calendar_button.grid(row=2, column=0, sticky="ew")

        self.activities_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Activities",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.calendar_image, anchor="w", command=self.activities_button_event)
        self.activities_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self, values=["Dark", "Light", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # Select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # Set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.calendar_button.configure(fg_color=("gray75", "gray25") if name == "calendar" else "transparent")

        # Show selected frame
        if name == "home":
            self.master.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.master.home_frame.grid_forget()
        if name == "calendar":
            self.master.calendar_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.master.calendar_frame.grid_forget()
        if name == "day_frame":
            self.master.day_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.master.day_frame.grid_forget()
        if name == "activities":
            self.master.activities_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.master.activities_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def calendar_button_event(self):
        self.select_frame_by_name("calendar")
    
    def activities_button_event(self):
        self.select_frame_by_name("activities")
    
    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
        

class HomeFrame(customtkinter.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)

        self.activities_list = self.master.activity_handler.get_activities()
        if not self.activities_list:
            self.no_activities_label = customtkinter.CTkLabel(self, text="No Activities")
            self.no_activities_label.grid(row=0, column=0, columnspan=2)
        else:
            self.next_date = self.activities_list[0][1].date
            self.next_time = self.activities_list[0][1].time
            self.next_remainder = self.activities_list[0][1].remainder
            self.next_message = self.activities_list[0][1].message

            self.next_activity_label = customtkinter.CTkLabel(self, text="Next Activity:")
            self.next_activity_label.grid(row=0, column=0, columnspan=2)
            self.date_label = customtkinter.CTkLabel(self, text=f"Date: {self.next_date}")
            self.date_label.grid(row=1, column=0)
            self.time_label = customtkinter.CTkLabel(self, text=f"Time: {self.next_time}")
            self.time_label.grid(row=1, column=1)
            self.remainder_label = customtkinter.CTkLabel(self, text=f"Remainder: {self.next_remainder}")
            self.remainder_label.grid(row=2, column=0)
            self.message_label = customtkinter.CTkLabel(self, text=f"Message: {self.next_message}")
            self.message_label.grid(row=2, column=1)


class CalendarFrame(customtkinter.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)

        self.event_list = []
        
        # Create Calendar  
        # self.calendar = MyCalendar(self)
        # self.calendar.pack()
        self.calendar = Calendar(self, selectmode='day', firstweekday = 'sunday',
                                showweeknumbers=False, cursor="hand2", date_pattern= 'dd-mm-y',
                                background="black", disabledbackground="black", bordercolor="black", 
                                headersbackground="black", normalbackground="black", foreground='white', 
                                normalforeground='white', headersforeground='white',
                                weekendbackground="gray50", othermonthbackground="gray75")
        self.calendar.pack(fill="both", expand=True)
        self.calendar.bind('<<CalendarMonthChanged>>', self._show_month_events)
        self.calendar.bind('<<CalendarSelected>>', self.get_day_frame)
        # https://stackoverflow.com/questions/61493630/is-there-a-way-to-change-tkcalendars-color
        # https://stackoverflow.com/questions/52515099/tkinter-tkcalendar-to-display-events
    
    # TODO: events in calendar ----------------------------
    def update_cal_events(self, act_list: list[Activity]) -> None:
        self.event_list = []
        print("aqui")
        for act in act_list:
            self.event_list.append((act.date, act.remainder, act.message))

    def _show_month_events(self, event) -> None:
        # remove previously displayed events
        self.calendar.calevent_remove('all')
        # month, year = self.calendar.get_displayed_month_year()
        for e in self.event_list:
            # if event[0].month == month and event[0].year == year:
            self.calendar.calevent_create(e[0], e[1], e[2])
    # -----------------------------------------------------------

    def get_day_frame(self, event=None) -> None:
        date = datetime.strptime(self.calendar.get_date(),"%d-%m-%Y")
        self.master.day_frame_update(date)

class ActivitiesFrame(customtkinter.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)

        self.activities_list = self.master.activity_handler.get_activities()
        if not self.activities_list:
            self.no_activities_label = customtkinter.CTkLabel(self, text="No Activities")
            self.no_activities_label.grid(row=0, column=0, columnspan=2)
        else:
            self.task_list = ScrollableRadiobuttonFrame(self, item_list=self.activities_list)
            self.task_list.pack(fill=tk.X)
            


ADD_BTN_TXT = "Add"
EDIT_BTN_TXT = "Edit"
DELETE_BTN_TXT = "Delete"

class DayFrame(customtkinter.CTkFrame):
    def __init__(self, master, date=None) -> None:
        super().__init__(master)

        if not date:
            date = datetime(datetime.now().year, datetime.now().month, datetime.now().day) 
        self.date = date

        self.task_list = ScrollableRadiobuttonFrame(self, item_list=[], command=self.on_select_activity)
        self.task_list.pack(fill=tk.X)

        self.add_task_button = customtkinter.CTkButton(
            self,
            text=ADD_BTN_TXT,
            width=100,
        )

        self.edit_task_button = customtkinter.CTkButton(
            self,
            text=EDIT_BTN_TXT,
            width=100,
            state=tk.DISABLED,
        )

        self.del_task_button = customtkinter.CTkButton(
            self,
            text=DELETE_BTN_TXT,
            width=100,
            state=tk.DISABLED,
        )
        self.add_task_button.pack(side=tk.LEFT, anchor=tk.NW, padx=20)
        self.edit_task_button.pack(side=tk.LEFT, anchor=tk.N, padx=20)
        self.del_task_button.pack(side=tk.LEFT, anchor=tk.NE, padx=20)

        self.bind_delete_activity(self.delete_activity)
        self.bind_edit_activity(self.edit_activity)
        self.bind_add_activity(self.add_activity)
        
        self.update_activity_list()
    
    def add_activity(self, event=None) -> None:
        self.add_toplevel = AddEditWindow(self.update_add_activity)
    
    def edit_activity(self, event=None) -> None:
        splitted= self.selected_task.split(",")
        id = splitted[0][1:]
        splitted2 = splitted[1].split(" ")
        date = splitted2[2][:10]
        time = splitted2[3][:5]
        remainder = splitted2[4][:5]
        message = splitted2[5][:-2]
        activity = Activity(datetime.strptime(date, "%d/%m/%Y"), datetime.strptime(time, "%H:%M"), datetime.strptime(remainder, "%H:%M"), message)
        self.add_toplevel = AddEditWindow(self.update_edit_activity, act_id=id, activity=activity)
    
    def delete_activity(self, event=None) -> None:
        self.master.activity_handler.delete_activity(id=self.selected_task.split(",")[0][1:])
        self.update_activity_list()
        self.operation_successful = OperationSuccessful("Delete")
        update_remainder()
    
    def bind_delete_activity(self, method: Callable[[tk.Event], None]) -> None:
        self.del_task_button.bind("<Button-1>", method)
    
    def bind_edit_activity(self, method: Callable[[tk.Event], None]) -> None:
        self.edit_task_button.bind("<Button-1>", method)

    def bind_add_activity(self, method: Callable[[tk.Event], None]) -> None:
        self.add_task_button.bind("<Button-1>", method)

    def update_add_activity(self, _, time, remainder, message):
        if isinstance(time, str):
            time = datetime.strptime(time, "%Hh%M")
        if isinstance(remainder, str):
            remainder = datetime.strptime(remainder, "%Hh%M")
        activity = Activity(self.date, time, remainder, message)
        self.master.activity_handler.add_activity(activity)
        self.update_activity_list()
        self.operation_successful = OperationSuccessful("Add")
        update_remainder()
        

    def update_edit_activity(self, act_id, time, remainder, message):
        if isinstance(time, str):
            time = datetime.strptime(time, "%Hh%M")
        if isinstance(remainder, str):
            remainder = datetime.strptime(remainder, "%Hh%M")
        activity = Activity(self.date, time, remainder, message)
        self.master.activity_handler.edit_activity(id=act_id, act=activity)
        self.update_activity_list()
        self.operation_successful = OperationSuccessful("Edit")
        update_remainder()

    @property
    def selected_task(self) -> str:
        return self.task_list.get_checked_item()

    def on_select_activity(self, event=None) -> None:
        self.edit_task_button.configure(state=tk.NORMAL)
        self.del_task_button.configure(state=tk.NORMAL)

    def on_focus_out(self, event=None) -> None:
        self.task_list.selection_clear(0, tk.END)
        self.del_task_button.configure(state=tk.DISABLED)

    def update_activity_list(self) -> None:
        self.task_list.update_list(self.master.activity_handler.get_day_activities(self.date))


class ScrollableRadiobuttonFrame(customtkinter.CTkScrollableFrame): # TODO: Solve edit and delete buttons active after deleting activities 
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.radiobutton_list = []
        for _, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        radiobutton = customtkinter.CTkRadioButton(self, text=item[1], value=item, variable=self.radiobutton_variable)
        if self.command is not None:
            radiobutton.configure(command=self.command)
        radiobutton.grid(row=len(self.radiobutton_list), column=0, pady=(0, 10), sticky="w")
        self.radiobutton_list.append(radiobutton)

    def remove_item(self, item):
        for radiobutton in self.radiobutton_list:
            if item == radiobutton.cget("text"):
                radiobutton.destroy()
                self.radiobutton_list.remove(radiobutton)
                return
    
    def update_list(self, item_list):
        for radiobutton in self.radiobutton_list:
            radiobutton.destroy()
        self.radiobutton_list = []
        for item in item_list:
            self.add_item(item)

    def get_checked_item(self):
        return self.radiobutton_variable.get()
    

class AddEditWindow:
    def __init__(self, update, act_id:int = None, activity: Activity = None):
        self.top = customtkinter.CTkToplevel()
        self.top.geometry("400x400")
        self.time_frame = customtkinter.CTkFrame(self.top, fg_color="transparent")
        self.remainder_frame = customtkinter.CTkFrame(self.top, fg_color="transparent")
        self.message_frame = customtkinter.CTkFrame(self.top, fg_color="transparent")
        self.add_frame = customtkinter.CTkFrame(self.top, fg_color="transparent")

        self.act_id = act_id
        
        if activity:
            self.time = activity.time
            self.remainder = activity.remainder
            self.message = activity.message
            self.top.title("Edit Activity")
            self.button_name = "Edit"
        else:
            self.time = None
            self.remainder = None
            self.message = None
            self.top.title("Add Activity") 
            self.button_name = "Add"

        self.time_label = customtkinter.CTkLabel(self.time_frame, text=f"Time: {datetime.strftime(self.time, '%Hh%M') if self.time else None}")
        self.time_button = customtkinter.CTkButton(self.time_frame, text="Configure Time", command=self.get_time_dialog_event)
        self.time_button.pack(side=tk.LEFT, padx=10, pady=5)
        self.time_label.pack(side=tk.LEFT, padx=10, pady=5)

        self.remainder_label = customtkinter.CTkLabel(self.remainder_frame, text=f"Remainder: {datetime.strftime(self.remainder, '%Hh%M') if self.remainder else None}")
        self.remainder_button = customtkinter.CTkButton(self.remainder_frame, text="Configure Remainder", command=self.get_remainder_dialog_event)
        self.remainder_button.pack(side=tk.LEFT, padx=10, pady=5)
        self.remainder_label.pack(side=tk.LEFT, padx=10, pady=5)

        self.message_label = customtkinter.CTkLabel(self.message_frame, text=f"Message: {self.message}")
        self.message_button = customtkinter.CTkButton(self.message_frame, text="Configure Message", command=self.get_message_dialog_event)
        self.message_button.pack(side=tk.LEFT, padx=10, pady=5)
        self.message_label.pack(side=tk.LEFT, padx=10, pady=5)

        self.submit_button = customtkinter.CTkButton(self.add_frame, text=self.button_name, command=self.submit, state=tk.DISABLED)
        self.submit_button.pack(side=tk.TOP, padx=10, pady=10)

        self.time_frame.pack(padx=10, pady=10)
        self.remainder_frame.pack(padx=10, pady=10)
        self.message_frame.pack(padx=10, pady=10)
        self.add_frame.pack(padx=10, pady=10)

        self.update = update

    def get_time_dialog_event(self) -> None:
        dialog = customtkinter.CTkInputDialog(text="Time (--h-- format):", title="CTkInputDialog")
        self.time = dialog.get_input()
        self.time_label.configure(text=f"Time: {self.time}")
        self.update_button()
    
    def get_remainder_dialog_event(self) -> None:
        dialog = customtkinter.CTkInputDialog(text="Remainder (--h-- format):", title="CTkInputDialog")
        self.remainder = dialog.get_input()
        self.remainder_label.configure(text=f"Remainder: {self.remainder}")
        self.update_button()
    
    def get_message_dialog_event(self) -> None:
        dialog = customtkinter.CTkInputDialog(text="Message:", title="CTkInputDialog")
        self.message = dialog.get_input()
        self.message_label.configure(text=f"Message: {self.message}")
        self.update_button()    
    
    def update_button(self) -> None:    
        if self.time and self.remainder and self.message:
            self.submit_button.configure(state=tk.NORMAL)
        else:
            self.submit_button.configure(state=tk.DISABLED)
    
    def submit(self) -> None:
        self.update(self.act_id, self.time, self.remainder, self.message) 
        self.top.destroy()


class OperationSuccessful:
    def __init__(self, type: str):
        self.top = customtkinter.CTkToplevel()
        self.top.geometry("400x400")
        self.top.title("Success!")
        self.frame = customtkinter.CTkFrame(self.top, fg_color="transparent") # TODO: Change fontsize
        self.label = customtkinter.CTkLabel(self.frame, text=f"{type} successfully!")
        self.button = customtkinter.CTkButton(self.frame, text="Ok", command=self.top.destroy)
        self.label.pack(padx=10, pady=10)  
        self.button.pack(padx=10, pady=10) 
        self.frame.pack(padx=10, pady=10)