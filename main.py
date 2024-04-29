import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

import traceback
from Utils.util import Logging

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
COMMAND_PREFIX = "/"

class GenshinBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=COMMAND_PREFIX, intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        for file in os.listdir("./Cogs"):
            if file.endswith(".py"):
                await bot.load_extension(f"Cogs.{file[:-3]}")
            elif file != "__pycache__":
                for f in os.listdir("./Cogs/" + file):
                    if f.endswith(".py"):
                        await bot.load_extension(f"Cogs.{file}.{f[:-3]}")

        await self.tree.sync()

    async def on_ready(self):
        # only slash command
        await self.change_presence(status=discord.Status.online, activity=discord.Game(f"{COMMAND_PREFIX}help 하는중"))
        print("bot starting...")

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

bot = GenshinBot()
bot.remove_command("help")

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    import exception as exc

    match type(error):
        case exc.GenshinCookieException:
            await interaction.followup.send(content="등록된 쿠키가 없습니다.")
        case exc.GenshinInvalidCookies:
            await interaction.followup.send(content="유효하지 않은 쿠키입니다.")
        case exc.DataBaseException:
            await interaction.followup.send(content="처리 중 에러가 발생했습니다.")
        case _:
            Logging.LOGGER.exception(f"알 수 없는 에러")
            await interaction.followup.send(content="알 수 없는 에러가 발생했습니다.", ephemeral=True)
            
bot.run(DISCORD_BOT_TOKEN)