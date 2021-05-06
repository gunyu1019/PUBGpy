import pubgpy
import asyncio

token = "<PUBG TOKEN>"


async def main():
    client = pubgpy.Client(token=token, platform=pubgpy.Platforms.STEAM)

    tournaments = await client.tournaments()
    tournament = await tournaments[0].load()
    match = await tournament.match(position=0)

    print(tournament.id)
    print(match.created_at)

event = asyncio.get_event_loop()
event.run_until_complete(main())
