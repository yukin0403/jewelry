import discord
from discord import Option
from discord.ext import commands
from discord.commands import slash_command
import modules.module as m


# ウマ娘登録確認
class UmaConfirm(commands.Cog):
	def __init__(self, bot):
		super().__init__()
		self.bot = bot

	@slash_command(
		name="uma_confirm",
		description="ウマ娘登録確認",
	)
	async def confirm(self, ctx):
		await ctx.interaction.response.defer(ephemeral=True)
		user_id = str(ctx.author.id)
		# シート[member]読み込み
		self.bot.member_data = m.get_sheet_all_values(self.bot.member_ws)
		# idリストを読み込んでstr型に変換
		id_list = self.bot.member_data["user_id"].tolist()
		id_list_str = [str(i) for i in id_list]
		# idリストの中にコマンド実行者のuser_idがあるか調べる
		if not (user_id in id_list_str):
			await ctx.followup.send(
				"ウマ娘登録が行われておりません。\n"
				"ウマ娘登録後、再度コマンドを実行してください。",
				ephemeral=True,
			)
			return
		else:
			user_info = self.bot.member_data[self.bot.member_data["user_id"] == str(user_id)]
			club_name = user_info["club_name"].to_string(header=False, index=False)
			user_name = user_info["user_name"].to_string(header=False, index=False)
			role = user_info["role"].to_string(header=False, index=False)
			uma_names = [
				user_info[f"uma_name{i}"].to_string(header=False, index=False)
				for i in range(1, 4)
			]
			uma_patterns = [
				user_info[f"uma_pattern{i}"].to_string(header=False, index=False)
				for i in range(1, 4)
			]
			trainer_id = user_info["trainer_id"].to_string(header=False, index=False)
			await ctx.followup.send(
				f"サークル名:{club_name}\n"
				f"登録名:{user_name}\n"
				f"役割:{role}\n"
				f"ウマ娘1:{uma_names[0]} ({uma_patterns[0]})\n"
				f"ウマ娘2:{uma_names[1]} ({uma_patterns[1]})\n"
				f"ウマ娘3:{uma_names[2]} ({uma_patterns[2]})\n"
				f"トレーナーID:{trainer_id}",
				ephemeral=True,
			)


def setup(bot):
	bot.add_cog(UmaConfirm(bot))
