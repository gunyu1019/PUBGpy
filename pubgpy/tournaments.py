"""
MIT License

Copyright (c) 2021 gunyu1019

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from .models import PUBGModel
from .matches import Matches
from datetime import datetime


class Tournaments(PUBGModel):
    def __init__(self, client, data):
        super().__init__(data)
        self.client = client
        self.id = data.get("id")
        self.type = data.get("type", "tournament")

        created_at = data.get("attributes", {}).get("createdAt")
        if created_at is not None:
            self.created_at = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=None)

        relationships = data.get("relationships")
        self.matches = list()
        if relationships is not None:
            matches = relationships.get("matches", {}).get("data")
            for i in matches:
                self.matches.append(i.get("id"))

    def __str__(self):
        return self.id

    async def match(self, position: int = 0):
        if position > len(self.matches):
            raise IndexError("list index out of Match List ()")
        match_id = self.matches[position]
        path = "/shards/{}/matches/{}".format("tournament", match_id)
        resp = await self.client.requests.get(path=path, ni_shards=False)
        data = resp.get('data')
        included = resp.get('included')
        return Matches(data=data, included=included)

    async def load(self):
        return self.client.tournament_id(self.id)
