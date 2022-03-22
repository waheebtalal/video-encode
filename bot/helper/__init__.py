from pyrogram import Client, filters

from decouple import config

api = 19663899
hash = "af0b19d19293e57b1b74cabcf6dcbbd6"
bot = "5029205621:AAHW2SeeJkQyO-zU3s1yRkUV3nSAdLAjwAk"
owner=40679394
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
