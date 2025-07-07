import discord
from discord.ext import commands
from settings.bot_settings import GC, SPREADSHEET_URL, BOT_INFO, IDS
import asyncio
import re

bot = commands.Bot(intents=BOT_INFO.INTENTS)
bot.global_lock = asyncio.Lock()

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
    guild = bot.get_guild(BOT_INFO.GUILD_ID)
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
    bot.remind_role = guild.get_role(IDS.REMIND_ROLE)
    # チャンネル読み込み
    bot.result_ch = bot.get_channel(IDS.RESULT_CH)
    bot.repeat_result_ch = bot.get_channel(IDS.REPEAT_RESULT_CH)
    bot.register_ch = bot.get_channel(IDS.REGISTER_CH)
    bot.remind_ch = bot.get_channel(IDS.REMIND_CH)

bot.run(BOT_INFO.TOKEN)
