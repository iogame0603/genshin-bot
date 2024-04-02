from pydantic import BaseModel, PrivateAttr
from typing import Union, List

from ..util import Util

class StatVal(BaseModel):
    type: str
    value: int = 0

class StatValPer(BaseModel):
    type: str
    value: float = 0

    def value2percent(self):
        return f"{self.value}%"
    
class BaseEquip(BaseModel):
    name: str = ""
    level: int = 1
    rankLevel: int = 1

    icon: str = ""

    def __init__(self, **data):
        _flat = data["flat"]
        data["rankLevel"] = _flat["rankLevel"]
        data["icon"] = Util.get_img_url(iconName=_flat["icon"])
        super().__init__(**data)

class Reliquary(BaseEquip):
    setName: str
    type: str
    mainStat: Union[StatVal, StatValPer]
    subStatList: List[Union[StatVal, StatValPer]]

    _nameTextHashId: Union[int, str] = PrivateAttr()

    @classmethod
    async def set_reliquary_name(cls):
        cls.name = await Util.get_reliquary_name(cls.nameTextHashId)

    @property
    def nameTextHashId(self):
        return self._nameTextHashId

    def __init__(self, **data):
        _flat = data["flat"]

        data["_nameTextHashId"] = _flat["nameTextMapHash"]
        data["setName"] = Util.get_localizations(id=_flat["setNameTextMapHash"])
        data["level"] = data["reliquary"]["level"] - 1
        data["type"] = _flat["equipType"]

        mainStat = _flat["reliquaryMainstat"]
        if type(mainStat["statValue"]) == int:
            data["mainStat"] = StatVal(type=Util.get_localizations(mainStat["mainPropId"]), value=mainStat["statValue"])
        elif type(mainStat["statValue"]) == float:
            data["mainStat"] = StatValPer(type=Util.get_localizations(mainStat["mainPropId"]), value=mainStat["statValue"])

        subStatList: List[Union[StatVal, StatValPer]] = []
        for subStat in _flat["reliquarySubstats"]:
            if type(subStat["statValue"]) == int:
                subStatList.append(StatVal(type=Util.get_localizations(subStat["appendPropId"]), value=subStat["statValue"]))
            elif type(subStat["statValue"]) == float:
                subStatList.append(StatValPer(type=Util.get_localizations(subStat["appendPropId"]), value=subStat["statValue"]))
            data["subStatList"] = subStatList
        super().__init__(**data)

class Weapon(BaseEquip):
    stats: List[Union[StatVal, StatValPer]]

    def __init__(self, **data):
        _flat = data["flat"]
        weaponStatList: List[Weapon] = []
        for weaponStat in _flat["weaponStats"]:
            if type(weaponStat["statValue"]) == int:
                weaponStatList.append(StatVal(type=Util.get_localizations(weaponStat["appendPropId"]), value=weaponStat["statValue"]))
            elif type(weaponStat["statValue"]) == float:
                weaponStatList.append(StatValPer(type=Util.get_localizations(weaponStat["appendPropId"]), value=weaponStat["statValue"]))
        data["stats"] = weaponStatList

        data["level"] = data["weapon"]["level"]
        data["name"] = Util.get_localizations(id=_flat["nameTextMapHash"])
        super().__init__(**data)