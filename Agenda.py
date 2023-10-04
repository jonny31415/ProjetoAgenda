from UI import UI
from Activity import Activity, ActivityHandler, ActionTypes

class Agenda:
    def __init__(self, ui: UI, activity_handler: ActivityHandler) -> None:
        self.ui = ui    
        self.activity_handler = activity_handler

        self.main_loop()
    
    def main_loop(self):
        while(True):
            self.ui.render_calendar()
            option = self.ui.render_activity_options()
            if option == ActionTypes.CHANGE_DATE.value:
                self.ui.render_change_date()
                self.ui.render_calendar()
            elif option == ActionTypes.ADD_ACT.value:
                date, remainder, message = self.ui.render_add_activity()
                act = Activity(date=date, remainder=remainder, message=message)
                self.activity_handler.add_activity(act=act) 
            elif option == ActionTypes.EDIT_ACT.value:
                act_list = self.activity_handler.get_activities()
                id, date, remainder, message = self.ui.render_edit_activity(act_list=act_list)
                act = Activity(date=date, remainder=remainder, message=message)
                self.activity_handler.edit_activity(id, act)
            elif option == ActionTypes.DELETE_ACT.value:
                act_list = self.activity_handler.get_activities()
                id = self.ui.render_delete_activity(act_list=act_list)
                self.activity_handler.delete_activity(id=id)
            else:
                raise TypeError()

