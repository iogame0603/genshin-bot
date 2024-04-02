import aiohttp
import aiofiles
from typing import Any
import json
from .config import Config
from .exception import *

class Route:
    def __init__(self, method: str, path: str, endpoint: str = "enka"):
        self.method = method
        self.url = ""
        
        if endpoint == "enka":
            self.url = f"{Config.ENKA_PROTOCOL}://{Config.ENKA_API_URL}{path}"
        elif endpoint == "asset":
            self.url = f"{Config.ASSET_PROTOCOL}://{path}"

class HttpClient:
    async def request(self, r: Route):
        async with aiohttp.ClientSession() as s:
            async with await s.request(method=r.method, url=r.url) as res:
                if 300 > res.status >= 200:
                    return await res.json(content_type=None)
                else:
                    raise HttpException(f"{r.url}  status code: {res.status}")
                
    async def save_asset(self, path: str, data: Any):
        async with aiofiles.open(path, "w", encoding="UTF-8") as file:
            await file.write(json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False))

    async def fetch_user(self, uid: int, info: bool = False):
            r = Route(method="GET", path=f"/api/uid/{uid}{'?info' if info else ''}")
            return await self.request(r=r)

    async def update_assets(self):
        # update character (github)
        r = Route(method="GET", path=Config.PATH.ASSET_GITHUB_PATH + Config.GITHUB_ASSET.CHARACTER, endpoint="asset")
        character = await self.request(r=r)
        await self.save_asset(path=Config.PATH.ASSET_FILE_PATH + Config.GITHUB_ASSET.CHARACTER, data=character)

        # update namecards (github)
        r = Route(method="GET", path=Config.PATH.ASSET_GITHUB_PATH + Config.GITHUB_ASSET.NAME_CARDS, endpoint="asset")
        namecard = await self.request(r=r)
        await self.save_asset(path=Config.PATH.ASSET_FILE_PATH + Config.GITHUB_ASSET.NAME_CARDS, data=namecard)

        # update pfps (github)
        r = Route(method="GET", path=Config.PATH.ASSET_GITHUB_PATH + Config.GITHUB_ASSET.PFPS, endpoint="asset")
        pfps_data = await self.request(r=r)
        await self.save_asset(path=Config.PATH.ASSET_FILE_PATH + Config.GITHUB_ASSET.PFPS, data=pfps_data)

        # update loc (github)
        r = Route(method="GET", path=Config.PATH.ASSET_GITHUB_PATH + Config.GITHUB_ASSET.LOC, endpoint="asset")
        loc_data = await self.request(r=r)
        await self.save_asset(path=Config.PATH.ASSET_FILE_PATH + Config.GITHUB_ASSET.LOC, data=loc_data)

        r = Route(method="GET", path=Config.PATH.ASSET_GITLAB_TEXTMAP_PATH + Config.GITLAB_ASSET.TEXTMAP_KR, endpoint="asset")
        textMapKr = await self.request(r=r)
        await self.save_asset(path=Config.PATH.ASSET_FILE_PATH + Config.GITLAB_ASSET.TEXTMAP_KR, data=textMapKr)