# PUBGpy
A python wrapper for Battleground API.<br/>
It is composed of asynchronous devices, enabling more efficient use of modules.

It is not difficult to use, but there are some differences from official documents.
* [Offical Documentation](https://documentation.pubg.com/en/introduction.html)

If you have any questions, 건유1019#0001 on discord or e-mail (gunyu1019@yhs.kr), you may ask.

### Installation
```commandline
// Windows
py -3 -m pip install pubgpy

// Linux / MacOS
python3 -m pip install pubgpy
```

### Quick Example
```python
import pubgpy
import asyncio

token = "<PUBG TOKEN>"


async def main():
    client = pubgpy.Client(token=token, platform=pubgpy.Platforms.STEAM)

    player = await client.player("gunyu1128")
    resp = await player.season_stats(season=pubgpy.get_season(d_season=10, platform=pubgpy.Platforms.STEAM))

    print("Nickname: {}".format(player.name))
    print("Assets: {}".format(resp.squad.kills))
    print("Kills: {}".format(resp.squad.kills))

event = asyncio.get_event_loop()
event.run_until_complete(main())
```

### License
**MIT License**<br/>
Copyright (c) 2021 gunyu1019