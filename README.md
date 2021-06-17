<p align="center">
    <img src="https://user-images.githubusercontent.com/16767890/121933538-2e86e600-cd81-11eb-8ed6-0f85540be74c.png" width="50%" style=""/>
</p>
<h1 align="center">PUBGpy</h1>
<p align="center">
    <a href="https://www.codefactor.io/repository/github/gunyu1019/pubgpy"><img src="https://www.codefactor.io/repository/github/gunyu1019/pubgpy/badge" alt="CodeFactor" /></a>
    <a href="https://www.codacy.com/gh/gunyu1019/PUBGpy/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=gunyu1019/PUBGpy&amp;utm_campaign=Badge_Grade">     <img src="https://app.codacy.com/project/badge/Grade/9ec565ce3eb74786b1fe8d02d281bb1d"/></a>
    <a href="https://pypistats.org/packages/pubgpy"><img src="https://img.shields.io/pypi/dm/pubgpy" alt="PyPi Downloading" /></a>
    <a href="https://pypi.org/project/PUBGpy"><img src="https://img.shields.io/pypi/v/pubgpy" alt="PyPi Version" /></a>
    <a href="https://pypi.org/project/PUBGpy"><img src="https://img.shields.io/pypi/pyversions/pubgpy" alt="PyPi Version" /></a>
</p>

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
