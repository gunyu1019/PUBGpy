import pubgpy
import asyncio

token = "<PUBG TOKEN>"


async def main():
    client = pubgpy.Client(token=token, platform=pubgpy.Platforms.STEAM)

    player = await client.player("gunyu1128")
    resp = await player.match(position=0)

    player_stats = resp.get_player(player.name)
    team = resp.roster[0]
    member_id = team.teams[0]
    member = resp.filter(pubgpy.Participant, member_id)

    print(player_stats.kills)
    print(member.kills)

event = asyncio.get_event_loop()
event.run_until_complete(main())
