from pyrogram import Client, filters

from decouple import config

api = 000
hash = "abcdefghijklmn"
bot = ""
owner=888888
try:
    api = config("api", cast=int)
    hash = config("hash")
    bot = config("bot")
    owner=config("owner")
except:
    print("error config")
app = Client("bot", api_id=api, api_hash=hash, bot_token=bot)
download_dir = "download"
codec_dir = "codec"
