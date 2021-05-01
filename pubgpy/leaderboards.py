"""
MIT License

Copyright (c) 2021 gunyu1019

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from .models import PUBGModel
from .player import Player


class Leaderboards(PUBGModel):
    """Leaderboard objects show the current rank of the top 500 players for a game mode."""
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
