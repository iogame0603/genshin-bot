from discord.ext import commands
from discord import app_commands
import discord
import asyncio

from Utils.Database.query import *
from Types.cookie_type import *
from Utils.Genshin.cookie import get_cookies

class AddCookieModal(discord.ui.Modal, title="쿠키 등록"):
    ltuid_v2 = discord.ui.TextInput(label=Cookie.LTUID_V2, placeholder=Cookie.LTUID_V2 + "를 입력해주세요.")
    ltmid_v2 = discord.ui.TextInput(label=Cookie.LTMID_V2, placeholder=Cookie.LTMID_V2 + "를 입력해주세요.")
    ltoken_v2 = discord.ui.TextInput(label=Cookie.LTOKEN_V2, placeholder=Cookie.LTOKEN_V2 + "를 입력해주세요.")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        insert_cookies(user_id=interaction.user.id, ltuid_v2=self.ltuid_v2.value, ltmid_v2=self.ltmid_v2.value, ltoken_v2=self.ltoken_v2.value)
        await interaction.followup.send(content="쿠키를 등록하였습니다.")

class UpdateCookieModal(discord.ui.Modal):
    def __init__(self, title: str, cookie_type: str):
        self.cookie_type = cookie_type
        super().__init__(title=title)

    cookie = discord.ui.TextInput(label="쿠키를 입력해주세요.")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        update_cookies(user_id=interaction.user.id, cookie_type=self.cookie_type, cookie=self.cookie.value)
        await interaction.followup.send(content="쿠키를 정상적으로 수정하였습니다.")

class GenshinCookie(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    cookie_group = app_commands.Group(name="쿠키", description="쿠키 관련 커맨드입니다.")

    @cookie_group.command(name="등록", description="쿠키를 등록합니다.")
    async def add_cookie(self, interaction: discord.Interaction):
        res_cookies = select_cookies(user_id=interaction.user.id)
        if res_cookies != None:
            await interaction.response.send_message(content="이미 등록된 쿠키가 존재합니다.")
            return
        await interaction.response.send_modal(AddCookieModal())

    @cookie_group.command(name="확인", description="등록된 쿠키를 확인합니다.")
    async def show_cookie(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        cookies = get_cookies(user_id=interaction.user.id)

        cookie_embed = discord.Embed(title=f"{interaction.user.name}님의 쿠키")
        cookie_embed.add_field(name=Cookie.LTUID_V2, value=cookies[Cookie.LTUID_V2], inline=False)
        cookie_embed.add_field(name=Cookie.LTMID_V2, value=cookies[Cookie.LTMID_V2], inline=False)
        cookie_embed.add_field(name=Cookie.LTOKEN_V2, value=cookies[Cookie.LTOKEN_V2], inline=False)

        await interaction.followup.send(embed=cookie_embed)

    @cookie_group.command(name="삭제", description="쿠키를 삭제합니다.")
    async def delete_cookie(self, interaction: discord.Interaction):
        await interaction.response.send_message(content="정말 쿠키를 삭제하시겠습니까?")
        origin_msg = await interaction.original_response()
        await origin_msg.add_reaction("⭕")
        await origin_msg.add_reaction("❌")

        def check(payload: discord.RawReactionActionEvent):
            return payload.user_id == interaction.user.id

        try:
            msg = await self.bot.wait_for("raw_reaction_add", timeout=10.0, check=check)
            if msg.emoji.name == "⭕":
                import exception as exc
                try:
                    delete_cookies(user_id=interaction.user.id)
                    await origin_msg.reply(content="쿠키를 삭제하였습니다.")
                except exc.DataBaseException:
                    await origin_msg.reply(content="처리 중 에러가 발생했습니다.")
            elif msg.emoji.name == "❌":
                await origin_msg.reply(content="작업을 취소하였습니다.")
        except asyncio.TimeoutError:
            await msg.reply(content="시간이 초과되었습니다.")
        finally:
            if not isinstance(interaction.channel, discord.channel.DMChannel):
                await origin_msg.clear_reactions()

    @cookie_group.command(name="수정", description="등록된 쿠키를 수정합니다.")
    async def update_cookie(self, interaction: discord.Interaction, cookie_type: Cookie):
        await interaction.response.send_modal(UpdateCookieModal(title=f"{cookie_type} 수정", cookie_type=cookie_type))

    @commands.is_owner()
    @app_commands.command(name="유저_쿠키_확인", description="특정 유저의 쿠키를 확인합니다.")
    @app_commands.describe(user_id = "사용자 id의 쿠키를 확인합니다.")
    async def show_all_cookies(self, interaction: discord.Interaction, user_id: str):
        await interaction.response.defer(ephemeral=True)

        cookies = get_cookies(user_id=int(user_id))
        
        cookie_embed = discord.Embed(title=f"{user_id}님의 쿠키")
        cookie_embed.add_field(name=Cookie.LTUID_V2, value=cookies[Cookie.LTUID_V2], inline=False)
        cookie_embed.add_field(name=Cookie.LTMID_V2, value=cookies[Cookie.LTMID_V2], inline=False)
        cookie_embed.add_field(name=Cookie.LTOKEN_V2, value=cookies[Cookie.LTOKEN_V2], inline=False)

        await interaction.followup.send(embed=cookie_embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(GenshinCookie(bot))