from pydantic import Field, BaseModel
from .player import PlayerInfo
from .avatar import AvatarInfoDetail
from typing import List

class EnkaNetworkAPI(BaseModel):
    player: PlayerInfo = Field(None, alias="playerInfo")
    avatarInfoList: List[AvatarInfoDetail] = Field([], alias="avatarInfoList")
    ttl: int = Field(0, alias="ttl")
    uid: str = Field("", alias="uid")