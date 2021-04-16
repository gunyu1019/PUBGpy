from .models import BaseModel


class Player:
    def __init__(self, client, data):
        self.data = data
        self.client = client
        self.id = self.data.get("id")

        self.type = self.data.get("type", "Player")

#       Attributes
        self.name = self.data.get("attributes", {}).get("name")
        self.shard = self.data.get("attributes", {}).get("shardId")
        self.titleId = self.data.get("attributes", {}).get("titleId")
        self.stats = self.data.get("attributes", {}).get("stats")
        self.patchVersion = self.data.get("attributes", {}).get("patchVersion")

#       relationships
        self.assets = self.data.get("relationships", {}).get("assets", {}).get('data')
        self.matches = [_.get('id') for _ in self.data.get("relationships", {}).get("matches", {}).get('data', [])]

    def __dict__(self):
        return self.data

    def __eq__(self, other):
        return other.name == self.name and other.id == self.id and self.type == other.type

    def __repr__(self):
        return "Player(id='{}', name='{}', type='{}')".format(self.id, self.name, self.type)

    def __str__(self):
        return self.name

    async def current_season(self):
        if self.client is None:
            raise TypeError("missing 1 required positional argument: 'season'")
        seasons = await self.client.season()
        for i in seasons:
            if i.current:
                return i
        raise ValueError("Can not find current season.")

    async def season_stats(self, season: str = None):
        if season is None:
            season_fp = await self.current_season()
            season = season_fp.id
        path = "/players/{}/seasons/{}".format(self.id, season)
        resp = await self.client.requests.get(path=path)
        return GameMode(resp.get("data", {}).get("attributes", {}).get("gameModeStats", {}), SeasonStats)

    async def ranked_stats(self, season: str = None):
        if season is None:
            season_fp = await self.current_season()
            season = season_fp.id
        path = "/players/{}/seasons/{}/ranked".format(self.id, season)
        resp = await self.client.requests.get(path=path)
        return GameMode(resp.get("data", {}).get("attributes", {}).get("rankedGameModeStats", {}), RankedStats)

    async def match(self, position: int = 0):
        if position > len(self.matches):
            raise IndexError("list index out of Match List")
        return await self.client.matches(match_id=self.matches[position])


class SeasonStats(BaseModel):
    def __init__(self, data: dict):
        super().__init__(data)
        self.data = data

        self.assists = data.get("assists")
        self.boosts = data.get("boosts")
        self.dbnos = data.get("dBNOs")
        self.daily_kills = data.get("dailyKills")
        self.daily_wins = data.get("dailyWins")
        self.damage_dealt = data.get("damageDealt")
        self.days = data.get("days")
        self.headshot_kills = data.get("headshotKills")
        self.heals = data.get("heals")
        self.kills = data.get("kills")
        self.longest_kill = data.get("longestKill")
        self.longest_time_survived = data.get("longestTimeSurvived")
        self.losses = data.get("losses")
        self.max_kill_streaks = data.get("maxKillStreaks")
        self.most_survival_time = data.get("mostSurvivalTime")
        self.revives = data.get("revives")
        self.ride_distance = data.get("rideDistance")
        self.road_kills = data.get("roadKills")
        self.round_most_kills = data.get("roundMostKills")
        self.rounds_played = data.get("roundsPlayed")
        self.suicides = data.get("suicides")
        self.swim_distance = data.get("swimDistance")
        self.team_kills = data.get("teamKills")
        self.time_survived = data.get("timeSurvived")
        self.top10s = data.get("top10s")
        self.vehicle_destroys = data.get("vehicleDestroys")
        self.walk_distance = data.get("walkDistance")
        self.weapons_acquired = data.get("weaponsAcquired")
        self.weekly_kills = data.get("weeklyKills")
        self.weekly_wins = data.get("weeklyWins")
        self.wins = data.get("wins")

    def __repr__(self):
        return "SeasonStats(assists='{}', boosts='{}', dBNOs='{}' daily_kills='{}' daily_wins='{}' damage_dealt='{}' " \
               "days='{}' headshot_kills='{}' heals='{}' kills='{}' longest_kill='{}' longest_time_survived='{}' " \
               "losses='{}' max_kill_streaks='{}' revives='{}' ride_distance='{}' road_kills='{}'" \
               "round_most_kills='{}' rounds_played='{}' suicides='{}' swim_distance='{}' team_kills='{}' " \
               "time_survived='{}' top10s='{}' vehicle_destroys='{}' walk_distance='{}' weapons_acquired='{}' " \
               "weekly_wins='{} wins='{}')".format(
                self.assists, self.boosts, self.dbnos, self.daily_kills, self.daily_wins, self.damage_dealt, self.days,
                self.headshot_kills, self.heals, self.kills, self.longest_kill, self.longest_time_survived, self.losses,
                self.max_kill_streaks, self.revives, self.ride_distance, self.road_kills, self.round_most_kills,
                self.rounds_played, self.suicides, self.swim_distance, self.team_kills, self.time_survived, self.top10s,
                self.vehicle_destroys, self.walk_distance, self.weapons_acquired,
                self.weekly_wins, self.wins)

    def __str__(self):
        return self.__repr__()


