import discord
from discord import app_commands
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="핑", description="현재 핑을 확인합니다.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(content=f":ping_pong: {round(self.bot.latency, 2) * 1000}ms")

async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))