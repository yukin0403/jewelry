import discord
from discord import Option
from discord.ext import commands
from discord.commands import slash_command
from discord.commands import SlashCommandGroup
import pandas as pd
import numpy as np
import global_value as g
import settings.group as gr
import unicodedata
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
ADMIN_IDS = os.getenv("ADMIN_IDS").split(",")
REMIND_ROLE_ID = int(os.getenv("REMIND_ROLE_ID"))


class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # コマンドグループ[admin]
    admin = SlashCommandGroup("admin", "管理者用コマンド")

    # シート再読み込み
    @admin.command(
        name="read",
        description="スプレッドシート読み込み",
    )
    @commands.has_role("大会運営")
    async def read(self, ctx):
        sheets = [g.room_ws, g.member_ws, g.club_ws]
        sheet_data_lists = []
        for sheet in sheets:
            data = g.get_sheet_all_values(sheet)
            sheet_data_lists.append(data)
        # 読み込んだシートを格納
        g.room_data = sheet_data_lists[0]
        g.room_data["room_role"] = g.room_data["room"] + g.room_data["role"]
        g.member_data = sheet_data_lists[1]
        g.club_data = sheet_data_lists[2]

        # 運営陣取得
        admins = []
        for admin_id in ADMIN_IDS:
            user = ctx.guild.get_member(int(admin_id))
            admins.append(user)
        g.admins_mention = " ".join([admin.mention for admin in admins])
        # リマインド先ロール取得
        g.remind_role = ctx.guild.get_role(REMIND_ROLE_ID)

        await ctx.interaction.response.send_message(
            f"スプレッドシートを読み込みました。", ephemeral=True
        )

    # 鯖全員から指定のロールを消す
    @admin.command(
        name="role_delete",
        description="ロール削除",
    )
    @commands.has_role("大会運営")
    async def role_delete(self, ctx, role_name: str):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        await ctx.interaction.response.send_message(
            f"【ロール:{role}】を全員から削除しました。", ephemeral=True
        )
        for member in ctx.guild.members:
            if not member.bot:
                await member.remove_roles(role)

    # memberシートの全員にロール付与
    @admin.command(
        name="role_append",
        description="ロール付与",
    )
    @commands.has_role("大会運営")
    async def role_append(self, ctx, role_name: str):
        id_list = g.member_data["user_id"].tolist()
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        await ctx.interaction.response.send_message(
            f"【ロール:{role}】が正常に付与できました。", ephemeral=True
        )
        for id in id_list:
            member = ctx.guild.get_member(int(id))
            await member.add_roles(role)

    # 複数部屋建て通知メンション
    @admin.command(
        name="builds",
        description="部屋建て通知",
    )
    async def builds(self, ctx, matchs: discord.Option(str, choices=gr.match_groups), code):  # type: ignore
        if code != "ノースフライト":
            await ctx.interaction.response.send_message(
                f"コードが違います。", ephemeral=True
            )
            return
        else:
            await ctx.interaction.response.send_message(
                f"正常に送信が完了しました。", ephemeral=True
            )
            # matchesで選んだ値に対応したリストを取得
            groups = gr.match_group_mapping.get(matchs, [])

            for group in groups:
                names = []  # embed用リスト
                values = []  # embed用リスト
                build_members = []  # メンション先のユーザーリスト
                role_lists = ["先鋒", "次鋒", "中堅", "副将", "大将"]  # 役割リスト
                # 役割リストでfor文回してembed作成
                for role_list in role_lists:
                    member_list = g.room_data[
                        g.room_data["room_role"] == str(group) + str(role_list)
                    ]  # y1先鋒, y1次鋒, ･･･ ,y1大将
                    member_ids = [member_list[f'member_id{i}'].to_string(header=False, index=False) for i in range(1, 4)]  # fmt: skip
                    if any(member_id == "" for member_id in member_ids):
                        continue
                    member_names = [member_list[f'member{i}'].to_string(header=False, index=False) for i in range(1, 4)]  # fmt: skip
                    members = [
                        ctx.guild.get_member(int(member_id)) for member_id in member_ids
                    ]
                    # 部屋建てする人だけ別のリストにも格納
                    build_members.append(members[0].mention)
                    # embed用のリストに格納
                    names.append(
                        str(role_list)
                    )  # "先鋒", "次鋒", "中堅", "副将", "大将"
                    values.append(
                        f"{member_names[0]}【{members[0].mention}】☆部屋建て\n"
                        f"{member_names[1]}【{members[1].mention}】\n"
                        f"{member_names[2]}【{members[2].mention}】\n"
                        f"---------------------------------------------------------------------------\n"
                    )
                # チャンネル取得
                channel = discord.utils.get(ctx.guild.text_channels, name=group)
                # 部屋建てユーザーのメンションリスト
                build_members_mention = " ".join(
                    [build_member for build_member in build_members]
                )
                # 対戦表構築
                embed = discord.Embed(title="", description="", color=0xCA3B61)
                for name, value in zip(names, values):
                    embed.add_field(name=name, value=value, inline=False)
                await channel.send(f"{build_members_mention}\n{g.build_message}")
                await channel.send(embed=embed)

    # 強制ログアウト
    @admin.command(
        name="logout",
        description="強制ログアウト",
    )
    @commands.has_role("大会運営")
    async def logout(self, ctx, code):
        if not code == "ログアウト":
            await ctx.interaction.response.send_message(
                f"コードが違います。", ephemeral=True
            )
        else:
            await ctx.interaction.response.send_message(
                f"強制終了しました。", ephemeral=True
            )
            await self.bot.close()


def setup(bot):
    bot.add_cog(admin(bot))