class RankedStats(BaseModel):
    def __init__(self, data: dict):
        super().__init__(data)
        self.data = data

        self.current = Rank(tier=data.get("currentTier"), point=data.get("currentRankPoint"))
        self.best = Rank(tier=data.get("bestTier"), point=data.get("bestRankPoint"))

        self.assists = data.get("assists")
        self.avg_rank = data.get("avgRank")
        self.dbnos = data.get("dBNOs")
        self.deaths = data.get("deaths")
        self.damage_dealt = data.get("damageDealt")
        self.kda = data.get("kda")
        self.kills = data.get("kills")
        self.rounds_played = data.get("roundsPlayed")
        self.top10_ratio = data.get("top10Ratio")
        self.top10s = data.get("top10Ratio")
        self.win_ratio = data.get("winRatio")
        self.wins = data.get("wins")

    def __repr__(self):
        return "RankedStats(assists='{}' avg_rank='{}' dbnos='{}' deaths='{}' damage_dealt='{}' kda='{}' kills='{}' " \
               "rounds_played='{}' top10_ratio='{}' top10s='{}' win_ratio='{}' wins='{}')".format(
                self.assists, self.avg_rank, self.dbnos, self.deaths, self.damage_dealt, self.kda, self.kills,
                self.rounds_played, self.top10_ratio, self.top10s, self.win_ratio, self.wins)

    def __str__(self):
        return self.__repr__()


class Rank:
    def __init__(self, tier: dict, point: int):
        self.tier = tier.get("tier")
        self.subtier = tier.get("subTier")
        self.point = point

    def __eq__(self, other):
        return self.point == other.point

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.point < other.point

    def __gt__(self, other):
        return self.point > other.point

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __repr__(self):
        return "Rank(tier='{}' subtier='{}' point={})".format(self.tier, self.subtier, self.point)

    def __str__(self):
        if self.tier == "Unranked" or self.tier == "Master":
            return self.tier
        return "{} {}".format(self.tier, self.subtier)


class GameMode(BaseModel):
    def __init__(self, data, type_class: (RankedStats, SeasonStats)):
        super().__init__(data)
        self.type_class = type_class

        self.solo = self.type_class(data=data.get('solo', {}))
        self.solo_fpp = self.type_class(data=data.get('solo-fpp', {}))
        self.squad = self.type_class(data=data.get('squad', {}))
        self.squad = self.type_class(data=data.get('squad-fpp', {}))
        if self.type_class == SeasonStats:
            self.duo = SeasonStats(data=data.get('duo', {}))
            self.duo_fpp = SeasonStats(data=data.get('duo-fpp', {}))
        else:
            self.duo = None
            self.duo_fpp = None

    def __repr__(self):
        return "GameMode(type='{}')".format(self.type_class.__name__)

    def __str__(self):
        return self.__repr__()
