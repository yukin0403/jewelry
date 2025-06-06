import discord
from discord.ext import commands
from settings.bot_settings import GC, BOT_INTENTS, TOKEN, GUILD_ID, SPREADSHEET_URL, REMIND_CH_ID, RESULT_CH_ID, REPEAT_RESULT_CH_ID, REGISTER_CH_ID, REMIND_ROLE_ID
import re

bot = commands.Bot(intents=BOT_INTENTS)

cogs_list = [
    "admin",
    "result",
    "club_register",
    "club_confirm",
    "uma_register",
    "uma_confirm",
    "reminder",
]
for cog in cogs_list:
    bot.load_extension(f"cogs.{cog}")


@bot.event
async def on_ready():
    print(f"{bot.user}はここだよ～")
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.CustomActivity(name="ファッションリーダー"),
    )
    guild = bot.get_guild(GUILD_ID)
    # スプシのURLからKEY取得
    match = re.search(r"/d/([^/]+)/", SPREADSHEET_URL)
    if match:
        spreadsheet_key = match.group(1)
    else:
        print("IDが見つかりませんでした。")
        return
    sh = GC.open_by_key(spreadsheet_key)

    # シート取得
    bot.result_ws = sh.worksheet("result")
    bot.room_ws = sh.worksheet("room")
    bot.member_ws = sh.worksheet("member")
    bot.club_ws = sh.worksheet("club")
    bot.input_member_ws = sh.worksheet("input_member")
    bot.input_club_ws = sh.worksheet("input_club")
    # ロール取得
    bot.remind_role = guild.get_role(REMIND_ROLE_ID)
    # チャンネル読み込み
    bot.result_ch = bot.get_channel(RESULT_CH_ID)
    bot.repeat_result_ch = bot.get_channel(REPEAT_RESULT_CH_ID)
    bot.register_ch = bot.get_channel(REGISTER_CH_ID)
    bot.remind_ch = bot.get_channel(REMIND_CH_ID)


bot.run(TOKEN)
