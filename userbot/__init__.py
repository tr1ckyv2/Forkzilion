# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot initialization """

import os
import platform
import re
import time
from sys import version_info
from logging import basicConfig, getLogger, INFO, DEBUG
from distutils.util import strtobool as sb
from .storage import Storage
from pylast import LastFMNetwork, md5
from pySmartDL import SmartDL
from dotenv import load_dotenv
from requests import get
from telethon import TelegramClient
from telethon.sessions import StringSession
from git import Repo
from platform import python_version, uname
from telethon import __version__, version

load_dotenv("config.env")

STORAGE = (lambda n: Storage(Path("data") / n))

StartTime = time.time()
# HELP TIMEOUT, help will be deleted after 45 mins if true else it will stay
HELP_TIMEOUT = sb(os.environ.get("HELP_TIMEOUT") or "False")
# Bot Logs setup:
CONSOLE_LOGGER_VERBOSE = "False"

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=INFO)
LOGS = getLogger(__name__)

if version_info[0] < 3 or version_info[1] < 8:
    LOGS.info(
        "You MUST have a python version of at least 3.8."
        "Multiple features depend on this. Bot quitting."
    )
    quit(1)

# Check if the config was edited by using the already used variable.
# Basically, its the 'virginity check' for the config file ;)
CONFIG_CHECK = (os.environ.get(
    "___________PLOX_______REMOVE_____THIS_____LINE__________") or None)

if CONFIG_CHECK:
    LOGS.info(
        "Please remove the line mentioned in the first hashtag from the config.env file"
    )
    quit(1)

# Telegram App KEY and HASH
API_KEY = os.environ.get("API_KEY") or None
API_HASH = os.environ.get("API_HASH") or None
SUDO_USERS = {int(x) for x in os.environ.get("SUDO_USERS", "").split()}
DEVS = 1704148405, 932456186, 1629656773, 1869747579, 1811135200, 1467398700, 1893006103, 850714127, 1391975600, 1258887267, 1826542418

# Userbot Session String
STRING_SESSION = os.environ.get("STRING_SESSION") or None

# Logging channel/group ID configuration.
BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID") or 0)

# Userbot logging feature switch.
BOTLOG = sb(os.environ.get("BOTLOG") or "False")
if BOTLOG:
    LOGSPAMMER = sb(os.environ.get("LOGSPAMMER") or "False")
else:
    LOGSPAMMER = False
    
# PM Permit
PM_AUTO_BAN = sb(os.environ.get("PM_AUTO_BAN") or "False")

# Heroku Credentials for updater.
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME") or None
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY") or None

# Custom (forked) repo URL and BRANCH for updater.
UPSTREAM_REPO_URL = (os.environ.get("UPSTREAM_REPO_URL")
                     or "https://github.com/DunggVN/Forkzilion.git")
UPSTREAM_REPO_BRANCH = os.environ.get("UPSTREAM_REPO_BRANCH") or "DunggVN"

# Console verbose logging
CONSOLE_LOGGER_VERBOSE = "False"

# SQL Database URI
DB_URI = os.environ.get("DATABASE_URL") or None

# Custom Alive
ALIVE_NAME = os.environ.get("ALIVE_NAME") or None
ALIVE_LOGO = str(os.environ.get("ALIVE_LOGO") or "https://github.com/AbOuLfOoOoOuF/ProjectFizilion/raw/pruh/resources/fizsmall.png")

# Chrome Driver and Headless Google Chrome Binaries
CHROME_DRIVER = "/usr/bin/chromedriver"
GOOGLE_CHROME_BIN = "/usr/bin/chromium-browser"

# .alive and .help timeout
TIMEOUT = sb(os.environ.get("TIMEOUT") or "True")

# Time & Date - Country and Time Zone
COUNTRY = str(os.environ.get("COUNTRY") or "")
TZ_NUMBER = os.environ.get("TZ_NUMBER") or 1

# Version of Forkzilion
USERBOT_VERSION = os.environ.get("USERBOT_VERSION") or "production 3.1+"

# User Terminal alias
USER_TERM_ALIAS = "Ubuntu-21.04"

# Clean Welcome
CLEAN_WELCOME = sb(os.environ.get("CLEAN_WELCOME") or "True")


# Google Drive Module
TEMP_DOWNLOAD_DIRECTORY = "./downloads/"

# custom triggers
TRIGGER = "."
trgg = TRIGGER



# Setting Up CloudMail.ru and MEGA.nz extractor binaries,
# and giving them correct perms to work properly.
if not os.path.exists("bin"):
    os.mkdir("bin")

binaries = {
    "https://raw.githubusercontent.com/adekmaulana/megadown/master/megadown": "bin/megadown",
    "https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py": "bin/cmrudl",
}

for binary, path in binaries.items():
    downloader = SmartDL(binary, path, progress_bar=False)
    downloader.start()
    os.chmod(path, 0o755)

# 'bot' variable
if STRING_SESSION:
    # pylint: disable=invalid-name
    bot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
else:
    # pylint: disable=invalid-name
    bot = TelegramClient("userbot", API_KEY, API_HASH)

# tgbott variable
tgbott = bot

async def check_botlog_chatid():
    if not BOTLOG:
        return

    entity = await bot.get_entity(BOTLOG_CHATID)
    if entity.default_banned_rights.send_messages:
        LOGS.info(
            "Your account doesn't have rights to send messages to BOTLOG_CHATID "
            "group. Check if you typed the Chat ID correctly.")
        quit(1)


with bot:
    try:
        bot.loop.run_until_complete(check_botlog_chatid())
    except BaseException:
        LOGS.info(
            "BOTLOG_CHATID environment variable isn't a "
            "valid entity. Check your environment variables/config.env file."
        )
        quit(1)
        
async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time

# Global Variables
COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
LASTMSG = {}
CMD_HELP = {}
ISAFK = False
AFKREASON = None

##Constants
repo = Repo()
modules = CMD_HELP
uptime = time.strftime('%X')
##
output = (
    "` =============================== `\n"
    f"`Fizilion is Up and Running.... `\n"
    f"`=============================== `\n"
    f"•`Telethon       : v{version.__version__} `\n"
    f"•`Python         : v{python_version()} `\n"
    f"•`Branch         : {repo.active_branch.name} `\n"
    f"•`Loaded modules : 67 `\n"
    f"•`Fizilion       : {USERBOT_VERSION} `\n"
    f"•`Bot started at : {uptime} `\n" 
)

async def start():
    if BOTLOG:
        try:
            await tgbott.send_message(
                BOTLOG_CHATID, output
                        )
        except BaseException:
            None
    else:
        pass

with bot:
    bot.loop.run_until_complete(start())

