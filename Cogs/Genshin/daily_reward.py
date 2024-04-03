import genshin
import discord
from discord.ext import commands, tasks
from discord import app_commands
from Utils.Database.query import *
from Utils.Genshin.cookie import *
import exception as exc

import traceback

class DailyReward(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.auto_daily_check.start()

    @app_commands.command(name="출석체크", description="출석체크를 합니다.")
    async def daily_reward_check(self, interaction: discord.Interaction):
        await interaction.response.defer()

        client = get_genshin_client(user_id=interaction.user.id)
        if client == None:
            raise exc.GenshinCookieException

        try:
            reward = await client.claim_daily_reward(game=genshin.types.Game.GENSHIN)

            rewardEmbed = discord.Embed(title=f"출석체크 보상")
            rewardEmbed.set_thumbnail(url=reward.icon)
            rewardEmbed.add_field(name="보상", value=reward.name, inline=True)
            rewardEmbed.add_field(name="수량", value=reward.amount, inline=True)

            await interaction.followup.send(embed=rewardEmbed)
        except genshin.errors.AlreadyClaimed:
            await interaction.followup.send("이미 출석체크를 했습니다.")
        except genshin.errors.InvalidCookies:
            await interaction.followup.send("유효하지 않은 쿠키입니다.")

    @tasks.loop(minutes=1)
    async def auto_daily_check(self):
        users = select_users()

        for u in users:
            user_id = u[0]
            user: discord.User = await self.bot.fetch_user(user_id)
            if user == None:
                continue

            client = get_genshin_client(user_id=user_id)
            if client == None:
                continue

            try:
                reward = await client.claim_daily_reward(game=genshin.types.Game.GENSHIN)

                rewardEmbed = discord.Embed(title=f"출석체크 보상")
                rewardEmbed.set_thumbnail(url=reward.icon)
                rewardEmbed.add_field(name="보상", value=reward.name, inline=True)
                rewardEmbed.add_field(name="수량", value=reward.amount, inline=True)

                await user.send(embed=rewardEmbed)
            except genshin.errors.AlreadyClaimed:
                continue
            except genshin.errors.InvalidCookies:
                continue
            except Exception as e:
                Logging.LOGGER.warning(f"{user_id} 출석체크 중 에러 발생")
                continue

async def setup(bot: commands.Bot):
    await bot.add_cog(DailyReward(bot))