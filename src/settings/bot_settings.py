import discord
import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '.env'))
json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "discord-bot-421209-29d380fbb0a5.json")

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
credentials = ServiceAccountCredentials.from_json_keyfile_name(
	json_path, scope
)
GC = gspread.authorize(credentials)

intents = discord.Intents.default()
intents.members = True
BOT_INTENTS = intents

TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

SPREADSHEET_URL = os.getenv("SPREADSHEET_URL")

ADMIN_IDS = os.getenv("ADMIN_IDS").split(",")

RESULT_CH_ID = int(os.getenv("RESULT_CH_ID"))
REPEAT_RESULT_CH_ID = int(os.getenv("REPEAT_RESULT_CH_ID"))
REGISTER_CH_ID = int(os.getenv("REGISTER_CH_ID"))
REMIND_CH_ID = int(os.getenv("REMIND_CH_ID"))
REMIND_ROLE_ID = int(os.getenv("REMIND_ROLE_ID"))