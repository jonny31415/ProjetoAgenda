from typing import Protocol
from datetime import datetime
import calendar
import customtkinter


class UI(Protocol):
    def render_calendar(month: int, year: int) -> None:
        NotImplementedError()
    def render_activities(day: int) -> None:
        NotImplementedError()

class CLI:
    def render_calendar(self, month: int = datetime.now().month, year: int = datetime.now().year) -> None:
        print(calendar.month(year,month))
    def render_activities(day: int) -> None:
        pass

class GUI:
    pass