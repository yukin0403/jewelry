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
    def __init__(self, uma_list: list, user_list: list, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.uma_list = uma_list
        self.user_list = user_list

        self.add_item(discord.ui.InputText(label="サークル名"))
        self.add_item(
            discord.ui.InputText(label="トレーナーID", min_length=9, max_length=12)
        )
        self.add_item(
            discord.ui.InputText(
                label="意気込み",
                required=False,
                placeholder="任意",
                style=discord.InputTextStyle.long,
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="登録ウマ娘(確認用)",
                required=False,
                style=discord.InputTextStyle.long,
                value=f"-----このフォームは確認用です。変更したい場合はキャンセルを押してください。-----\n"
                f"ウマ娘1:{self.uma_list[0]}({self.uma_list[1]})\n"
                f"ウマ娘2:{self.uma_list[2]}({self.uma_list[3]})\n"
                f"ウマ娘3:{self.uma_list[4]}({self.uma_list[5]})",
            )
        )

    async def callback(self, interaction: discord.Interaction):
        # 変数に格納
        dt_now = datetime.datetime.now()
        timestamp = dt_now.strftime("%m/%d %H:%M:%S")  # 02/04 21:04:15
        club_name = unicodedata.normalize("NFKC", str(self.children[0].value))
        user_name = self.user_list[0]
        role = self.user_list[2]
        un1 = self.uma_list[0]
        up1 = self.uma_list[1]
        un2 = self.uma_list[2]
        up2 = self.uma_list[3]
        un3 = self.uma_list[4]
        up3 = self.uma_list[5]
        trainer_id = str(self.children[1].value)
        user_id = self.user_list[1]
        enthusiasm = str(self.children[2].value)
        new_raw = [
            timestamp,
            club_name,
            user_name,
            role,
            un1,
            up1,
            un2,
            up2,
            un3,
            up3,
            trainer_id,
            user_id,
            enthusiasm,
        ]
        # サークル名リストを読み込んで入力したサークル名と一致するか調べる
        club_name_list = g.club_data["club_name"].tolist()
        if not (club_name in club_name_list):
            await interaction.response.send_message(
                "一致するサークル名がありません。\n"
                "登録したサークル名を確認するか、サークル登録を行ってからウマ娘登録を実行してください。",
                ephemeral=True,
            )
            return
        # 役職重複確認
        club_member_list = g.member_data[g.member_data["club_name"] == club_name]
        role_list = club_member_list["role"].tolist()
        if role in role_list:
            register_name = str(
                club_member_list.loc[
                    club_member_list["role"] == role, "user_name"
                ].values[0]
            )
            await interaction.response.send_message(
                f"{role}には既に{register_name}さんが登録されています。\n"
                "修正が必要な場合は運営に問い合わせをお願いします。",
                ephemeral=True,
            )
            return
        # スプシに書き込み
        g.input_member_ws.append_row(new_raw)
        await interaction.response.send_message(
            f"サークル名:{club_name}\n"
            f"登録名:{user_name}\n"
            f"役割:{role}\n"
            f"ウマ娘1:{un1} ({up1})\n"
            f"ウマ娘2:{un2} ({up2})\n"
            f"ウマ娘3:{un3} ({up3})\n"
            f"トレーナーID:{trainer_id}",
            ephemeral=True,
        )


# ウマ娘登録
class uma_register(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @slash_command(
        name="uma_register",
        description="ウマ娘登録",
    )
    async def register(
        self,
        ctx,
        役割: Option(str, choices=["先鋒", "次鋒", "中堅", "副将", "大将"]),
        ウマ娘id1: Option(str, min_length=3, max_length=3),
        ウマ娘脚質1: Option(str, choices=["大逃げ", "逃げ", "先行", "差し", "追込"]),
        ウマ娘id2: Option(str, min_length=3, max_length=3),
        ウマ娘脚質2: Option(str, choices=["大逃げ", "逃げ", "先行", "差し", "追込"]),
        ウマ娘id3: Option(str, min_length=3, max_length=3),
        ウマ娘脚質3: Option(str, choices=["大逃げ", "逃げ", "先行", "差し", "追込"]),
    ):
        # 全角数字を半角数字に変換して、IDに対応したウマ娘の名前を取得
        uma_ids = [
            unicodedata.normalize("NFKC", uma_id)
            for uma_id in [ウマ娘id1, ウマ娘id2, ウマ娘id3]
        ]
        uma_names = [g.uma_list_mapping.get(uma_id) for uma_id in uma_ids]
        # ウマ娘名が存在しない場合
        if any(uma_name is None for uma_name in uma_names):
            await ctx.interaction.response.send_message(
                "存在しないウマ娘IDが指定されています。", ephemeral=True
            )
            return
        # ほしい要素をリストに格納してモーダルに送信
        else:
            uma_list = [
                uma_names[0],
                ウマ娘脚質1,
                uma_names[1],
                ウマ娘脚質2,
                uma_names[2],
                ウマ娘脚質3,
            ]
            user_list = [str(ctx.author.display_name), str(ctx.author.id), 役割]
            modal = MyModal(uma_list, user_list, title="ウマ娘登録")
            await ctx.send_modal(modal=modal)


def setup(bot):
    bot.add_cog(uma_register(bot))
