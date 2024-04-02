from datetime import timedelta
import discord
from discord import app_commands
from discord.ext import commands

import genshin

from Utils.Genshin.cookie import get_genshin_client
import exception as exc


class Notes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="실시간_메모", description="실시간 메모를 확인합니다.")
    async def notes(self, interaction: discord.Interaction):
        await interaction.response.defer()

        client = get_genshin_client(user_id=interaction.user.id)
        if client == None:
            raise exc.GenshinCookieException
    
        try:
            note = await client.get_genshin_notes()

            notesEmbed = discord.Embed(title="실시간 노트")

            ## 레진
            notesEmbed.add_field(name=f"<:resin:1050037836956565524> {note.current_resin} / {note.max_resin}",
                                  value=f"남은 시간: {str(timedelta(seconds=note.remaining_resin_recovery_time.seconds))}",
                                  inline=False)

            ## 일일퀘스트
            is_claimed_commission_reward = note.daily_task.claimed_commission_reward
            claimed_commission_reward_msg = ""
            if is_claimed_commission_reward:
                claimed_commission_reward_msg = "오늘의 일일퀘스트 보상을 받았습니다."
            else:
                claimed_commission_reward_msg = "아직 일일퀘스트 보상을 받지 않았습니다."

            notesEmbed.add_field(name=f"<:daily_task:1218141110355099718> {note.daily_task.completed_tasks} / {note.daily_task.max_tasks}",
                                       value=claimed_commission_reward_msg,
                                       inline=False)
            
            exp = note.expeditions

            ## 탐사
            if exp == []:
                await interaction.followup.send(content="현재 진행중인 탐사가 없습니다.")

            exp_value = ""

            for e in exp:
                # status = ""
                # if e.finished:
                #     status = "탐사 완료"
                # else:
                #     status = "탐사중"
                exp_value += f"남은 시간: {str(timedelta(seconds=e.remaining_time.seconds))}\n"
                
            notesEmbed.add_field(name=f"탐사 파견 제한 ({len(exp)} / {note.max_expeditions})", value=exp_value, inline=False)
            
            ## 선계 화폐
            notesEmbed.add_field(name=f"<:currency:1218895320633573516> {note.current_realm_currency} / {note.max_realm_currency}",
                                     value=f"남은 시간: {str(timedelta(seconds=note.realm_currency_recovery_time.second))}",
                                     inline=False)

            await interaction.followup.send(embed=notesEmbed)

        except genshin.errors.InvalidCookies:
            raise exc.GenshinInvalidCookies

    @app_commands.command(name="일일퀘스트", description="현재 일일퀘스트 현황을 확인합니다.")
    async def daily_tasks(self, interaction: discord.Interaction):
        await interaction.response.defer()

        client = get_genshin_client(user_id=interaction.user.id)
        if client == None:
            raise exc.GenshinCookieException
    
        try:
            note = await client.get_genshin_notes()

            is_claimed_commission_reward = note.daily_task.claimed_commission_reward
            claimed_commission_reward_msg = ""
            if is_claimed_commission_reward:
                claimed_commission_reward_msg = "오늘의 일일퀘스트 보상을 받았습니다."
            else:
                claimed_commission_reward_msg = "아직 일일퀘스트 보상을 받지 않았습니다."

            daily_task_embed = discord.Embed(title="일일퀘스트 현황")
            daily_task_embed.add_field(name=f"<:daily_task:1218141110355099718> {note.daily_task.completed_tasks} / {note.daily_task.max_tasks}",
                                       value=claimed_commission_reward_msg)
            
            await interaction.followup.send(embed=daily_task_embed)
        except genshin.errors.InvalidCookies:
            raise exc.GenshinInvalidCookies

    @app_commands.command(name="탐사", description="현재 탐사 현황을 확인합니다.")
    async def expeditions(self, interaction: discord.Interaction):
        await interaction.response.defer()

        client = get_genshin_client(user_id=interaction.user.id)
        if client == None:
            raise exc.GenshinCookieException
    
        try:
            note = await client.get_genshin_notes()

            exp = note.expeditions

            if exp == []:
                await interaction.followup.send(content="현재 진행중인 탐사가 없습니다.")

            expEmbed = discord.Embed(title="탐사 현황", description=f"{len(exp)} / {note.max_expeditions}")

            for e in exp:
                status = ""
                if e.finished:
                    status = "탐사 완료"
                else:
                    status = "탐사중"
                td = str(timedelta(seconds=e.remaining_time.seconds))
                
                expEmbed.add_field(name=status, value=f"남은 시간: {td}", inline=False)

            await interaction.followup.send(embed=expEmbed)
        except genshin.errors.InvalidCookies:
            raise exc.GenshinInvalidCookies
        
    @app_commands.command(name="레진", description="현재 레진을 확인합니다.")
    async def resin(self, interaction: discord.Interaction):
        await interaction.response.defer()

        client = get_genshin_client(user_id=interaction.user.id)
        if client == None:
            raise exc.GenshinCookieException
    
        try:
            note = await client.get_genshin_notes()

            td = str(timedelta(seconds=note.remaining_resin_recovery_time.seconds))

            resinEmbed = discord.Embed(title="레진")
            resinEmbed.add_field(name=f"<:resin:1050037836956565524> {note.current_resin} / {note.max_resin}",
                                  value=f"남은 시간: {td}")
            
            await interaction.followup.send(embed=resinEmbed)
        except genshin.errors.InvalidCookies:
            await interaction.followup.send("유효하지 않은 쿠키입니다.")

    @app_commands.command(name="선계_화폐", description="현재 선계 화페를 확인합니다.")
    async def currency(self, interaction: discord.Interaction):
        await interaction.response.defer()

        client = get_genshin_client(user_id=interaction.user.id)
        if client == None:
            raise exc.GenshinCookieException

        try:
            note = await client.get_genshin_notes()

            currencyEmbed = discord.Embed(title="선계 화폐")
            currencyEmbed.add_field(name=f"<:currency:1218895320633573516> {note.current_realm_currency} / {note.max_realm_currency}",
                                     value=f"남은 시간: {str(timedelta(seconds=note.realm_currency_recovery_time.second))}")

            await interaction.followup.send(embed=currencyEmbed)
        except genshin.errors.InvalidCookies:
            raise exc.GenshinInvalidCookies
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Notes(bot))