from .models import BaseModel, PUBGModel
from .player import Player


class Leaderboards(PUBGModel):
    def __init__(self, client, data, included):
        self.data = data
        self.client = client

        self.id = self.data.get("id")
        self.type = self.data.get("type", "leaderboard")
        super().__init__(self)

        # attributes
        attributes = self.data.get("attributes")
        self.shard_id = attributes.get("shardId")
        self.gamemode = attributes.get("gameMode")
        self.season = attributes.get("seasonId")

        # included
        self.included = list()
        for i in included:
            self.included.append(Player(client, i))

        # relationships
        self.players = list()
        relationships = self.data.get("relationships")

        def search_people(player_id):
            next(players for players in self.included if players == player_id)

        for x in relationships.get("players"):
            self.players.append(search_people(x.get("id")))

    def __repr__(self):
        return "Leaderboards(id='{}' type='{}' shard='{}' gamemode='{}' season='{}' players='{}')".format(
            self.id, self.type, self.shard_id, self.gamemode, self.season, self.player)
        
    def __str__(self):
        return self.__repr__()
