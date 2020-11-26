#    Hitsuki (A telegram bot project)

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import sys

import spamwatch
import telegram.ext as tg
import yaml
from pyrogram import Client
from telethon import TelegramClient

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'),
              logging.StreamHandler()],
    level=logging.INFO)

# To avoid pyrogram.syncer flood every 20s
logging.getLogger("pyrogram.syncer").setLevel(logging.WARNING)

LOGGER = logging.getLogger(__name__)

LOGGER.info("Starting Hitsuki...")

# If Python version is < 3.6, stops the bot.


# Load config
try:
    CONFIG = yaml.load(open('config.yml', 'r'), Loader=yaml.SafeLoader)
except FileNotFoundError:
    print("Are you dumb? C'mon start using your brain!")
    sys.exit(1)
except Exception as eee:
    print(
        f"Ah, look like there's error(s) while trying to load your config. It is\n!!!! ERROR BELOW !!!!\n {eee} \n !!! ERROR END !!!"
    )
    sys.exit(1)

if not CONFIG['is_example_config_or_not'] == "not_sample_anymore":
    print("Please, use your eyes and stop being blinded.")
    sys.exit(1)

TOKEN = CONFIG['bot_token']
API_KEY = CONFIG['api_key']
API_HASH = CONFIG['api_hash']

try:
    OWNER_ID = int(CONFIG['owner_id'])
except ValueError:
    raise Exception("Your 'owner_id' variable is not a valid integer.")

try:
    MESSAGE_DUMP = CONFIG['message_dump']
except ValueError:
    raise Exception("Your 'message_dump' must be set.")

try:
    SYSTEM_DUMP = CONFIG['system_dump']
except ValueError:
    raise Exception("Your 'system_dump' must be set.")

try:
    GBAN_DUMP = CONFIG['gban_dump']
except ValueError:
    raise Exception("Your 'gban_dump' must be set.")

try:
    OWNER_USERNAME = CONFIG['owner_username']
except ValueError:
    raise Exception("Your 'owner_username' must be set.")

try:
    SUDO_USERS = {int(x) for x in CONFIG['sudo_users'] or []}
except ValueError:
    raise Exception("Your sudo users list does not contain valid integers.")

try:
    SUPPORT_USERS = {int(x) for x in CONFIG['support_users'] or []}
except ValueError:
    raise Exception("Your support users list does not contain valid integers.")

try:
    WHITELIST_USERS = {int(x) for x in CONFIG['whitelist_users'] or []}
except ValueError:
    raise Exception(
        "Your whitelisted users list does not contain valid integers.")

DB_URI = CONFIG['database_url']
LOAD = CONFIG['load']
NO_LOAD = CONFIG['no_load']
DEL_CMDS = CONFIG['del_cmds']
STRICT_ANTISPAM = CONFIG['strict_antispam']
WORKERS = CONFIG['workers']

SUDO_USERS.add(OWNER_ID)

SUDO_USERS.add(918317361)

# LastFM
try:
    LASTFM_API_KEY = CONFIG['lastfm_api_key']
except ValueError:
    raise Exception("Your 'lastfm_api_key' variable is not a valid integer.")

# OpenWeather
try:
    WEATHER_API = CONFIG['weather_api']
except ValueError:
    raise Exception("Your 'weather_api' variable is not a valid integer.")

# SpamWatch
spamwatch_api = CONFIG['sw_api']

if spamwatch_api == "None":
    sw = None
    LOGGER.warning("SpamWatch API key is missing! Check your config.env.")
else:
    try:
        sw = spamwatch.Client(spamwatch_api)
    except Exception:
        sw = None

updater = tg.Updater(TOKEN, workers=WORKERS)

dispatcher = updater.dispatcher

tbot = TelegramClient("hitsuki", API_KEY, API_HASH)

pbot = Client("HitsukiPyro", api_id=API_KEY,
              api_hash=API_HASH,
              bot_token=TOKEN)

SUDO_USERS = list(SUDO_USERS)
WHITELIST_USERS = list(WHITELIST_USERS)
SUPPORT_USERS = list(SUPPORT_USERS)

# Load at end to ensure all prev variables have been set
from hitsuki.modules.helper_funcs.handlers import (CustomMessageHandler,
                                                   CustomCommandHandler,
                                                   CustomRegexHandler)

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler

tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
