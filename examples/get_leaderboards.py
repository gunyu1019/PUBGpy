import pubgpy
import asyncio

token = "token"


async def main():
    client = pubgpy.Client(token=token, platform=pubgpy.Platforms.STEAM)

    current_season = await client.current_season()
    rank = await client.leaderboards(region=pubgpy.Region.AS, game_mode=pubgpy.GameMode.squad, season=current_season)
    top1 = rank.players[0]

    print(top1.name)
    print("Kills: {}".format(top1.stats.kills))
    print("Tier: {}".format(top1.stats.tier.tier))
    print("Sub Tier: {}".format(top1.stats.tier.subtier))
    print("Point: {}".format(top1.stats.tier.point))

event = asyncio.get_event_loop()
event.run_until_complete(main())
