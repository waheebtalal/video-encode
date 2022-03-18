from pyrogram import Client ,filters
from pyrogram.types import Message
from bot.helper import *
from bot.helper.worker import *
from tqdm import tqdm




@app.on_message(filters.private&filters.incoming&filters.media)
async def hello(client, message :Message):
    msg= await message.reply_text("Added to queue",quote=True)
    await add_queue([msg,message])


@app.on_message(filters.private&filters.incoming)
async def hello(client, message :Message):
    msg=await message.reply_text("Hi")

app.run()