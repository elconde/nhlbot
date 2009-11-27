from nhlbot_syntax import *
from schedule.py import Schedule

def process_command(command):
    print "TODO"
    
def handle_next(s, loc, toks):
    sched = Schedule()

    if toks.at:
        return sched.next_at(Team(toks.team1[0]), Team(toks.team2[0]))
    else:
        return sched.next(Team(toks.team1[0]), Team(toks.team2[0]))



next_command.addParseAction(handle_next)
