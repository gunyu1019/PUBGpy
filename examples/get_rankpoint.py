import pubgpy
import asyncio

token = "<PUBG TOKEN>"


async def main():
    client = pubgpy.Client(token=token, platform=pubgpy.Platforms.STEAM)

    player = await client.player("gunyu1128")
    resp = await player.ranked_stats(season=pubgpy.get_season(d_season=10, platform=pubgpy.Platforms.STEAM))

    print(str(resp.squad.best))
    print("Best Rank Point: {}".format(resp.squad.best.point))
    print(str(resp.squad.current))
    print("Current Rank Point: {}".format(resp.squad.current.point))
    print("Kills: {}".format(resp.squad.kills))

event = asyncio.get_event_loop()
event.run_until_complete(main())
