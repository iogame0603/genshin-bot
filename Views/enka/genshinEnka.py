import discord
from discord.ui import Button, View, Select, Item

from typing import Any, List, Union, Optional

from enkaNetwork.model import AvatarInfoDetail, Reliquary
from enkaNetwork.types import ReliquaryType, ElementColor, ElementType

from Utils.util import Logging

def get_avatar_data(avatarInfoList: List[AvatarInfoDetail], avatarId: Union[int, str]) -> AvatarInfoDetail:
    for avatarInfo in avatarInfoList:
        if str(avatarInfo.id) == str(avatarId):
            return avatarInfo
    Logging.LOGGER.warning(f"존재하지 않는 avatarId (id: {avatarId})")
    raise ValueError(f"avatarId: {avatarId} 정보를 찾을 수 없음")

def get_element_color(element: str):
    match element:
        case ElementType.WIND:
            return ElementColor.WIND.value
        case ElementType.ROCK:
            return ElementColor.ROCK.value
        case ElementType.ELECTRIC:
            return ElementColor.ELECTRIC.value
        case ElementType.WATER:
            return ElementColor.WATER.value
        case ElementType.ICE:
            return ElementColor.ICE.value
        case ElementType.FIRE:
            return ElementColor.FIRE.value
        case ElementType.GRASS:
            return ElementColor.GRASS.value
        case ElementType.NONE:
            return ElementColor.NONE.value
        case _:
            Logging.LOGGER.warning(f"존재하지 않는 원소 타입 (type: {element})")
            raise ValueError(f"존재하지 않는 원소타입 (type: {element})")

def character_info_embed(data: AvatarInfoDetail) -> discord.Embed:
    embed = discord.Embed(title=f"{data.name}", color=get_element_color(data.element))
    if data.costume != None:
        embed.set_thumbnail(url=data.costume.icon)
    else:
        embed.set_thumbnail(url=data.icon)

    avatarInfo: str = f"""
레벨: {data.level}
호감도: {data.fetterInfo.expLevel}"""
    embed.add_field(name="정보", value=avatarInfo, inline=False)

    avatarStats: str = f"""
체력: {data.stats.MAX_HP.value}
공격력: {data.stats.CURRENT_ATK.value}
방어력: {data.stats.CURRENT_DEF.value}
원소 마스터리: {data.stats.ELEMENTAL_MASTERY.value}
치명타 확률: {data.stats.CRIT_RATE.value2percent()}
치명타 피해: {data.stats.CRIT_DMG.value2percent()}
원소 충전 효율: {data.stats.ENERGY_RECHANGE.value2percent()}
"""
    if data.stats.PHYSICAL_DMG_BONUS.value != 0:
        avatarStats += f"물리 피해 보너스: {data.stats.PHYSICAL_DMG_BONUS.value2percent()}\n"
    if data.stats.PYRO_DMG_BONUS.value != 0:
        avatarStats += f"불 원소 피해 보너스: {data.stats.PYRO_DMG_BONUS.value2percent()}\n"
    if data.stats.ELECTRO_DMG_BONUS.value != 0:
        avatarStats += f"번개 원소 피해 보너스: {data.stats.ELECTRO_DMG_BONUS.value2percent()}\n"
    if data.stats.HYDRO_DMG_BONUS.value != 0:
        avatarStats += f"물 원소 피해 보너스: {data.stats.HYDRO_DMG_BONUS.value2percent()}\n"
    if data.stats.DENDRO_DMG_BONUS.value != 0:
        avatarStats += f"풀 원소 피해 보너스: {data.stats.DENDRO_DMG_BONUS.value2percent()}\n"
    if data.stats.ANEMO_DMG_BONUS.value != 0:
        avatarStats += f"바람 원소 피해 보너스: {data.stats.ANEMO_DMG_BONUS.value2percent()}\n"
    if data.stats.GEO_DMG_BONUS.value != 0:
        avatarStats += f"바위 원소 피해 보너스: {data.stats.GEO_DMG_BONUS.value2percent()}\n"
    if data.stats.CYRO_DMG_BONUS.value != 0:
        avatarStats += f"얼음 원소 피해 보너스: {data.stats.CYRO_DMG_BONUS.value2percent()}\n"

    embed.add_field(name="스탯", value=avatarStats, inline=True)
    return embed

