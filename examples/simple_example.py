import pubgpy
import asyncio

token = "token"


async def main():
    client = pubgpy.Client(token=token, platform=pubgpy.Platforms.STEAM)

    player = await client.player("gunyu1128")
    resp = await player.season_stats(season=pubgpy.get_season(d_season=10, platform=pubgpy.Platforms.STEAM))

    print("Nickname: {}".format(player.name))
    print("Assets: {}".format(resp.squad.kills))
    print("Kills: {}".format(resp.squad.kills))

event = asyncio.get_event_loop()
event.run_until_complete(main())
