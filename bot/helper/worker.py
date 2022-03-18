from _testcapi import awaitType

from bot.helper.ffmpeg_utils import *
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
    ttl=get_duration(video_file)
    print("ttl  :"+str(ttl))
    width_high=get_width_height(video_file)
    print("width_high :"+str(width_high))
    thumb=get_thumbnail(video_file,"thumbs//"+str(file.chat.id),1)
    print("thumb :"+str(thumb))
    outfile = await encode(video_file,file.chat.id)
    print("outfile :"+str(outfile))
    await app.send_video(msg.chat.id, outfile,
                         progress=UProgress,
                         progress_args=(msg.chat.id, msg.message_id)
                         ,duration=ttl
                         ,width=width_high[0]
                         ,height=width_high[1]
                         ,thumb=thumb
                         ,supports_streaming=True
                         )
    await msg.edit(text="Done!")
    os.remove(video_file)
    os.remove(outfile)
    os.remove(thumb)
    q.pop(0)
    if len(q) > 0:
        await enc(q[0])
