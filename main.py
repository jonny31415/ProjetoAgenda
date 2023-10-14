from Agenda import Agenda
from UI import GUI
from Activity import ActivityHandler

def main():
    act_hand = ActivityHandler()
    ui = GUI(act_hand)
    agenda = Agenda(ui, act_hand)
    agenda.run()

    # TODO: Create installer: https://www.pythonguis.com/tutorials/packaging-pyside6-applications-windows-pyinstaller-installforge/

if __name__=='__main__':
    main()