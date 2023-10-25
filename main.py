from Agenda import Agenda
from UI import GUI
from Activity import ActivityHandler
import sys

def main():

    # Check if Python version is 3.9 or higher
    if not sys.version_info > (3, 9):
        raise Exception("Python 3.9 or a more recent version is required.")

    act_hand = ActivityHandler()
    ui = GUI(act_hand)
    agenda = Agenda(ui, act_hand)
    agenda.run()

    # TODO: Create installer: https://www.pythonguis.com/tutorials/packaging-pyside6-applications-windows-pyinstaller-installforge/

if __name__=='__main__':
    main()