import discord
from discord import Option
from discord.ext import commands
from discord.commands import slash_command
from discord.commands import SlashCommandGroup
import pandas as pd
import numpy as np
import global_value as g
import unicodedata
import datetime


# 勝ったウマを選択
class UserInputSelect1(discord.ui.Select):
    def __init__(
        self, bot: commands.Bot, options: list[discord.SelectOption] = ...
    ) -> None:
        super().__init__(placeholder="選択", options=options)
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        # 変数に格納
        win_uma = self.values[0]
        transmission_user = self.view.result_info[0]
        transmission_user_name = self.view.result_info[1]
        win_member = self.view.result_info[2]
        win_room = self.view.result_info[3]
        # 役割取得
        user_info = g.member_data[g.member_data["user_name"] == str(win_member)]
        role = user_info["role"].to_string(header=False, index=False)
        # 結果一覧取得
        result_data = g.get_sheet_all_values(g.result_ws)
        # 送信した結果と取得した結果一覧のroom列とrole列結合
        room_role = str(win_room) + str(role)
        result_list = (result_data["room"] + result_data["role"]).tolist()
        # スプシに書き込み
        new_raw = [win_room, role, win_member, win_uma, transmission_user_name]
        g.result_ws.append_row(new_raw)
        # 特殊記号エスケープ
        transmission_user_name = g.symbols_escape(transmission_user_name)
        win_member = g.symbols_escape(win_member)
        # /resultしたチャンネルに結果送信
        result_message = (
            f"送信者: {transmission_user_name}\n"
            f"----------------------------------------\n"
            f"部屋名: {win_room}\n"
            f"役割: {role}\n"
            f"勝者: {win_member}\n"
            f"勝利ウマ娘: {win_uma}\n"
            f"----------------------------------------\n"
        )
        await interaction.response.send_message(result_message, ephemeral=True)
        await self.view.delete_message.delete()
        # 既に同じ部屋+役割の結果が入力されていた場合警告
        if room_role in result_list:
            await g.repeat_result_ch.send(
                f"重複した入力です。確認お願いします。\n"
                f"{g.admins_mention}\n"
                f"----------------------------------------\n"
                f"再送信した理由をこの結果に返信お願いします。重複入力した覚えがない場合はその旨返信お願いします。\n"
                f"{transmission_user.mention}\n\n\n"
                f"{result_message}"
            )
            return
        else:
            await g.result_ch.send(result_message)
            return


class WinUmaView(discord.ui.View):
    def __init__(
        self, bot: commands.Bot, options: list[discord.SelectOption], result_info: list
    ):
        super().__init__(timeout=10, disable_on_timeout=True)
        self.bot = bot
        self.result_info = result_info
        self.add_item(UserInputSelect1(bot=self.bot, options=options))


# 結果入力起動
class result(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @slash_command(
        name="result",
        description="結果入力",
    )
    @commands.cooldown(1, 5)
    async def result(self, ctx):
        options: list[discord.SelectOption] = []
        transmission_user_id = int(ctx.author.id)
        transmission_user = ctx.guild.get_member(transmission_user_id)
        transmission_user_name = str(ctx.author)
        win_member = str(ctx.author.display_name)
        win_member_id = str(ctx.author.id)
        win_room = str(ctx.channel)
        result_info = [transmission_user, transmission_user_name, win_member, win_room]
        # 登録名と表示名が一致してるかチェック
        id_list = g.member_data["user_id"].tolist()
        id_list_str = [str(i) for i in id_list]
        if not (win_member_id in id_list_str):
            await ctx.interaction.response.send_message(
                f"ウマ娘登録がされていません。", ephemeral=True
            )
            return
        else:
            uma_list = g.member_data[g.member_data["user_id"] == win_member_id]
            for i in range(1, 4):
                uma_name = uma_list[f"uma_name{i}"].to_string(header=False, index=False)
                options.append(discord.SelectOption(label=uma_name))
            await ctx.interaction.response.send_message(
                f"1位のウマ娘の名前を入力してください。",
                view=WinUmaView(bot=self.bot, options=options, result_info=result_info),
                ephemeral=True,
            )
            delete_message = await ctx.interaction.original_response()
            WinUmaView.delete_message = delete_message

    @result.error
    async def on_result_error(self, ctx: commands.Context, error):

        if isinstance(error, commands.CommandOnCooldown):
            retry_after_int = round(int(error.retry_after), 2)
            return await ctx.interaction.response.send_message(
                f"クールダウン中です。{retry_after_int}秒後使用可能です。",
                ephemeral=True,
            )


def setup(bot):
    bot.add_cog(result(bot))
