import discord
from discord import app_commands
from discord.ext import commands
from Utils.Genshin.cookie import *

import exception as exc
import matplotlib.pyplot as plt
from typing import List
from datetime import datetime


class Dirary(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # 원석 수입 구성 원형차트
    def create_pie_chart(self, categories: List[genshin.models.genshin.DiaryActionCategory], channel_id: int, user_id = int) -> None:
        labels = []
        values = [c.percentage for c in categories]

        for c in categories:
            labels.append(f"{c.name} ({c.percentage}%)")
        
        plt.rc("font", family="Malgun Gothic")
        plt.pie(x=values, wedgeprops={'linewidth': 1.5, 'edgecolor': 'white'})
        plt.legend(loc="center right",  labels=labels, bbox_transform=plt.gcf().transFigure, bbox_to_anchor=(0.9, 0.5))
        plt.subplots_adjust(left=0.0, bottom=0.1, right=0.7)

        try:
            plt.savefig(f"images/diary/{channel_id}/{user_id}_diary.png", bbox_inches="tight")
        except FileNotFoundError:
            os.mkdir(f"{os.path.abspath('')}/images/diary/{channel_id}")
            plt.savefig(f"images/diary/{channel_id}/{user_id}_diary.png", bbox_inches="tight")

    @app_commands.command(name="여행자_핸드북", description="여행자 핸드북을 확인합니다.")
    async def diary(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            client = get_genshin_client(user_id=interaction.user.id)

            diary = await client.get_diary(lang="ko-kr")
            data: genshin.models.genshin.MonthDiaryData = diary.data

            self.create_pie_chart(categories=data.categories, channel_id=interaction.channel_id, user_id=interaction.user.id)

            embed = discord.Embed(title=f"{diary.nickname}님의 여행일지", description=f"uid: {diary.uid}")
            embed.set_thumbnail(url="https://webstatic.hoyoverse.com/upload/op-public/2022/08/04/ff1419346528dfd64d77c35701ecd106_7596171599082743274.png?x-oss-process=image%2Fresize%2Cs_600%2Fauto-orient%2C0%2Finterlace%2C1%2Fformat%2Cwebp%2Fquality%2Cq_80")
            file = discord.File(f"{os.path.abspath('')}/images/diary/{interaction.channel_id}/{interaction.user.id}_diary.png", filename=f"{interaction.user.id}_diary.png")
            embed.set_image(url=f"attachment://{interaction.user.id}_diary.png")
            embed.add_field(name=f"{datetime.today().month}월 원석/모라 수입", value=f"원석: {data.current_primogems}\n모라: {data.current_mora}", inline=False)
            embed.add_field(name="원석 수입 구조", value="", inline=False)

            await interaction.followup.send(file=file, embed=embed)

            try:
                os.remove(f"{os.path.abspath('')}/images/diary/{interaction.channel_id}/{interaction.user.id}_diary.png")
            except:
                pass

        except genshin.errors.InvalidCookies:
            raise exc.GenshinInvalidCookies

async def setup(bot: commands.Bot):
    await bot.add_cog(Dirary(bot))