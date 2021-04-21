from .models import BaseModel, PUBGModel


class Weapon(PUBGModel):
    def __init__(self, data):
        self.data = data

        self.type = self.data.get("type", "weaponMasterySummary")
        self.id = self.data.get("id")
        
        super().__init__(self)

        # attributes
        attributes = self.data.get("attributes")
        self.platform = attributes.get("platform")
        self.latest_match = attributes.get("latestMatchId")
        
        self.summaries = list()
        summaries = attributes.get("weaponSummaries")
        for x in summaries.keys():
            self.summaries.append(WeaponSummary(x))


class WeaponSummary(BaseModel):
    def __init__(self, data):
        self.data = data
        super(BaseModel, self).__init__(data)

        self.xp = self.data.get("XPTotal")
        self.level = self.data.get("LevelCurrent")
        self.tier = self.data.get("TierCurrent")
        self.xp = self.data.get("XPTotal")

        # Stats
        stats = self.data.get("StatsTotal")
        self.most_defeats = stats.get("MostDefeatsInAGame")
        self.defeats = stats.get("Defeats")
        self.defeats = stats.get("Defeats")
        self.most_headshots = stats.get("MostHeadShotsInAGame")
        self.headshots = stats.get("HeadShots")
        self.longest_defeat = stats.get("LongestDefeat")
        self.long_range_defeat = stats.get("LongRangeDefeats")
        self.kills = stats.get("Kills")
        self.most_kills = stats.get("MostKillsInAGame")
        self.groggies = stats.get("Groggies")
        self.most_groggies = stats.get("MostGroggiesInAGame")

        self.medal = list()
        for i in self.data.get("Medals"):
            self.medal.append(Medal(i))


class Medal(BaseModel):
    def __init__(self, data):
        self.data = data

        super().__init__(data)
        self.id = self.data.get("MedalId")
        self.count = self.data.get("Count")


class Survival(PUBGModel):
    def __init__(self, data):
        self.data = data

        self.type = self.data.get("type", "survivalMasterySummary")
        self.id = self.data.get("id")
        super().__init__(self)

        attributes = self.data.get("attributes")
        self.xp = attributes.get("xp")
        self.level = attributes.get("level")
        self.round_played = attributes.get("totalMatchesPlayed")
        self.last_match = attributes.get("latestMatchId")

        stats = attributes.get("stats")
        self.air_drops = Stats(stats.get("airDropsCalled"))
        self.damage_dealt = Stats(stats.get("damageDealt"))
        self.damage_taken = Stats(stats.get("damageTaken"))
        self.swimming = Stats(stats.get("distanceBySwimming"))
        self.vehicle = Stats(stats.get("distanceByVehicle"))
        self.foot = Stats(stats.get("distanceByFoot"))
        self.distance = Stats(stats.get("distanceTotal"))
        self.healed = Stats(stats.get("healed"))
        self.hot_drop = Stats(stats.get("hotDropLandings"))
        self.enemy_crates = Stats(stats.get("enemyCratesLooted"))
        self.position = Stats(stats.get("position"))
        self.revived = Stats(stats.get("revived"))
        self.teammates_revived = Stats(stats.get("teammatesRevived"))
        self.time_survived = Stats(stats.get("timeSurvived"))
        self.throwable = Stats(stats.get("throwablesThrown"))
        self.top10 = Stats(stats.get("top10"))


class Stats(BaseModel):
    def __init__(self, data):
        super().__init__(data)
        self.data = data

        self.total = self.data.get("total")
        self.average = self.data.get("average")
        self.career = self.data.get("careerBest")
        self.last_match = self.data.get("lastMatchValue")
