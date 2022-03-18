from bot.helper.worker import *
from pyrogram import Client ,filters





@app.on_message(filters.private&filters.incoming&filters.media)
async def hello(client, message :Message):
    msg= await message.reply_text("Added to queue",quote=True)
    await add_queue([msg,message])


@app.on_message(filters.private&filters.incoming)
async def hello(client, message :Message):
    msg=await message.reply_text("Hi")

app.run()