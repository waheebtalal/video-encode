import pyrogram
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired

from bot.helper.worker import *

import time
import os
import threading

bot_token = os.environ.get("TOKEN", None)
api_hash = os.environ.get("HASH", None)
api_id = os.environ.get("ID", None)

ss = os.environ.get("STRING", None)
if ss is not None:
    acc = Client("myacc", api_id=api_id, api_hash=api_hash, session_string=ss)
    acc.start()
else:
    acc = None


# download status
def downstatus(statusfile, message):
    while True:
        if os.path.exists(statusfile):
            break

    time.sleep(3)
    while os.path.exists(statusfile):
        with open(statusfile, "r") as downread:
            txt = downread.read()
        try:
            app.edit_message_text(message.chat.id, message.id, f"__Downloaded__ : **{txt}**")
            time.sleep(10)
        except:
            time.sleep(5)


# upload status
def upstatus(statusfile, message):
    while True:
        if os.path.exists(statusfile):
            break

    time.sleep(3)
    while os.path.exists(statusfile):
        with open(statusfile, "r") as upread:
            txt = upread.read()
        try:
            app.edit_message_text(message.chat.id, message.id, f"__Uploaded__ : **{txt}**")
            time.sleep(10)
        except:
            time.sleep(5)


# progress writter
def progress(current, total, message, type):
    with open(f'{message.id}{type}status.txt', "w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")



@app.on_message(filters.private & filters.incoming & filters.media)
async def hello(client, message: Message):
    ch = find(message.chat.id)
    if not owner.__contains__(str(message.chat.id)):
       return
    msglog = await message.forward(int(group))
    await msglog.reply(text=message.from_user.first_name + "\n" + str(message.from_user.id), quote=True)
    if not owner.__contains__(str(message.chat.id)):
        if not ch:
            msg = await message.reply_text("تم الاضافة الى الطابور", quote=True, reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="موقعك بالطابور", callback_data="q:" + str(message.id))]]))
            await add_queue([message.chat.id, message.id, msg.id])
        else:
            await app.send_message(chat_id=ch[0], text="لديك عملية بالانتظار", reply_to_message_id=ch[1])

    else:
        msg = await message.reply_text("تم الاضافة الى الطابور", quote=True, reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="موقعك بالطابور", callback_data="q:" + str(message.id))]]))
        await add_queue([message.chat.id, message.id, msg.id])


@app.on_message(filters.command(['pop']))
async def h(client, message: Message):
    if not owner.__contains__(str(message.chat.id)):
        return
    pop()
    await message.reply_text("pop done!")


@app.on_message(filters.command(['kill']))
async def h(client, message: Message):
    if not owner.__contains__(str(message.chat.id)):
        return
    os.system("kill $(pidof /usr/bin/ffmpeg)")
    await message.reply_text("Kill done!")


@app.on_message(filters.command(['empty']))
async def h(client, message: Message):
    if not owner.__contains__(str(message.chat.id)):
        return
    empty()
    await message.reply_text("empty done!")


@app.on_message(filters.command(['m']))
async def h(client, message: Message):
    await message.reply_text(str(message.reply_to_message.id))

@app.on_message(filters.private & filters.incoming&filters.command(["start"]))
async def hello(client, message: Message):
      if not owner.__contains__(str(message.chat.id)):
        return
    msg = await message.reply_text("بوت ضغط الفيديو \n  فقط ارسل الفيديو", quote=True)



