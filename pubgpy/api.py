import aiohttp
import json


class Api:
    def __init__(self, token: str, platform: str):
        self.token = token

        self.BASE_URL = "https://api.pubg.com"
        self.platform = platform

    async def requests(self, method, path, ni_shards: bool = True, **kwargs):
        header = {
            "accept": "application/vnd.api+json",
            "Authorization": "Bearer {}".format(self.token)
        }
        header.update(**kwargs)

        if ni_shards:
            url = "{}/shards/{}{}" .format(self.BASE_URL, self.platform, path)
        else:
            url = "{}{}" .format(self.BASE_URL, path)
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=header) as resp:
                if resp.status == 200:
                    if resp.content_type == "application/json":
                        data = await resp.json()
                    else:
                        fp_data = await resp.text()
                        data = json.loads(fp_data)
                    return data

    async def get(self, path, platform: bool = True, **kwargs):
        return await self.requests(method="GET", path=path, ni_shards=platform, **kwargs)
