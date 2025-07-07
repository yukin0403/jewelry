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
SPREADSHEET_URL = os.getenv("SPREADSHEET_URL")

class BOT_INFO:
	INTENTS = discord.Intents.default()
	INTENTS.members = True

	TOKEN = os.getenv("TOKEN")
	GUILD_ID = int(os.getenv("GUILD_ID"))


class IDS:
	ADMIN = os.getenv("ADMIN_IDS").split(",")

	RESULT_CH = int(os.getenv("RESULT_CH_ID"))
	REPEAT_RESULT_CH = int(os.getenv("REPEAT_RESULT_CH_ID"))
	REGISTER_CH = int(os.getenv("REGISTER_CH_ID"))
	REMIND_CH = int(os.getenv("REMIND_CH_ID"))
	REMIND_ROLE = int(os.getenv("REMIND_ROLE_ID"))
