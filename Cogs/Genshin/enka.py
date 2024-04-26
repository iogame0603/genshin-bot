import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

from enkaNetwork.enkaNetworkClient import EnkaNetworkClient
from enkaNetwork.exception import HttpException

from Views.enka.genshinEnka import CharacterInfoView, character_info_embed

from Utils.util import Logging

class GenshinEnka(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="엔카", description="엔카 네트워크의 정보를 확인합니다.")
    @app_commands.describe(uid="검색할 유저의 uid입니다.", game="검색할 게임입니다. 기본값: 원신")
    @app_commands.choices(game=[
        Choice(name="원신", value=0),
        Choice(name="스타레일", value=1)
    ])
    async def enkaNetwork(self, interaction: discord.Interaction, uid: int, game: Choice[int] = 0):
        await interaction.response.defer()

        try:
            client = EnkaNetworkClient()

            if game == 0:
                data = await client.fetch_genshin_user(uid=uid)
                if len(data.avatarInfoList) == 0:
                    await interaction.followup.send(content=f"{uid}계정은 공개한 캐릭터가 없습니다.")
                    return
                characterInfoView = CharacterInfoView(author=interaction.user, data=data.avatarInfoList, avatarId=data.avatarInfoList[0].id)
                characterInfoView.message = await interaction.followup.send(embed=character_info_embed(data.avatarInfoList[0]),
                                                                            view=characterInfoView)
            elif game == 1:
                data = await client.fetch_starrail_user(uid=uid)
                
                # TODO

        except HttpException:
            Logging.LOGGER.warning("데이터 로드 실패")
            await interaction.followup.send(content="데이터를 불러오는데 실패하였습니다.")

    @app_commands.command(name="에셋_업데이트", description="enka network assets를 업데이트합니다.")
    @commands.is_owner()
    async def update_enka(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        client = EnkaNetworkClient()
        try:
            await client.update_genshin_assets()
            await interaction.followup.send(content="에셋 업데이트가 완료되었습니다.", ephemeral=True)
        except:
            Logging.LOGGER.exception("enka network 에셋 업데이트 실패")
            await interaction.followup.send(content="에셋 업데이트 실패", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(GenshinEnka(bot))