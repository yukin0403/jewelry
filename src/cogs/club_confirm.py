import discord
from discord import Option
from discord.ext import commands
from discord.commands import slash_command
import modules.module as m

# 確認メッセージ作成
def _get_confirm_message(list):
	members = []
	club_name = list["club_name"].to_string(header=False, index=False)
	user_name = list["user_name"].to_string(header=False, index=False)
	x_id = list["x_id"].to_string(header=False, index=False)
	for i in ["先鋒", "次鋒", "中堅", "副将", "大将"]:
		member = list[i].to_string(header=False, index=False)
		members.append(member)
	message = (
		f"サークル名:{club_name}\n"
		f"代表者登録名:{user_name}\n"
		f"代表者連絡先:{x_id}\n\n"
		f"先鋒:{members[0]}\n"
		f"次鋒:{members[1]}\n"
		f"中堅:{members[2]}\n"
		f"副将:{members[3]}\n"
		f"大将:{members[4]}"
	)
	return message


# サークル登録確認
class ClubConfirm(commands.Cog):
	def __init__(self, bot):
		super().__init__()
		self.bot = bot

	@slash_command(
		name="club_confirm",
		description="サークル登録確認",
	)
	async def confirm(self, ctx):
		await ctx.interaction.response.defer(ephemeral=True)
		user_id = str(ctx.author.id)  # コマンド実行者のuser_id
		# シート[club]読み込み
		self.bot.club_data = m.get_sheet_all_values(self.bot.club_ws)
		club_user_id_list = self.bot.club_data["user_id"].tolist()
		club_user_id_list_str = [
			str(i) for i in club_user_id_list
		]  # user_idリストを読み込んでstr型に変換
		# idリストの中にコマンド実行者のuser_idがあるか調べる
		if not (user_id in club_user_id_list_str):
			self.bot.member_data = m.get_sheet_all_values(
				self.bot.member_ws
			)  # シート[member]読み込み
			member_user_id_list = self.bot.member_data["user_id"].tolist()
			member_user_id_list_str = [
				str(i) for i in member_user_id_list
			]  # member_idリストを読み込んでstr型に変換
			# idリストの中にコマンド実行者のuser_idがあるか調べる
			if not (user_id in member_user_id_list_str):
				await ctx.followup.send(
					"サークル未登録、またはサークル登録をした代表者ではない、またはウマ娘登録が行われておりません。\n"
					"サークル登録を行うか、代表者がコマンドを実行するか、ウマ娘登録を行ってからコマンドを実行してください。",
					ephemeral=True,
				)
				return
			else:
				user_info = self.bot.member_data[self.bot.member_data["user_id"] == user_id]
				user_club = user_info["club_name"].to_string(header=False, index=False)
				confirm_list = self.bot.club_data[self.bot.club_data["club_name"] == user_club]
				confirm_message = _get_confirm_message(confirm_list)
				await ctx.followup.send(
					confirm_message, ephemeral=True
				)
				return
		else:
			confirm_list = self.bot.club_data[self.bot.club_data["user_id"] == user_id]
			confirm_message = _get_confirm_message(confirm_list)
			await ctx.followup.send(confirm_message, ephemeral=True)
			return


def setup(bot):
	bot.add_cog(ClubConfirm(bot))
