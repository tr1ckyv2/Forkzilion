from telethon import TelegramClient
from userbot import BOT_TOKEN, API_KEY, API_HASH

inlinebot = TelegramClient("inlinebot", API_KEY, API_HASH).start(bot_token=BOT_TOKEN)
