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

# モーダルウィンドウ
class MyModal(discord.ui.Modal):
    def __init__(self, user_name: str, user_id: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user_name = user_name
        self.user_id = user_id

        self.add_item(discord.ui.InputText(label="代表者所属サークル名",))
        self.add_item(discord.ui.InputText(label="代表者連絡先(X_ID)", value="@"))

    async def callback(self, interaction: discord.Interaction):
        # 変数に格納
        dt_now = datetime.datetime.now()
        timestamp = dt_now.strftime('%m/%d %H:%M:%S') # 02/04 21:04:15
        club_name = unicodedata.normalize('NFKC', str(self.children[0].value))
        user_name = str(self.user_name)
        user_id = str(self.user_id)
        x_id = str(self.children[1].value)
        new_raw = [timestamp, club_name, user_name, user_id, x_id]
        # シート[club]読み込み
        g.club_data = g.get_sheet_all_values(g.club_ws)
        club_name_list = g.club_data['club_name'].tolist()
        # 登録されているサークルが規定数に達していないか調べる
        if len(club_name_list) >= 42:
            await interaction.response.send_message(f"サークル登録数が規定数に達しました。登録が締め切られていないか確認してください。", ephemeral=True)
            return
        if len(club_name_list) == 41:
            await g.register_ch.send(f"{g.admins_mention}\n"
                                     f"サークル登録数が規定数に達しました。重複入力がなければ登録を締め切ってください。")
            g.input_club_ws.append_row(new_raw)
            await interaction.response.send_message(f"サークル名:{club_name}\n"
                                                    f"代表者登録名:{user_name}\n"
                                                    f"代表者連絡先:{x_id}", ephemeral=True)
            return
        # スプシに書き込み
        else:
            g.input_club_ws.append_row(new_raw)
            await interaction.response.send_message(f"サークル名:{club_name}\n"
                                                    f"代表者登録名:{user_name}\n"
                                                    f"代表者連絡先:{x_id}", ephemeral=True)
            return

# サークル登録
class club_register(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @slash_command(
        name = "club_register",
        description = "サークル登録",
    )
    async def register(self, ctx):
        user_name = str(ctx.author.display_name)
        user_id = str(ctx.author.id)
        modal = MyModal(user_name, user_id, title="サークル登録")
        await ctx.send_modal(modal=modal)

def setup(bot):
	bot.add_cog(club_register(bot))