class ActorsData:

    def __init__(self, id, shortName, longName):
        self.id = id
        self.shortName = shortName
        self.longName = longName

    def __repr__(self):
        return str(self.id) + " " + self.shortName + " " + self.longName
