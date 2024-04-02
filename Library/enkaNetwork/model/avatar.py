from pydantic import Field, BaseModel
from typing import Dict, Any, List, Union

from .avatarStat import AvatarStat
from ..util import Util
from .equip import Reliquary, Weapon
from .skill import Skill

class Costume(BaseModel):
    id: Union[int, str] = Field(alias="costumeId")
    icon: str = ""
    art: str = ""

class BaseAvatar(BaseModel):
    name: str = ""
    id: int = Field(0, alias="avatarId")
    icon: str = ""
    element: str = ""
    costume: Costume = None

    def __init__(self, **data):
        avatarInfo = None
        if "costumeId" in data:
            avatarInfo = Util.get_avatar_info(data["avatarId"], data["costumeId"])
            data["costume"] = Costume(**avatarInfo["costume"])
        else:
            avatarInfo = Util.get_avatar_info(data["avatarId"])

        data["name"] = avatarInfo["name"]
        data["icon"] = avatarInfo["icon"]
        data["element"] = avatarInfo["element"]

        super().__init__(**data)

class FetterInfo(BaseModel):
    expLevel: int = Field(0, alias="expLevel")

class AvatarInfo(BaseAvatar):
    level: int = Field(0, alias="level")

class AvatarInfoDetail(BaseAvatar):
    xp: int = 0
    ascension: int = 0
    level: int = 0
    stats: AvatarStat = Field({}, alias="fightPropMap")
    fetterInfo: FetterInfo = Field(None, alias="fetterInfo")

    reliquaryList: List[Reliquary] = []
    weapon: Weapon = None
    skillList: List[Skill] = []

    def __init__(self, **data):
        if "propMap" in data:
            propMap: Dict[str, Any] = data["propMap"]
            if "1001" in propMap:
                data["xp"] = int(propMap["1001"]["ival"])
            if "1002" in propMap:
                data["ascension"] = int(propMap["1002"]["ival"])
            if "4001" in propMap:
                data["level"] = int(propMap["4001"]["ival"])

        if "equipList" in data:
            reliquaryList: List[Reliquary] = []
            for d in data["equipList"]:
                if d["flat"]["itemType"] == "ITEM_RELIQUARY":
                    reliquaryList.append(Reliquary(**d))
                elif d["flat"]["itemType"] == "ITEM_WEAPON":
                    data["weapon"] = Weapon(**d)
            data["reliquaryList"] = reliquaryList

        skillList: List[Skill] = []
        avatarSkills = Util.get_avatar_skills(data["avatarId"])
        for skillId in data["skillLevelMap"]:
            if skillId in avatarSkills:
                skillList.append(Skill(id=skillId, level=data["skillLevelMap"][str(skillId)], icon=avatarSkills[str(skillId)]))
        data["skillList"] = skillList

        super().__init__(**data)