from UI import GUI
from Activity import Activity, ActivityHandler, ActionTypes

class Agenda:
    def __init__(self, ui: GUI, activity_handler: ActivityHandler) -> None:
        self.ui = ui    
        self.activity_handler = activity_handler
        self.ui.day_frame.get_callbacks([("delete_activity", self.delete_activity), ("add_activity", self.add_activity)])
        self.ui.day_frame.bind_callbacks()

        self.ui.mainloop()

    def add_activity(self, event=None) -> None:
        print("add")
        activity = self.ui.day_frame.get_entry_text()
        self.ui.day_frame.clear_entry()
        self.activity_handler.add_activity(activity)
        self.ui.day_frame.update_activity_list()

    def delete_activity(self, event=None) -> None:
        print("oi")
        self.activity_handler.delete_activity(self.ui.selected_task)
        self.ui.day_frame.update_task_list()
    
    def run(self) -> None:
            self.ui.mainloop()
            # while(True):
            #     self.ui.render_calendar()
            #     option = self.ui.render_activity_options()
            #     if option == ActionTypes.CHANGE_DATE.value:
            #         self.ui.render_change_date()
            #         self.ui.render_calendar()
            #     elif option == ActionTypes.ADD_ACT.value:
            #         date, remainder, message = self.ui.render_add_activity()
            #         act = Activity(date=date, remainder=remainder, message=message)
            #         self.activity_handler.add_activity(act=act) 
            #     elif option == ActionTypes.EDIT_ACT.value:
            #         act_list = self.activity_handler.get_activities()
            #         id, date, remainder, message = self.ui.render_edit_activity(act_list=act_list)
            #         act = Activity(date=date, remainder=remainder, message=message)
            #         self.activity_handler.edit_activity(id, act)
            #     elif option == ActionTypes.DELETE_ACT.value:
            #         act_list = self.activity_handler.get_activities()
            #         id = self.ui.render_delete_activity(act_list=act_list)
            #         self.activity_handler.delete_activity(id=id)
            #     else:
            #         raise TypeError()