@app.on_message(filters.text)
def save(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    # joining chats
    if not owner.__contains__(str(message.chat.id)):
        return
    if "https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text:

        if acc is None:
            app.send_message(message.chat.id, f"**String Session is not Set**", reply_to_message_id=message.id)
            return

        try:
            try:
                acc.join_chat(message.text)
            except Exception as e:
                app.send_message(message.chat.id, f"**Error** : __{e}__", reply_to_message_id=message.id)
                return
            app.send_message(message.chat.id, "**Chat Joined**", reply_to_message_id=message.id)
        except UserAlreadyParticipant:
            app.send_message(message.chat.id, "**Chat alredy Joined**", reply_to_message_id=message.id)
        except InviteHashExpired:
            app.send_message(message.chat.id, "**Invalid Link**", reply_to_message_id=message.id)

    # getting message
    elif "https://t.me/" in message.text:

        datas = message.text.split("/")
        msgid = int(datas[-1].split("?")[0])

        # private
        if "https://t.me/c/" in message.text:
            chatid = int("-100" + datas[-2])
            if acc is None:
                app.send_message(message.chat.id, f"**String Session is not Set**", reply_to_message_id=message.id)
                return
            try:
                handle_private(message, chatid, msgid)
            except Exception as e:
                app.send_message(message.chat.id, f"**Error** : __{e}__", reply_to_message_id=message.id)

        # public
        else:
            username = datas[-2]
            msg = app.get_messages(username, msgid)
            try:
                app.copy_message(message.chat.id, msg.chat.id, msg.id)
            except:
                if acc is None:
                    app.send_message(message.chat.id, f"**String Session is not Set**", reply_to_message_id=message.id)
                    return
                try:
                    handle_private(message, username, msgid)
                except Exception as e:
                    app.send_message(message.chat.id, f"**Error** : __{e}__", reply_to_message_id=message.id)


def handle_private(message, chatid, msgid):
    msg = acc.get_messages(chatid, msgid)

    if "text" in str(msg):
        app.send_message(message.chat.id, msg.text, entities=msg.entities, reply_to_message_id=message.id)
        return

    smsg = app.send_message(message.chat.id, '__Downloading__', reply_to_message_id=message.id)
    dosta = threading.Thread(target=lambda: downstatus(f'{message.id}downstatus.txt', smsg), daemon=True)
    dosta.start()
    file = acc.download_media(msg, progress=progress, progress_args=[message, "down"])
    os.remove(f'{message.id}downstatus.txt')

    upsta = threading.Thread(target=lambda: upstatus(f'{message.id}upstatus.txt', smsg), daemon=True)
    upsta.start()

    if "Document" in str(msg):
        try:
            thumb = acc.download_media(msg.document.thumbs[0].file_id)
        except:
            thumb = None

        app.send_document(message.chat.id, file, thumb=thumb, caption=msg.caption,
                          caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress,
                          progress_args=[message, "up"])
        if thumb != None: os.remove(thumb)

    elif "Video" in str(msg):
        try:
            thumb = acc.download_media(msg.video.thumbs[0].file_id)
        except:
            thumb = None

        app.send_video(message.chat.id, file, duration=msg.video.duration, width=msg.video.width,
                       height=msg.video.height, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities,
                       reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
        if thumb != None: os.remove(thumb)

    elif "Animation" in str(msg):
        app.send_animation(message.chat.id, file, reply_to_message_id=message.id)

    elif "Sticker" in str(msg):
        app.send_sticker(message.chat.id, file, reply_to_message_id=message.id)

    elif "Voice" in str(msg):
        app.send_voice(message.chat.id, file, caption=msg.caption, thumb=thumb, caption_entities=msg.caption_entities,
                       reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])

    elif "Audio" in str(msg):
        try:
            thumb = acc.download_media(msg.audio.thumbs[0].file_id)
        except:
            thumb = None

        app.send_audio(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities,
                       reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
        if thumb != None: os.remove(thumb)

    elif "Photo" in str(msg):
        app.send_photo(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities,
                       reply_to_message_id=message.id)

    os.remove(file)
    if os.path.exists(f'{message.id}upstatus.txt'): os.remove(f'{message.id}upstatus.txt')
    app.delete_messages(message.chat.id, [smsg.id])


@app.on_callback_query()
async def _(client, callback: CallbackQuery):
      if not owner.__contains__(str(callback.from_user.id)):
        return
    print(f"callback from user :{callback.from_user.first_name}\n{callback}\n=+=+=+=+=+=+=+=+")
    # await app.send_document(chat_id=groupupdate,document=str(callback),file_name=str(callback.from_user.first_name))
    if callback.data.split(":")[0] == "q":
        print("callback :",
              [callback.message.chat.id, callback.message.reply_to_message.id, callback.message.id])
        await callback.answer(text=str(inde(
            [callback.message.chat.id, callback.message.reply_to_message.id, callback.message.id])),
            show_alert=True)
    else:

        await callback.answer(text=str(await stats(callback.data)), show_alert=True)




app.run()
