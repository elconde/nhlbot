
class Player():

    def __init__(self, firstName, lastName, position):
        self.firstName = firstName
        self.lastName = lastName
        self.position = position 

    def __repr__(self):
        return self.firstName + " " + self.lastName
