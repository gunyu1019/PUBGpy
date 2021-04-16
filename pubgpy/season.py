from .platforms import Platforms
from .models import BaseModel


def get_season(d_season: int, platform: str):
    if platform == Platforms.STEAM or platform == Platforms.KAKAO:
        f_season = "pc"
    elif platform == Platforms.XBOX or platform == Platforms.PLAYSTATION or platform == Platforms.STADIA:
        f_season = "console"
    else:
        raise TypeError(
            "Platform information not found. PUBGpy only supports Steam, Kakao, XBOX, PlayStation, and Stadia.")

    if isinstance(d_season, int):
        d_season = str(d_season)
    d_season = d_season.zfill(2)

    return Season({
        "id": "division.bro.official.{}-2018-{}".format(f_season, d_season),
        "type": "season"
    })


class Season(BaseModel):
    def __init__(self, data: dict):
        super().__init__(data)
        self.data = data
        self.type = self.data.get("type")
        self.id = self.data.get("id", "season")

        self.current = self.data.get("attributes", {}).get("isCurrentSeason")
        self.off_season = self.data.get("attributes", {}).get("isOffseason")

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "Season(id='{}', current='{}', type='{}')".format(self.id, self.current, self.type)

    def __str__(self):
        return self.id
