from Agenda import Agenda
from UI import CLI
from Activity import ActivityHandler

def main():
    act_hand = ActivityHandler()
    ui = CLI()
    agenda = Agenda(ui, act_hand)

if __name__=='__main__':
    main()