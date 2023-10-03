from dataclasses import dataclass
from datetime import datetime

@dataclass
class Activity:
    date: datetime  # Date and time of activity
    remainder: datetime # Remainder time before activity
    message: str

class ActivityHandler:
    def new_activity(self, new_act: Activity) -> None:
        pass
    def edit_activity(self, edit_act: Activity) -> None:
        pass
    def remove_activity(self, rem_act: Activity) -> None:
        pass