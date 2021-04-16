from .models import BaseModel
from dateutil import parser


class MatchesBaseModel:
    def __init__(self, match_id: str, match_type: str):
        self.id = match_id
        self.type = match_type

    def __eq__(self, other):
        if isinstance(other, str):
            return self.id == other
        return self.id == other.id and self.type == other.type

    def __ne__(self, other):
        return not self.__eq__(other)


class Roster(BaseModel, MatchesBaseModel):
    def __init__(self, data):
        super().__init__(data)
        self.data = data

        self.type = data.get("type", "roster")
        self.id = data.get("id")

#       attributes
        attributes = data.get("attributes", {})
        self.shard = attributes.get("shardId")
        self.rank = attributes.get("stats", {}).get("rank")
        self.team_id = attributes.get("stats", {}).get("teamId")
        self.won = attributes.get("won")

#       relationships
        relationships = data.get("relationships", {})
        self.teams = [x.get("id") for x in relationships.get("participant", {}).get("data", {})]

    def __repr__(self):
        return "Roster(id='{}' type='{}' shard='{}' rank='{}' team_id='{}' won='{}' teams='{}') ".format(
                self.id, self.type, self.shard, self.rank, self.team_id, self.won, self.teams)

    def __str__(self):
        return self.__repr__()


class Participant(BaseModel, MatchesBaseModel):
    def __init__(self, data):
        super().__init__(data)
        self.data = data

        self.type = data.get("type", "participant")
        self.id = data.get("id")

#       attributes
        attributes = data.get("attributes", {})
        self.shard = attributes.get("shardId")

#       attributes(stats)
        stats = attributes.get("stats", {})
        self.dbnos = stats.get("DBNOs")
        self.assists = stats.get("assists")
        self.boosts = stats.get("boosts")
        self.damage_dealt = stats.get("damageDealt")
        self.death_type = stats.get("deathType")
        self.headshot_kills = stats.get("headshotKills")
        self.heals = stats.get("heals")
        self.kill_place = stats.get("killPlace")
        self.kill_streaks = stats.get("killStreaks")
        self.kills = stats.get("kills")
        self.longest_kill = stats.get("longestKill")
        self.name = stats.get("name")
        self.player_id = stats.get("playerId")
        self.revives = stats.get("revives")
        self.ride_distance = stats.get("rideDistance")
        self.road_kills = stats.get("roadKills")
        self.swim_distance = stats.get("swimDistance")
        self.team_kills = stats.get("teamKills")
        self.time_survived = stats.get("timeSurvived")
        self.vehicle_destroys = stats.get("vehicleDestroys")
        self.walk_distance = stats.get("walkDistance")
        self.weapons_acquired = stats.get("weaponsAcquired")
        self.win_place = stats.get("winPlace")

    def __repr__(self):
        return "Participant(id='{}' type='{}' shard='{}' dbnos='{}' assists='{}' boosts='{}' damage_dealt='{}' " \
               "death_type='{}' headshot_kills='{}' heals='{}' kill_place='{}' kill_streaks='{}' kills='{}' " \
               "longest_kill='{}' name='{]' player_id='{}' revives='{}' ride_distance='{}' road_kills='{}' " \
               "swim_distance='{}' team_kills='{}' time_survived='{}' vehicle_destroys='{}' walk_distance='{}' " \
               "weapons_acquired='{}' win_place='{}')".format(
                self.id, self.type, self.shard, self.dbnos, self.assists, self.damage_dealt, self.death_type,
                self.headshot_kills, self.heals, self.kill_place, self.kill_streaks, self.kills, self.longest_kill,
                self.name, self.player_id, self.revives, self.ride_distance, self.road_kills, self.swim_distance,
                self.team_kills, self.time_survived, self.vehicle_destroys, self.walk_distance, self.weapons_acquired,
                self.win_place)

    def __str__(self):
        return self.name


