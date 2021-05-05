import pubgpy
import asyncio

token = "<PUBG TOKEN>"


async def main():
    client = pubgpy.Client(token=token, platform=pubgpy.Platforms.STEAM)

    current_season = await client.current_season()
    rank = await client.leaderboards(region=pubgpy.Region.AS, game_mode=pubgpy.GameMode.squad, season=current_season)
    top1 = rank.players[0]

    print(top1.name)
    print(top1.stats.kills)
    print(top1.stats.tier.tier)
    print(top1.stats.tier.subtier)
    print(top1.stats.tier.point)

event = asyncio.get_event_loop()
event.run_until_complete(main())
