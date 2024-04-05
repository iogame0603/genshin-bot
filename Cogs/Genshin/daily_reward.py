import genshin
import discord
from discord.ext import commands, tasks
from discord import app_commands
from discord.app_commands import Choice
from Utils.Database.query import *
from Utils.Genshin.cookie import *
import exception as exc

class DailyReward(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.auto_daily_check.start()

    @app_commands.command(name="출석체크", description="출석체크를 합니다.")
    @app_commands.describe(game="출석체크를 할 게임입니다.")
    @app_commands.choices(game=[
        Choice(name="원신", value=genshin.types.Game.GENSHIN),
        Choice(name="붕괴", value=genshin.types.Game.HONKAI),
        Choice(name="스타레일", value=genshin.types.Game.STARRAIL)
    ])
    async def daily_reward_check(self, interaction: discord.Interaction, game: Choice[str]):
        await interaction.response.defer()

        client = get_genshin_client(user_id=interaction.user.id)

        try:
            reward = await client.claim_daily_reward(game=game.value)

            rewardEmbed = discord.Embed(title=f"출석체크 보상")
            rewardEmbed.set_thumbnail(url=reward.icon)
            rewardEmbed.add_field(name="보상", value=reward.name, inline=True)
            rewardEmbed.add_field(name="수량", value=reward.amount, inline=True)

            await interaction.followup.send(embed=rewardEmbed)
        except genshin.errors.AlreadyClaimed:
            await interaction.followup.send("이미 출석체크를 했습니다.")
        except genshin.errors.InvalidCookies:
            raise exc.GenshinInvalidCookies
        except genshin.errors.GenshinException:
            await interaction.followup.send(f"{game.name} 계정을 찾을 수 없습니다.")

    @tasks.loop(minutes=1)
    async def auto_daily_check(self):
        users = select_users()

        for u in users:
            user_id = u[0]
            user: discord.User = await self.bot.fetch_user(user_id)
            if user == None:
                continue

            try:
                client = get_genshin_client(user_id=user_id)

                reward = await client.claim_daily_reward(game=genshin.types.Game.GENSHIN)

                rewardEmbed = discord.Embed(title=f"출석체크 보상")
                rewardEmbed.set_thumbnail(url=reward.icon)
                rewardEmbed.add_field(name="보상", value=reward.name, inline=True)
                rewardEmbed.add_field(name="수량", value=reward.amount, inline=True)

                await user.send(embed=rewardEmbed)
            except (genshin.errors.AlreadyClaimed,
                    genshin.errors.InvalidCookies,
                    genshin.CookieException,
                    exc.GenshinInvalidCookies):
                continue
            except Exception as e:
                Logging.LOGGER.warning(f"{user_id} 출석체크 중 에러 발생")
                continue

async def setup(bot: commands.Bot):
    await bot.add_cog(DailyReward(bot))