class Assets(BaseModel, MatchesBaseModel):
    def __init__(self, data):
        super().__init__(data)
        self.data = data

        self.type = data.get("type", "participant")
        self.id = data.get("id")

#       attributes
        attributes = data.get("attributes", {})
        self.shard = attributes.get("shardId")
        self.url = attributes.get("url")
        create_at = attributes.get("createdAt")
        self.created_at = parser.isoparse(create_at).replace(tzinfo=None)
        self.name = attributes.get("name", "Telemetry")

    def __repr__(self):
        return "Assets(id='{}' type='{}' shard='{}' url='{}' created_at='{}' name='{}') ".format(
                self.id, self.type, self.shard, self.url, self.created_at, self.name)

    def __str__(self):
        return self.__repr__()


class Matches(BaseModel, MatchesBaseModel):
    def __init__(self, data, included):
        super().__init__(data)
        self.data = data
        self.included = included

#       data Information (general)
        self.id = data.get("id")
        self.type = data.get("type", "matches")

#       data Information (attributes)
        attributes = data.get("attributes", {})
        self.game_mode = attributes.get("gameMode")
        self.title = attributes.get("titleId")
        self.shard = attributes.get("shardId")
        self.tags = attributes.get("tags")
        self.map_name = attributes.get("mapName")
        self.match_type = attributes.get("matchType")
        self.duration = attributes.get("duration")
        self.stats = attributes.get("stats")
        self.season_state = attributes.get("seasonState")

        create_at = attributes.get("createdAt")
        self.created_at = parser.isoparse(create_at).replace(tzinfo=None)
        self.custom = attributes.get("isCustomMatch")

#       data Information (relationships)
        relationships = data.get("relationships", {})
        self.rosters = [x.get("id") for x in relationships.get("rosters", {}).get("data", [])]
        self.assets = [x.get("id") for x in relationships.get("assets", {}).get("data", [])]
#       self.rounds = [x.get("id") for x in relationships.get("rounds", {}).get("data", [])]
#       self.spectators = [x.get("id") for x in relationships.get("spectators", {}).get("data", [])]

#       include Information
        self.participant = list()
        self.roster = list()
        self.asset = list()
        for i in self.included:
            if i.get("type") == "participant":
                self.participant.append(Participant(i))
            elif i.get("type") == "roster":
                self.roster.append(Roster(i))
            elif i.get("type") == "asset":
                self.asset.append(Assets(i))

    def __repr__(self):
        return "Matches(id='{}' type='{}' game_mode='{}' title='{}' shard='{}' tags='{}' map_name='{}' " \
               "match_type='{}' duration='{}' stats'{}' season_state='{}' created_at='{}' custom='{}') ".format(
                self.id, self.type, self.game_mode, self.title, self.shard, self.tags, self.map_name, self.match_type,
                self.duration, self.stats, self.season_state, self.created_at, self.custom)

    def __str__(self):
        return self.__repr__()

    def filter(self, filter_id, base_model: (Roster, Participant, Assets) = None):
        list_search = list()
        if base_model is not None:
            if base_model == Roster:
                list_search = self.roster
            elif base_model == Participant:
                list_search = self.participant
            elif base_model == Assets:
                list_search = self.asset
        else:
            list_search.extend(self.roster)
            list_search.extend(self.participant)
            list_search.extend(self.asset)

        if filter_id in list_search or len(list_search) == 0:
            raise ValueError("No results for the item in searching data")

        result = None
        for x in list_search:
            if x.id == filter_id:
                result = x
        return result

    def get_team(self, team_id: str):
        if team_id not in self.rosters:
            raise ValueError("Non-existent Team ID")

        member = list()
        team = self.filter(team_id, Roster)
        for i in team.teams:
            x = self.filter(i.id, Participant)
            member.append(x)
        return member

    def get_player(self, nickname: str):
        players = self.participant
        for i in players:
            if i.name == nickname:
                return i

    def get_player_id(self, player_id: str):
        players = self.participant
        for i in players:
            if i.player_id == player_id:
                return i
