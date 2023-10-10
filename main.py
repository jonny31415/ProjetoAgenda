from Agenda import Agenda
from UI import CLI, GUI
from Activity import ActivityHandler

def main():
    act_hand = ActivityHandler()
    ui = GUI(act_hand)
    agenda = Agenda(ui, act_hand)
    agenda.run()

if __name__=='__main__':
    main()