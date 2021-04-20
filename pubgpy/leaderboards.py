from .models import BaseModel
from .player import Player


class Leaderboards(BaseModel):
    def __init__(self, client, data, included):
        super().__init__(data)
        self.data = data
        self.client = client

        self.id = self.data.get("id")
        self.type = self.data.get("type", "leaderboard")

        # attributes
        attributes = self.data.get("attributes")
        self.shard_id = attributes.get("shardId")
        self.game_mode = attributes.get("gameMode")
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
