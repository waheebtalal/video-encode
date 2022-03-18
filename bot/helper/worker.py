from _testcapi import awaitType

from bot.helper.ffmpeg_utils import encode
from pyrogram.types import Message
from bot.helper import *

q = []


async def FProgress(current, total, chatid, messageid):
    print(f"{current * 100 / total:.1f}%")
    #  print("\r[%-20s] %d%%" % ('=' * int(current * 10 / total),int(current * 100 / total)), end='')
    await app.edit_message_text(chat_id=chatid, message_id=messageid, text="downloading \n" + (
            "[%-20s] %d%%" % ('=' * (int(current * 20 / total)), (current * 100 / total))))


async def UProgress(current, total, chatid, messageid):
    print(f"{current * 100 / total:.1f}%")
    #  print("\r[%-20s] %d%%" % ('=' * int(current * 10 / total),int(current * 100 / total)), end='')
    await app.edit_message_text(chat_id=chatid, message_id=messageid, text="uploading \n" + (
            "[%-20s] %d%%" % ('=' * (int(current * 20 / total)), (current * 100 / total))))


async def add_queue(msg:[]):
    print("add_queue")
    q.append(msg)
    if len(q) == 1:
        await  enc(msg)


async def enc(ls:[]):
    msg=ls[0]
    file:Message=ls[1]
    print("enc")
    video_file = await file.download(file_name=str(file.chat.id)+"-"+str(file.message_id), progress=FProgress, progress_args=(msg.chat.id, msg.message_id))
    print(video_file)
    await msg.edit(text="Encoding")
    outfile = await encode(video_file)
    await app.send_video(msg.chat.id, outfile, progress=UProgress, progress_args=(msg.chat.id, msg.message_id))
    await msg.edit(text="Done!")
    q.pop(0)
    if len(q) > 0:
        await enc(q[0])