class CharacterSelect(Select):
    def __init__(self, data: List[AvatarInfoDetail]):
        self.data = data

        options: List[discord.SelectOption] = []
        for avatarInfo in data:
            options.append(discord.SelectOption(label=avatarInfo.name, value=avatarInfo.id))
        super().__init__(options=options, placeholder="캐릭터를 선택해주세요.")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        avatarId = interaction.data["values"][0]
        view = CharacterInfoView.from_message(message=interaction.message, data=self.data, avatarId=avatarId)
        await interaction.followup.edit_message(interaction.message.id,
                                                embed=character_info_embed(get_avatar_data(self.data, avatarId=avatarId)),
                                                view=view)

class CharacterInfoBtn(Button):
    def __init__(self, data: AvatarInfoDetail):
        self.data = data
        self.avatarId = data.id
        super().__init__(label="캐릭터", custom_id=f"char_{data.id}")
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.followup.edit_message(interaction.message.id,
                                                embed=character_info_embed(self.data))

class CharacterWeaponBtn(Button):
    def __init__(self, data: AvatarInfoDetail):
        self.data = data
        self.avatarId = data
        super().__init__(label="무기", custom_id=f"weapon_{data.id}")
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        weapon = self.data.weapon
        weaponStats: str = ""
        for weaponStat in weapon.stats:
            if type(weaponStat.value) == int:
                weaponStats += f"{weaponStat.type}: {weaponStat.value}\n"
            elif type(weaponStat.value) == float:
                weaponStats += f"{weaponStat.type}: {weaponStat.value2percent()}\n"

        embed = discord.Embed(title=weapon.name, color=get_element_color(self.data.element))
        embed.set_thumbnail(url=weapon.icon)
        embed.add_field(name="무기 스탯", value=weaponStats)
        embed.set_footer(text=self.data.name, icon_url=self.data.icon)

        await interaction.followup.edit_message(interaction.message.id,
                                                embed=embed)

class CharacterReliquaryBtn(Button):
    def __init__(self, avatarId: Union[int, str], avatarInfoList: List[AvatarInfoDetail], disabled: bool = False):
        self.avatarId = avatarId
        self.avatarInfoList = avatarInfoList
        super().__init__(label="성유물", disabled=disabled)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        characterReliquaryView = CharacterReliquaryView(interaction.user, self.avatarId, self.avatarInfoList)
        characterReliquaryView.message = await interaction.followup.edit_message(interaction.message.id, view=characterReliquaryView)

class CharacterInfoView(View):
    def __init__(self, author: Union[discord.User, discord.Member], data: List[AvatarInfoDetail], avatarId: int = None):
        self.author = author
        self.data = data
        self.avatarId = None
        if avatarId == None:
            self.avatarId = data[0].id
        else:
            self.avatarId = avatarId
        super().__init__(timeout=None)

        avatarInfo = get_avatar_data(avatarInfoList=data, avatarId=self.avatarId)
        self.add_item(item=CharacterSelect(data=data))
        self.add_item(item=CharacterInfoBtn(data=avatarInfo))
        self.add_item(item=CharacterWeaponBtn(data=avatarInfo))
        if avatarInfo.reliquaryList == []:
            self.add_item(item=CharacterReliquaryBtn(avatarId=self.avatarId, avatarInfoList=data, disabled=True))
        else:
            self.add_item(item=CharacterReliquaryBtn(avatarId=self.avatarId, avatarInfoList=data))

    @classmethod
    def from_message(cls, message: discord.Message, data: List[AvatarInfoDetail], avatarId: Union[int, str]):
        cls = super().from_message(message)
        cls.clear_items()

        avatarInfo = get_avatar_data(avatarInfoList=data, avatarId=avatarId)
        cls.add_item(CharacterSelect(data=data))
        cls.add_item(CharacterInfoBtn(data=avatarInfo))
        cls.add_item(CharacterWeaponBtn(data=avatarInfo))
        if avatarInfo.reliquaryList == []:
            cls.add_item(item=CharacterReliquaryBtn(avatarId=avatarId, avatarInfoList=data, disabled=True))
        else:
            cls.add_item(item=CharacterReliquaryBtn(avatarId=avatarId, avatarInfoList=data))
        return cls

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.author.id

    async def on_error(self, interaction: discord.Interaction, error: Exception, item: Item):
        await interaction.response.send_message(content="알 수 없는 에러가 발생했습니다.", ephemeral=True)

    async def on_timeout(self) -> None:
        await self.message.edit(view=None)

