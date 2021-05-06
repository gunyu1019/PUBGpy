import pubgpy
import asyncio

token = "<PUBG TOKEN>"


async def main():
    client = pubgpy.Client(token=token, platform=pubgpy.Platforms.STEAM)

    player = await client.player("gunyu1128")
    resp = await player.match(position=0)

    player_stats = resp.get_player(nickname=player.name)
    team = resp.get_team(player_id=player_stats.id)
    member = team.teams

    print("Team Member: {}".format(member))
    print("Kill: {}".format(player_stats.kills))


event = asyncio.get_event_loop()
event.run_until_complete(main())
