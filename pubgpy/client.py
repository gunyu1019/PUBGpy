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

import datetime

from .api import Api
from .player import Player
from .enums import Platforms
from .errors import APIException
from .season import Season
from .matches import Matches
from .leaderboards import Leaderboards
from .tournaments import Tournaments
from .sample import Sample


class Client:
    def __init__(self, token: str, platform: (str, Platforms) = None):
        self.token = token
        if isinstance(platform, Platforms):
            self.Platform = platform.value
        else:
            self.Platform = platform
        self.requests = Api(token=token, platform=self.Platform)

    def platform(self, platform: str):
        self.Platform = platform
        return self.Platform

    def player_id(self, player_id: str):
        _data = {
            "id": player_id
        }
        return Player(client=self, data=_data)

    async def player(self, nickname: str):
        data = await self.players(players=[nickname])
        return data[0]

    async def players(self, players: list = None, ids: list = None):
        path = "/players"
        if players is not None:
            join_data = "%2c".join(players)
            path += "?filter[playerNames]={}".format(join_data)
        if ids is not None:
            if players is not None:
                path += "&"
            else:
                path += "?"
            join_data = "%2c".join(ids)
            path += "filter[playerIds]={}".format(join_data)

        resp = await self.requests.get(path=path)
        data = resp.get('data')
        return [Player(client=self, data=_) for _ in data]

    async def current_season(self):
        seasons = await self.seasons()
        for i in seasons:
            if i.current:
                return i
        raise ValueError("Can not find current season.")

    async def seasons(self):
        path = "/seasons"
        resp = await self.requests.get(path=path)
        data = resp.get('data')
        return [Season(_) for _ in data]

    async def season_stats(self, player_id: str, season: str = None):
        player = self.player_id(player_id=player_id)
        data = await player.season_stats(season)
        return data

    async def ranked_stats(self, player_id: str, season: str = None):
        player = self.player_id(player_id=player_id)
        data = await player.ranked_stats(season)
        return data

    async def lifetime_stats(self, player_id: str):
        player = self.player_id(player_id=player_id)
        data = await player.lifetime_stats()
        return data

    async def weapon_mastery(self, player_id: str):
        player = self.player_id(player_id=player_id)
        data = await player.weapon()
        return data

    async def survival_mastery(self, player_id: str):
        player = self.player_id(player_id=player_id)
        data = await player.survival()
        return data

    async def matches(self, match_id: str):
        path = "/matches/{}".format(match_id)
        resp = await self.requests.get(path=path)
        data = resp.get('data')
        included = resp.get('included')
        return Matches(data=data, included=included)

    async def tournaments(self):
        path = "/tournaments"
        resp = await self.requests.get(path=path, ni_shards=False)
        data = resp.get('data')
        return [Tournaments(self, x) for x in data]

    async def tournament_id(self, tournament_id: str):
        path = "/tournaments/{}".format(tournament_id)
        resp = await self.requests.get(path=path, ni_shards=False)
        data = resp.get('data')
        return Tournaments(self, data)

    async def samples(self, create_at: (datetime.datetime, str) = None):
        path = "/samples"
        if create_at is not None:
            if isinstance(create_at, datetime.datetime):
                create_at = create_at.strftime("%Y-%m-%dT%H:%M:%SZ")
            path += "?filter[createdAt-start]={}".format(create_at)
        resp = await self.requests.get(path=path)
        data = resp.get('data')
        return Sample(self, data)

    async def status(self):
        path = "/status"
        try:
            await self.requests.get(path=path, ni_shards=False)
        except APIException:
            return False
        return True

    async def leaderboards(self, region: str, game_mode: str, season: str = None):
        if season is None:
            season = await self.current_season()
        platform = self.requests.platform

        if platform == "steam" or "kakao":
            type_platform = "pc"
        elif platform == "xbox":
            type_platform = "xbox"
        elif platform == "psn":
            type_platform = "psn"
        else:
            raise TypeError("Unsupported platform (stadia not supported)")

        shard = '{}-{}'.format(type_platform, region)
        path = "/shards/{}/leaderboards/{}/{}".format(shard, season, game_mode)
        resp = await self.requests.get(path=path, ni_shards=False)

        data = resp.get('data')
        included = resp.get('included')
        return Leaderboards(self, data, included)
