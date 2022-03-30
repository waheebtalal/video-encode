from pyrogram import Client, filters

from decouple import config

api = 000
hash = "abcdefghijklmn"
bot = ""
owner=888888
group=""
try:
    api = config("api", cast=int)
    hash = config("hash")
    bot = config("bot")
    owner=str(config("owner"))
    group = config("group")
except:
    print("error config")
app = Client("bot", api_id=api, api_hash=hash, bot_token=bot)
download_dir = "download"
codec_dir = "codec"
