import discord
from discord import app_commands
from discord.ui import Button, View
from discord.ext import commands
import genshin

from typing import Sequence, Union, List

import genshin.models
from Utils.Genshin.cookie import *
import exception as exc

class ExplorationBtn(Button):
    def __init__(self, exploration: genshin.models.genshin.Exploration, childrenExploration: List[genshin.models.genshin.Exploration] = None):
        self.explorationData = exploration
        self.childrenExploration = childrenExploration
        super().__init__(label=exploration.name, custom_id=str(exploration.id))

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        embed = discord.Embed(title=f"{self.explorationData.name} 탐사도")

        if self.explorationData.id == 6:
            # 층암거연
            embed.add_field(name=self.explorationData.name, value=f"{self.explorationData.explored}%")
            embed.add_field(name=self.childrenExploration[0].name, value=f"{self.childrenExploration[0].explored}%")
        elif self.childrenExploration == None:
            embed.description=f"합계: {self.explorationData.explored}%"
            for ae in self.explorationData.area_exploration_list:
                embed.add_field(name=ae.name, value=f"{ae.exploration_percentage}%")
        elif self.childrenExploration != None:
            for ce in self.childrenExploration:
                embed.add_field(name=ce.name, value=f"{ce.explored}%")

        embed.set_thumbnail(url=self.explorationData.icon)
        await interaction.followup.edit_message(interaction.message.id, embed=embed)

class ExplorationView(View):
    def __init__(self, author: Union[discord.Member, discord.User], data: Sequence[genshin.models.genshin.Exploration]):
        self.explorationData = data
        self.author = author
        super().__init__(timeout=None)

        for e in self.explorationData:
            if e.parent_id == 0:
                childrenExploration = self.find_children_explorations(e.id)
                if childrenExploration == []:
                    self.add_item(ExplorationBtn(e))
                else:
                    self.add_item(ExplorationBtn(e, childrenExploration))

    def find_children_explorations(self, id: int) -> List[genshin.models.genshin.Exploration]:
        newExpList = []
        for e in self.explorationData:
            if e.parent_id == id:
                newExpList.append(e)
        return newExpList

    async def interaction_check(self, interaction: discord.Interaction):
        return self.author.id == interaction.user.id

class GenshinExplorations(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="탐사도", description="탐사도를 조회합니다.")
    @app_commands.describe(uid="검색할 유저의 uid입니다.")
    async def exploration(self, interaction: discord.Interaction, uid: int):
        await interaction.response.defer()
        client: genshin.Client = get_genshin_client(user_id=self.bot.user.id)
        try:
            data = await client.get_genshin_user(uid=uid)
            exp: Sequence[genshin.models.genshin.Exploration] = sorted(data.explorations, key=lambda e: e.id)

            await interaction.followup.send(view=ExplorationView(interaction.user, exp))
        except ValueError:
            await interaction.followup.send(content=f"``{uid}`` 알 수 없는 uid입니다.")
        except genshin.errors.AccountNotFound:
            await interaction.followup.send(content=f"{uid} 계정을 찾을 수 없습니다.")
        except genshin.errors.DataNotPublic:
            await interaction.followup.send(content=f"{uid} 계정은 비공개 계정입니다.")
        except genshin.errors.InvalidCookies:
            raise exc.GenshinInvalidCookies

async def setup(bot: commands.Bot):
    await bot.add_cog(GenshinExplorations(bot))