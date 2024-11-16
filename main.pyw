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
import os
from dotenv import load_dotenv
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import re

load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD_ID = os.getenv('GUILD_ID')
SPREADSHEET_URL = os.getenv('SPREADSHEET_URL')
REMIND_CH_ID = int(os.getenv('REMIND_CH_ID'))
RESULT_CH_ID = int(os.getenv('RESULT_CH_ID'))
REGISTER_CH_ID = int(os.getenv('REGISTER_CH_ID'))

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('discord-bot-421209-2883c9978631.json', scope)
gc = gspread.authorize(credentials)

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(intents=intents)
guild = bot.get_guild(GUILD_ID) #type: ignore

cogs_list = [
    'admin',
    'result',
    'club_register',
    'club_confirm',
    'uma_register',
    'uma_confirm',
    'reminder',
]
for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')

@bot.event
async def on_ready():
    print(f"{bot.user}はここだよ～")
    await bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name='ファッションリーダー'))

    # スプシのURLからKEY取得
    match = re.search(r'/d/([^/]+)/', SPREADSHEET_URL)
    if match:
        spreadsheet_key = match.group(1)
        sh = gc.open_by_key(spreadsheet_key)
    else:
        print("IDが見つかりませんでした。")
        return

    # シート取得
    g.result_ws = sh.worksheet('result')
    g.room_ws = sh.worksheet("room")
    g.member_ws = sh.worksheet("member")
    g.club_ws = sh.worksheet("club")
    g.input_member_ws = sh.worksheet("input_member")
    g.input_club_ws = sh.worksheet("input_club")

    # 結果出力先チャンネル読み込み
    g.result_ch = bot.get_channel(RESULT_CH_ID)
    # 登録用チャンネル読み込み
    g.register_ch = bot.get_channel(REGISTER_CH_ID)
    # リマインド用チャンネル読み込み
    g.remind_ch = bot.get_channel(REMIND_CH_ID)

bot.run(TOKEN)