class ReliquaryBackBtn(Button):
    def __init__(self, author: Union[discord.Member, discord.User], avatarId: Union[int, str], avatarInfoList: List[AvatarInfoDetail]):
        self.author = author
        self.avatarId = avatarId
        self.avatarInfoList = avatarInfoList
        super().__init__(label="BACK")
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.followup.edit_message(interaction.message.id,
                                                embed=character_info_embed(get_avatar_data(avatarInfoList=self.avatarInfoList,
                                                                                           avatarId=self.avatarId)),
                                                view=CharacterInfoView(author=self.author,
                                                                       data=self.avatarInfoList,
                                                                       avatarId=self.avatarId))

class ReliquaryBtn(Button):
    def __init__(self, label: str, custom_id: str, disabled: bool = False, reliquaryData: Optional[Reliquary] = None, avatarInfo: Optional[AvatarInfoDetail] = None):
        self.reliquaryData = reliquaryData
        self.avatarInfo = avatarInfo
        super().__init__(label=label, custom_id=custom_id, disabled=disabled)

    def value2percent(self, stat) -> Union[int, str]:        
        if type(stat.value) == int:
            return stat.value
        elif type(stat.value) == float:
            return stat.value2percent()

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.reliquaryData.set_reliquary_name()

        statValues = ""
        for stat in self.reliquaryData.subStatList:
            statValues += f"{stat.type}: {self.value2percent(stat)}\n"

        embed = discord.Embed(title=self.reliquaryData.name, description=f"세트명: {self.reliquaryData.setName}", color=get_element_color(self.avatarInfo.element))
        embed.set_thumbnail(url=self.reliquaryData.icon)
        embed.add_field(name=(f"{self.reliquaryData.mainStat.type}: {self.value2percent(self.reliquaryData.mainStat)}"), value=statValues)
        embed.set_footer(text=self.avatarInfo.name, icon_url=self.avatarInfo.icon)

        await interaction.followup.edit_message(interaction.message.id,
                                                embed=embed)

class CharacterReliquaryView(View):
    def __init__(self, author: Union[discord.User, discord.Member], avatarId: Union[int, str], avatarInfoList: List[AvatarInfoDetail]):
        self.avatarId = avatarId
        self.avatarInfoList = avatarInfoList
        self.avatarInfo = get_avatar_data(avatarId=avatarId, avatarInfoList=avatarInfoList)
        self.author = author

        super().__init__(timeout=None)

        self.add_item(CharacterSelect(avatarInfoList))
        self.add_item(ReliquaryBackBtn(self.author, self.avatarId, self.avatarInfoList))

        for r in ReliquaryType.enumToList():
            reliquaryTypeName = self.get_reliquary_type_name(r)
            if self.reliquaryInList(r):
                reliquaryData = self.get_reliquary_data(reliquaryType=r)
                self.add_item(ReliquaryBtn(label=reliquaryTypeName, custom_id=r, reliquaryData=reliquaryData, avatarInfo=self.avatarInfo))
            else:
                self.add_item(ReliquaryBtn(label=reliquaryTypeName, custom_id=r, disabled=True))

    def reliquaryInList(self, reliquaryType: str) -> bool:
        for r in self.avatarInfo.reliquaryList:
            if r.type == reliquaryType:
                return True
        return False

    def get_reliquary_type_name(self, reliquaryType: str) -> str:
        match reliquaryType:
            case ReliquaryType.flower.value:
                return "생명의 꽃"
            case ReliquaryType.feather.value:
                return "죽음의 깃털"
            case ReliquaryType.sands.value:
                return "시간의 모래"
            case ReliquaryType.goblet.value:
                return "공간의 성배"
            case ReliquaryType.circlet.value:
                return "이성의 왕관"
            case _:
                Logging.LOGGER.warning(f"존재하지 않는 성유물 타입 (type: {reliquaryType})")
                raise ValueError(f"존재하지 않는 성유물 타입 (type: {reliquaryType})")

    def get_reliquary_data(self, reliquaryType: str) -> Reliquary:
        for r in self.avatarInfo.reliquaryList:
            if r.type == reliquaryType:
                return r
        Logging.LOGGER.warning(f"존재하지 않는 성유물 타입 (type: {reliquaryType})")
        raise ValueError(f"존재하지 않는 성유물 타입 (type: {reliquaryType})")

    async def on_error(self, interaction: discord.Interaction, error: Exception, item: Item):
        await interaction.response.send_message(content="알 수 없는 에러가 발생했습니다.", ephemeral=True)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.author.id

    async def on_timeout(self) -> None:
        await self.message.edit(view=None)
