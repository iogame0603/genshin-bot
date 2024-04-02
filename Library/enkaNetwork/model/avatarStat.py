from pydantic import BaseModel, field_validator
from typing import Union

class StatVal(BaseModel):
    id: int
    value: Union[int, float] = 0

    @field_validator("value")
    def round_val(cls, v: Union[int, float]):
        return round(v)
    
    class Config:
        validate_assignment = True

class StatValPer(BaseModel):
    id: int
    value: Union[int, float] = 0

    @field_validator("value")
    def round_val(cls, v: Union[int, float]):
        return round(v * 100, 1)

    def value2percent(self):
        return f"{self.value}%"
    
    class Config:
        validate_assignment = True
    
class AvatarStat(BaseModel):
    BASE_HP: StatVal = StatVal(id=1)
    HP: StatVal = StatVal(id=2)
    HP_PER: StatValPer = StatValPer(id=3)

    BASE_ATK: StatVal = StatVal(id=4)
    ATK: StatVal = StatVal(id=5)
    ATK_PER: StatValPer = StatValPer(id=6)

    BASE_DEF: StatVal = StatVal(id=7)
    DEF: StatVal = StatVal(id=8)
    DEF_PER: StatValPer = StatValPer(id=9)

    BASE_SPD: StatVal = StatVal(id=10)
    SPD_PER: StatValPer = StatValPer(id=11)

    CRIT_RATE: StatValPer = StatValPer(id=20)
    CRIT_DMG: StatValPer = StatValPer(id=22)

    ENERGY_RECHANGE: StatValPer = StatValPer(id=23)

    HEALING_BONUS: StatValPer = StatValPer(id=26)
    INCOMING_HEALING_BONUS: StatValPer = StatValPer(id=27)

    ELEMENTAL_MASTERY: StatVal = StatVal(id=28)

    PHYSICAL_RES: StatValPer = StatValPer(id=29)
    PHYSICAL_DMG_BONUS: StatValPer = StatValPer(id=30)
    PYRO_DMG_BONUS: StatValPer = StatValPer(id=40)
    ELECTRO_DMG_BONUS: StatValPer = StatValPer(id=41)
    HYDRO_DMG_BONUS: StatValPer = StatValPer(id=42)
    DENDRO_DMG_BONUS: StatValPer = StatValPer(id=43)
    ANEMO_DMG_BONUS: StatValPer = StatValPer(id=44)
    GEO_DMG_BONUS: StatValPer = StatValPer(id=45)
    CYRO_DMG_BONUS: StatValPer = StatValPer(id=46)
    
    PYRO_RES: StatValPer = StatValPer(id=50)
    ELECTRO_RES: StatValPer = StatValPer(id=51)
    HYDRO_RES: StatValPer = StatValPer(id=52)
    DENDRO_RES: StatValPer = StatValPer(id=53)
    ANEMO_RES: StatValPer = StatValPer(id=54)
    GEO_RES: StatValPer = StatValPer(id=55)
    CYRO_RES: StatValPer = StatValPer(id=56)

    PYRO_ENEGRY_COST: StatVal = StatVal(id=70)
    ELECTRO_ENEGRY_COST: StatVal = StatVal(id=71)
    HYDRO_ENEGRY_COST: StatVal = StatVal(id=72)
    DENDRO_ENEGRY_COST: StatVal = StatVal(id=73)
    ANEMO_ENEGRY_COST: StatVal = StatVal(id=74)
    CYRO_ENEGRY_COST: StatVal = StatVal(id=75)
    GEO_ENEGRY_COST: StatVal = StatVal(id=76)

    COOLDOWN_REDUCTION: StatValPer = StatValPer(id=80)
    SHIELD_STRENGTH: StatValPer = StatValPer(id=81)

    CURRENT_PYRO_ENERGY: StatVal = StatVal(id=1000)
    CURRENT_ELECTRO_ENERGY: StatVal = StatVal(id=1001)
    CURRENT_HYDRO_ENERGY: StatVal = StatVal(id=1002)
    CURRENT_DENDRO_ENERGY: StatVal = StatVal(id=1003)
    CURRENT_ANEMO_ENERGY: StatVal = StatVal(id=1004)
    CURRENT_CYRO_ENERGY: StatVal = StatVal(id=1005)
    CURRENT_GEO_ENERGY: StatVal = StatVal(id=1006)

    CURRENT_HP: StatVal = StatVal(id=1010)
    MAX_HP: StatVal = StatVal(id=2000)
    CURRENT_ATK: StatVal = StatVal(id=2001)
    CURRENT_DEF: StatVal = StatVal(id=2002)
    CURRENT_SPD: StatVal = StatVal(id=2003)

    ELEMENTAL_REACTION_CRIT_RATE: StatValPer = StatValPer(id=3025)
    ELEMENTAL_REACTION_CRIT_DMG: StatValPer = StatValPer(id=3026)
    OVERLOADED_CRIT_RATE: StatValPer = StatValPer(id=3027)
    OVERLOADED_CRIT_DMG: StatValPer = StatValPer(id=3028)
    SWIRL_CRIT_RATE:  StatValPer = StatValPer(id=3029)
    SWIRL_CRIT_DMG: StatValPer = StatValPer(id=3030)
    ELECTRO_CHARGED_CRIT_RATE: StatValPer = StatValPer(id=3031)
    ELECTRO_CHARGED_CRIT_DMG: StatValPer = StatValPer(id=3032)
    SUPERCONDUCT_CRIT_RATE: StatValPer = StatValPer(id=3033)
    SUPERCONDUCT_CRIT_DMG: StatValPer = StatValPer(id=3034)
    BURN_CRIT_RATE: StatValPer = StatValPer(id=3035)
    BURN_CRIT_DMG: StatValPer = StatValPer(id=3036)
    SHATTERED_CRIT_RATE: StatValPer = StatValPer(id=3037)
    SHATTERED_CRIT_DMG: StatValPer = StatValPer(id=3038)
    BLOOM_CRIT_RATE: StatValPer = StatValPer(id=3039)
    BLOOM_CRIT_DMG: StatValPer = StatValPer(id=3040)
    BURGEON_CRIT_RATE: StatValPer = StatValPer(id=3041)
    BURGEON_CRIT_DMG: StatValPer = StatValPer(id=3042)
    HYPERBLOOM_CRIT_RATE: StatValPer = StatValPer(id=3043)
    HYPERBLOOM_CRIT_DMG: StatValPer = StatValPer(id=3044)
    BASE_ELEMENTAL_REACTION_CRIT_RATE: StatValPer = StatValPer(id=3045)
    BASE_ELEMENTAL_REACTION_CRIT_DMG: StatValPer = StatValPer(id=3046)

    def __init__(self, **data):
        super().__init__(**data)
        _stats = self.__dict__

        for k in _stats:
            if str(_stats[k].id) in data:
                _stats[k].value = data[str(_stats[k].id)]