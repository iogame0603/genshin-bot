from .httpClient import HttpClient
from .model.enkaNetworkAPI import EnkaNetworkAPI
from .config import Config

class EnkaNetworkClient:
    def __init__(self, lang="ko"):
        if not lang in Config.LANG_LIST:
            raise ValueError(f"Unknown language: {lang}")
        Config.LANG = lang
        self.__http = HttpClient()

    async def fetch_user(self, uid: int, info: bool = False) -> EnkaNetworkAPI:
        data = await self.__http.fetch_user(uid=uid, info=info)
        enka_data = EnkaNetworkAPI(**data)
        return enka_data
    
    async def update_assets(self):
        await self.__http.update_assets()