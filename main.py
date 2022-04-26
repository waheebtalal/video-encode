from future.backports.email.quoprimime import quote

from bot.helper.worker import *
from pyrogram import Client, filters


@app.on_message(filters.private & filters.incoming & filters.media)
async def hello(client, message: Message):
    ch = find(message.chat.id)
    if block.__contains__(str(message.chat.id)):
        return
    msglog = await message.forward(int(group))
    await msglog.reply(text=message.from_user.first_name + "\n" + str(message.from_user.id), quote=True)
    if owner.__contains__(str(message.chat.id)):
        if not ch:
            msg = await message.reply_text("تم الاضافة الى الطابور", quote=True, reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="موقعك بالطابور", callback_data="q:" + str(message.message_id))]]))
            await add_queue([message.chat.id, message.message_id, msg.message_id])
        else:
            await app.send_message(chat_id=ch[0], text="لديك عملية بالانتظار", reply_to_message_id=ch[1])

    else:
        msg = await message.reply_text("تم الاضافة الى الطابور", quote=True, reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="موقعك بالطابور", callback_data="q:" + str(message.message_id))]]))
        await add_queue([message.chat.id, message.message_id, msg.message_id])


@app.on_message(filters.command(['pop']))
async def h(client, message: Message):
    pop()
    await message.reply_text("pop done!")


@app.on_message(filters.command(['empty']))
async def h(client, message: Message):
    empty()
    await message.reply_text("empty done!")


@app.on_message(filters.command(['m']))
async def h(client, message: Message):
    await message.reply_text(str(message.reply_to_message.message_id))


@app.on_message(filters.private & filters.incoming)
async def hello(client, message: Message):
    msg = await message.reply_text("بوت ضغط الفيديو \n  فقط ارسل الفيديو", quote=True)


@app.on_callback_query()
async def _(client, callback: CallbackQuery):
    print(f"callback from user :{callback.from_user.first_name}\n{callback}\n=+=+=+=+=+=+=+=+")
    # await app.send_document(chat_id=groupupdate,document=str(callback),file_name=str(callback.from_user.first_name))
    if callback.data.split(":")[0] == "q":
        print("callback :",
              [callback.message.chat.id, callback.message.reply_to_message.message_id, callback.message.message_id])
        await callback.answer(text=str(inde(
            [callback.message.chat.id, callback.message.reply_to_message.message_id, callback.message.message_id])),
            show_alert=True)
    else:

        await callback.answer(text=str(await stats(callback.data)), show_alert=True)


app.run()
