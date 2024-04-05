import discord
from discord import app_commands
from discord.ext import commands

from Utils.Genshin.cookie import *
from Types.cookie_type import *
import exception as exc

class GenshinStats(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="데이터_일람", description="데이터 일람 조회합니다.")
    @app_commands.describe(uid="검색할 유저의 uid입니다.")
    async def stats(self, interaction: discord.Interaction, uid: int):
        await interaction.response.defer()
        
        IMAGE_URL = "https://webstatic.hoyoverse.com/upload/op-public/2022/08/04/47a1d15958531397e733abcbfceaad35_1250354074216960329.png?x-oss-process=image%2Fresize%2Cs_600%2Fauto-orient%2C0%2Finterlace%2C1%2Fformat%2Cwebp%2Fquality%2Cq_80"
        client = get_genshin_client(user_id=self.bot.user.id)
        try:
            data = await client.get_genshin_user(uid=uid)
            statsData: genshin.models.genshin.stats.Stats = data.stats

            embed = discord.Embed(title="데이터 일람", description=f"닉네임: {data.info.nickname}")
            embed.set_thumbnail(url=IMAGE_URL)
            embed.add_field(name="활동 일수", value=statsData.days_active)
            embed.add_field(name="업적 달성 개수", value=statsData.achievements)
            embed.add_field(name="흭득한 캐릭터 수", value=statsData.characters)
            embed.add_field(name="나선 비경", value=statsData.spiral_abyss)
            embed.add_field(name="워프 포인트 활성화", value=statsData.unlocked_waypoints)

            embed.add_field(name="바람 신의 눈동자", value=statsData.anemoculi)
            embed.add_field(name="바위 신의 눈동자", value=statsData.geoculi)
            embed.add_field(name="번개 신의 눈동자", value=statsData.electroculi)
            embed.add_field(name="풀의 신의 눈동자", value=statsData.dendroculi)
            embed.add_field(name="물의 신의 눈동자", value=statsData.hydroculi)

            embed.add_field(name="비경 개방", value=statsData.unlocked_domains)

            embed.add_field(name="화려한 보물상자", value=statsData.luxurious_chests)
            embed.add_field(name="진귀한 보물상자", value=statsData.precious_chests)
            embed.add_field(name="정교한 보물상자", value=statsData.exquisite_chests)
            embed.add_field(name="평범한 보물상자", value=statsData.common_chests)
            embed.add_field(name="신묘한 보물상자", value=statsData.remarkable_chests)

            await interaction.followup.send(embed=embed)
        except genshin.errors.AccountNotFound:
            await interaction.followup.send(content=f"{uid} 계정을 찾을 수 없습니다.")
        except genshin.errors.DataNotPublic:
            await interaction.followup.send(content=f"{uid} 계정은 비공개 계정입니다.")
        except genshin.errors.InvalidCookies:
            raise exc.GenshinInvalidCookies

async def setup(bot: commands.Bot):
    await bot.add_cog(GenshinStats(bot))