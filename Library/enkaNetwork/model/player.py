from typing import List
from pydantic import Field, BaseModel, AliasChoices

from .avatar import AvatarInfo
from ..util import Util

class ProfilePicture(BaseModel):
    id: int = Field(None, validation_alias=AliasChoices("avatarId", "id"))
    icon: str = ""

    def __init__(self, **data):
        if "avatarId" in data:
            data["icon"] = Util.get_profile_img_by_avatarId(data["avatarId"])
        if "id" in data:
            data["icon"] = Util.get_profile_img_by_id(data["id"])
        super().__init__(**data)

class NameCard(BaseModel):
    id: int
    icon: str = ""

    def __init__(self, **data):
        data["icon"] = Util.get_namecard_img(data["id"])
        super().__init__(**data)

class PlayerInfo(BaseModel):
    nickname: str = Field("", alias="nickname")
    level: int = Field(0, alias="level")
    signature: str = Field("", alias="signature")
    worldLevel: int = Field(0, alias="worldLevel")
    nameCard: NameCard = None

    towerFloorIndex: int = Field(0, alias="towerFloorIndex")
    towerLevelIndex: int = Field(0, alias="towerLevelIndex")

    showAvatarInfoList: List[AvatarInfo] = Field([], alias="showAvatarInfoList")
    showNameCardList: List[NameCard] = []

    profilePicture: ProfilePicture = Field(None, alias="profilePicture")

    def __init__(self, **data):
        data["profilePicture"] = ProfilePicture(**data["profilePicture"])
        data["nameCard"] = NameCard(id=data["nameCardId"])
        data["showNameCardList"] = [NameCard(id=id) for id in data["showNameCardIdList"]]
        super().__init__(**data)