from pyrogram import Client ,filters
 
from decouple import config
api=19663899
hash="af0b19d19293e57b1b74cabcf6dcbbd6"
bot="5272600822:AAEPxO-u2yva7aXhz-ZdTup_DZrkwOZiVAE"
try:
 api=config("api", cast=int)
 hash=config("hash")
 bot=config("bot")   
except:
  print("error config")
app=Client("bot",api_id=api,api_hash=hash,bot_token=bot)
download_dir="download"
codec_dir="codec"
