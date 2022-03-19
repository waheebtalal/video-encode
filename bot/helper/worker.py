from _testcapi import awaitType

from bot.helper.ffmpeg_utils import *
from pyrogram.types import Message
from bot.helper import *
from bot.helper.fast import FastDownload

q = []


async def FProgress(current, total, chatid, messageid):
    print(f"{current * 100 / total:.1f}%")
    #  print("\r[%-20s] %d%%" % ('=' * int(current * 10 / total),int(current * 100 / total)), end='')
    try:
        await app.edit_message_text(chat_id=chatid, message_id=messageid, text="downloading \n" + (
            "[%-20s] %d%%" % ('=' * (int(current * 20 / total)), (current * 100 / total))))
    except:
        print("error download progress")


async def UProgress(current, total, chatid, messageid):
    print(f"{current * 100 / total:.1f}%")
    #  print("\r[%-20s] %d%%" % ('=' * int(current * 10 / total),int(current * 100 / total)), end='')
    try:
        await app.edit_message_text(chat_id=chatid, message_id=messageid, text="uploading \n" + (
            "[%-20s] %d%%" % ('=' * (int(current * 20 / total)), (current * 100 / total))))
    except:
        print("error upload progress")


async def add_queue(msg:[]):
    print("add_queue")
    q.append(msg)
    if len(q) == 1:
        await  enc(msg)


async def enc(ls:[]):
    msg=ls[0]
    file:Message=ls[1]
    try:
        print("enc")
        video_file=""
        video_file = await file.download(file_name=str(file.chat.id)+"-"+str(file.message_id), progress=FProgress, progress_args=(msg.chat.id, msg.message_id))
        print(video_file)
        try:
            await msg.edit(text="Encoding")
        except:
            try:
                await msg.reply_text(text="Encoding")
            except:
                print("error reply encoding")
            print("error edit encoding")
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
        try:
            await msg.edit(text="Done!")
        except:
            try:
                await msg.reply_text(text="Done!")
            except:
                print("error reply done")
            print("error edit done")
        os.remove(video_file)
        os.remove(outfile)
        os.remove(thumb)
    except:
        print("except")
        await file.reply_text("Error")



    q.pop(0)
    if len(q) > 0:
        await enc(q[0])

def pop():
    q.pop(0)

def empty():
    q=[]
