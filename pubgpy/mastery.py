from .models import BaseModel, PUBGModel


class Weapon(BaseModel, PUBGModel):
    def __init__(self, data):
        self.data = data

        self.type = self.data.get("type", "weaponMasterySummary")
        self.id = self.data.get("id")
        
        super(BaseModel, self).__init__(data)
        super(PUBGModel, self).__init__(self.id, self.type)

        # attributes
        attributes = self.data.get("attributes")
        self.platform = attributes.get("platform")
        self.latest_match = attributes.get("latestMatchId")
        
        self.summaries = list()
        summaries = attributes.get("weaponSummaries")
        for x in summaries.keys():
            self.summaries.append()


class weaponSummary(BaseModel):
    def __init__(self, data):
        self.data = data
        super(BaseModel, self).__init__(data)

        self.xp = self.data.get("XPTotal")
        self.level = self.data.get("LevelCurrent")
        self.tier = self.data.get("TierCurrent")
        self.xp = self.data.get("XPTotal")
        self.stats = self.data.get("StatsTotal")

        self.medal = list()
        for i in self.data.get("Medals"):
            self.medal.append(Medal(i))


class Medal(BaseModel):
    def __init__(self, data)
        self.data = data

        super(BaseModel, self).__init__(data)
        self.id = self.data.get("MedalId")
        self.count = self.data.get("Count")


# Todo > Weapon Stat 작업, Survival 작업