from future.backports.email.quoprimime import quote

from bot.helper.worker import *
from pyrogram import Client ,filters


@app.on_message(filters.private&filters.incoming&filters.media)
async def hello(client, message :Message):
    msg= await message.reply_text("Added to queue",quote=True,reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="queue", callback_data="q:"+str(message.message_id))]]))
    await add_queue([message.chat.id,message.message_id,msg.message_id])
    print("add queue:",[message.chat.id,message.message_id,msg.message_id])



@app.on_message(filters.command(['pop']))
async def h(client, message:Message):
    pop()
    await message.reply_text("pop done!")

@app.on_message(filters.command(['empty']))
async def h(client, message:Message):
    empty()
    await message.reply_text("empty done!")


@app.on_message(filters.command(['m']))
async def h(client, message: Message):
    await message.reply_text(str(message.reply_to_message.message_id))


@app.on_message(filters.private&filters.incoming)
async def hello(client, message :Message):
    msg=await message.reply_text("Hi",reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="state", callback_data="hi")]]),quote=True)

@app.on_callback_query()
async def _(client,callback:CallbackQuery):
    if callback.data.split(":")[0]=="q":
        print("callback :",[callback.message.chat.id, callback.message.reply_to_message.message_id,callback.message.message_id])
        await callback.answer(text=str(inde([callback.message.chat.id, callback.message.reply_to_message.message_id,callback.message.message_id])))
    else:

     await callback.answer(text=str(await stats(callback.data)),show_alert=True)


app.run()
