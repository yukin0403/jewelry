import discord
from discord import Option
from discord.ext import commands
from discord.commands import slash_command
from discord.commands import SlashCommandGroup
import pandas as pd
import numpy as np
import global_value as g
import unicodedata
from datetime import datetime
from schedule import schedule_data
import asyncio

types = [
    "予選",
    "勝者側-準々決",
    "勝者側-準決",
    "敗者側-予選",
    "敗者側-準々決",
    "敗者側-準決",
]


class reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # タスクループのリスト
        self.tasks = []

    # コマンドグループ[reminder]
    reminder = SlashCommandGroup("reminder", "リマインダー")

    async def start_tasks(self):
        # 5 つの異なる type に対してタスクループを開始
        for type in types:
            task = asyncio.create_task(self.loop(type))
            task.type = type  # type パラメータをタスクの属性として保存
            self.tasks.append(task)

    async def loop(self, type):
        while True:  # ループを継続
            current_datetime = datetime.now()  # 現在の日時を取得
            schedules = [
                schedule for schedule in schedule_data if schedule.type == type
            ]
            for schedule in schedules:
                # 現在時刻とschedule_dataの時間差を計測して10分以内の範囲で通知
                time_difference = current_datetime - schedule.datetime
                if (
                    time_difference.total_seconds() >= 0
                    and time_difference.total_seconds() <= 300
                ):
                    message = f"{g.remind_role.mention}\n" f"{schedule.event}です。"
                    await g.remind_ch.send(message)
            await asyncio.sleep(300)  # 5 分間待機

    @commands.Cog.listener()
    async def on_ready(self):

        await self.start_tasks()

    async def stop_task(self, type):
        # type に対応するタスクを停止
        for task in self.tasks:
            if hasattr(task, "type") and task.type == type:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

    @reminder.command(
        name="stop",
        description="リマインダーを止める",
    )
    async def stop(self, ctx, type: Option(str, choices=types)):
        await self.stop_task(type)
        await ctx.interaction.response.send_message(
            f"Type {type} のタスクを停止しました。", ephemeral=True
        )

    @reminder.command(
        name="check",
        description="どのリマインダーが動いてるか確認する",
    )
    async def check(self, ctx):
        running_loops = []
        for task in self.tasks:
            if task.done():
                continue
            if task.get_coro().__qualname__ == "reminder.loop":
                running_loops.append(str(task.type))  # type を取得
        if running_loops:
            await ctx.interaction.response.send_message(
                f"現在動作中のループ: {', '.join(running_loops)}", ephemeral=True
            )
        else:
            await ctx.interaction.response.send_message(
                "現在動作中のループはありません。", ephemeral=True
            )


def setup(bot):
    bot.add_cog(reminder(bot))
