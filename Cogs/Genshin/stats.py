from discord.ext import commands
from discord import app_commands
import discord
from typing import Sequence

from Utils.Genshin.cookie import *
from Types.cookie_type import *
import exception as exc

class GenshinStats(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="전적", description="전적 확인합니다.")
    @app_commands.describe(uid="검색할 유저의 uid입니다.")
    async def stats(self, interaction: discord.Interaction, uid: int):
        await interaction.response.defer()

        client = get_genshin_client(user_id=self.bot.user.id)
        try:
            data = await client.get_genshin_user(uid=uid)
            stats: genshin.models.genshin.stats.Stats = data.stats
            info: genshin.models.hoyolab.UserInfo = data.info

            stats_embed = discord.Embed(title=f"{info.nickname}님의 전적", description=f"level: {info.level}\nuid: {uid}")
            stats_embed.set_thumbnail(url="https://webstatic.hoyoverse.com/upload/op-public/2022/08/04/47a1d15958531397e733abcbfceaad35_1250354074216960329.png?x-oss-process=image%2Fresize%2Cs_600%2Fauto-orient%2C0%2Finterlace%2C1%2Fformat%2Cwebp%2Fquality%2Cq_80")

            # TODO
            # stats_embed.add_field(name="활동 일수", value=stats.days_active, inline=True)
            # stats_embed.add_field(name="업적 달성 개수", value=stats.achievements, inline=True)
            # stats_embed.add_field(name="획득한 캐릭터", value=stats.characters, inline=True)
            # stats_embed.add_field(name="나선 비경", value=stats.spiral_abyss, inline=True)

            await interaction.followup.send(embed=stats_embed)
        except genshin.errors.AccountNotFound:
            await interaction.followup.send(content=f"{uid} 계정을 찾을 수 없습니다.")
        except genshin.errors.DataNotPublic:
            await interaction.followup.send(content=f"{uid} 계정은 비공개 계정입니다.")
        except genshin.errors.InvalidCookies:
            await interaction.followup.send(content="유효하지 않은 쿠키입니다.")
        
    @app_commands.command(name="탐사도", description="탐사도를 확인합니다.")
    @app_commands.describe(uid="검색할 유저의 uid입니다.")
    async def t(self, interaction: discord.Interaction, uid: int):
        await interaction.response.defer()
        client = get_genshin_client(user_id=self.bot.user.id)
        try:
            data = await client.get_genshin_user(uid=uid)
            info: genshin.models.hoyolab.UserInfo = data.info
            exp: Sequence[genshin.models.genshin.Exploration] = data.explorations

            exp_embed = discord.Embed(title=f"{info.nickname}님의 탐사도")
            for e in exp:
                values = f"탐사도: {e.explored}%"
                for o in e.offerings:
                    if o.name == "Reputation":
                        values += f"\n평판: {o.level}"
                    else:
                        values += f"\n{o.name}: {o.level}"
                exp_embed.add_field(name=e.name, value=values, inline=False)

            await interaction.followup.send(embed=exp_embed)

        except genshin.errors.AccountNotFound:
            await interaction.followup.send(content=f"{uid} 계정을 찾을 수 없습니다.")
        except genshin.errors.DataNotPublic:
            await interaction.followup.send(content=f"{uid} 계정은 비공개 계정입니다.")
        except genshin.errors.InvalidCookies:
            raise exc.GenshinInvalidCookies
        
async def setup(bot: commands.Bot):
    await bot.add_cog(GenshinStats(bot))