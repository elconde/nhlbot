from datetime import datetime
import Team
import threading

class GameTracking( threading.Thread ):

    def __init__(self, gameObj):
        self.gameObj = gameObj
        threading.Thread.__init__(self)
        self.tracking.halt = False
        self.pollTime = 60

    def run(self):
        pass 

class Game():
    def __init__(self, home_team, away_team, date, tracking):
        self.home_team = home_team
        self.away_team = away_team
        
        self.home_score = 0
        self.away_score = 0
        self.scorers = []
        
        self.date = date
        if tracking is True:
            self.tracking = GameTracking(self)

    def __repr__(self):
        return str(self.home_team) + " vs " + str(self.away_team) + \
                " on " + self.date.strftime("%a %b %d at %I:%M%p")

    def enable_tracking(self):
        if tracking is not None:
            raise RuntimeWarning("Error: Tracking thread already active for Game " + self)
        else:
            self.tracking = GameTracking(self)

    def disable_tracking(self):
        if tracking is None:
            raise RuntimeWarning("Error: Tracking is already disabled for Game " + self)
        else:
            self.tracking.halt = True
            self.tracking.join(30.0)

            if self.tracking.isAlive():
                raise RuntimeError("Unable to kill tracking thread for " + self)

    def goal(self, team):
        if team == self.home_team:
            self.home_score += 1
        elif team == self.away_team:
            self.away_score += 1
        else:
            raise RuntimeError("Goal for Team " + team + " is invalid for Game " + self)
