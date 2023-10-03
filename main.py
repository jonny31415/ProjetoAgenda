from Agenda import Agenda
from UI import CLI
from Activity import ActivityHandler

def main():
    ui = CLI()
    act_hand = ActivityHandler()
    agenda = Agenda(ui, act_hand)

if __name__=='__main__':
    main()