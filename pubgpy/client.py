from .api import Api
from .player import Player
from .season import Season
from .matches import Matches
from .leaderboards import Leaderboards


class Client:
    def __init__(self, token: str, platform: str = None):
        self.token = token
        self.Platform = platform
        self.requests = Api(token=token, platform=platform)

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
        self.requests.platform = shard
        path = "/leaderboards/{}/{}".format(season, game_mode)
        resp = await self.requests.get(path=path)
        self.requests.platform = platform

        data = resp.get('data')
        included = resp.get('included')
        return Leaderboards(self, data, included)
