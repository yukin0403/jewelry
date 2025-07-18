import discord
from discord import Option
from discord.ext import commands
from discord.commands import slash_command
import unicodedata
import datetime
from settings.uma_list import uma_list_mapping
from modules import module as m
import asyncio

# モーダルウィンドウ
class MyModal(discord.ui.Modal):
	def __init__(self, bot, uma_list: list, user_list: list, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)
		self.bot = bot
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
		await interaction.response.defer(ephemeral=True)
		await asyncio.sleep(0)
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
		# 確認用メッセージ
		uma_message = (
				f"サークル名:{club_name}\n"
				f"登録名:{user_name}\n"
				f"役割:{role}\n"
				f"ウマ娘1:{un1} ({up1})\n"
				f"ウマ娘2:{un2} ({up2})\n"
				f"ウマ娘3:{un3} ({up3})\n"
				f"トレーナーID:{trainer_id}"
		)
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
		# シート[club]読み込み
		self.bot.club_data = m.get_sheet_all_values(self.bot.club_ws)
		club_name_list = self.bot.club_data["club_name"].tolist()
		# サークル名リストを読み込んで入力したサークル名と一致するか調べる
		if not (club_name in club_name_list):
			await interaction.followup.send(
				"一致するサークル名がありません。\n"
				"登録したサークル名を確認するか、サークル登録を行ってからウマ娘登録を実行してください。",
				ephemeral=True,
			)
			return
		# 役職重複確認
		self.bot.member_data = m.get_sheet_all_values(self.bot.member_ws)
		club_member_list = self.bot.member_data[self.bot.member_data["club_name"] == club_name]
		role_list = club_member_list["role"].tolist()
		if role in role_list:
			register_name = str(
				club_member_list.loc[
					club_member_list["role"] == role, "user_name"
				].values[0]
			)
			register_id = str(
				club_member_list.loc[
					club_member_list["role"] == role, "user_id"
				].values[0]
			)
			if register_id != user_id:
				await interaction.followup.send(
					f"{role}には既に{register_name}さんが登録されています。\n"
					"修正が必要な場合は運営に問い合わせをお願いします。",
					ephemeral=True,
				)
				return
		await interaction.followup.send(uma_message, ephemeral=True)
		# スプシに書き込み
		self.bot.input_member_ws.append_row(new_raw)


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
		役割: str = Option(str, choices=["先鋒", "次鋒", "中堅", "副将", "大将"]),
		ウマ娘id1: str = Option(str, min_length=3, max_length=3),
		ウマ娘脚質1: str = Option(str, choices=["大逃げ", "逃げ", "先行", "差し", "追込"]),
		ウマ娘id2: str = Option(str, min_length=3, max_length=3),
		ウマ娘脚質2: str = Option(str, choices=["大逃げ", "逃げ", "先行", "差し", "追込"]),
		ウマ娘id3: str = Option(str, min_length=3, max_length=3),
		ウマ娘脚質3: str = Option(str, choices=["大逃げ", "逃げ", "先行", "差し", "追込"]),
	):
		# 全角数字を半角数字に変換して、IDに対応したウマ娘の名前を取得
		uma_ids = [
			unicodedata.normalize("NFKC", uma_id)
			for uma_id in [ウマ娘id1, ウマ娘id2, ウマ娘id3]
		]
		uma_names = [uma_list_mapping.get(uma_id) for uma_id in uma_ids]
		uma_patterns = [ウマ娘脚質1, ウマ娘脚質2, ウマ娘脚質3]
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
				uma_patterns[0],
				uma_names[1],
				uma_patterns[1],
				uma_names[2],
				uma_patterns[2],
			]
			user_list = [str(ctx.author.display_name), str(ctx.author.id), 役割]
			modal = MyModal(self.bot, uma_list, user_list, title="ウマ娘登録")
			await ctx.send_modal(modal=modal)


def setup(bot):
	bot.add_cog(uma_register(bot))
