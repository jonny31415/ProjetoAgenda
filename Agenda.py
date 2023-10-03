from UI import UI
from Activity import Activity, ActivityHandler

class Agenda:
    def __init__(self, ui: UI, activity_handler: ActivityHandler) -> None:
        self.ui = ui    
        self.activity_handler = activity_handler
        self.activities = []

        self.initialize()
    
    def initialize(self):
        self.ui.render_calendar()
    