from _testcapi import awaitType
from pathlib import Path

from bot.helper.ffmpeg_utils import *
from pyrogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from bot.helper import *
import asyncio
from pyrogram.errors import FloodWait
from bot.helper.fast import FastDownload
from os import path

q = []


async def FProgress(current, total, msg: Message):
    print(f"{current * 100 / total:.1f}%")
    #  print("\r[%-20s] %d%%" % ('=' * int(current * 10 / total),int(current * 100 / total)), end='')
    proc = "downloading \n" + (
            "[%-20s] %.1f%%" % ('=' * (int(current * 20 / total)), (current * 100 / total)))
    if msg.text != proc:
        try:
            await msg.edit(text="downloading \n" + (
                    "[%-20s] %.1f%%" % ('=' * (int(current * 20 / total)), (current * 100 / total))))
        except FloodWait as e:
            print("error download progress")
            await asyncio.sleep(e.x)


async def stats(out):
    try:
        ot = os.path.getsize(out)
        oos = ot / (1024 * 1024)
        ans = "جاري الضغط:" + " \n " + str(oos)
        return ans
    except:
        return "خطأ !!"


async def UProgress(current: int, total, msg: Message):
    print(f"{current * 100 / total:.1f}%")
    #  print("\r[%-20s] %d%%" % ('=' * int(current * 10 / total),int(current * 100 / total)), end='')
    progress = "uploading \n" + (
            "[%-20s] %.1f%%" % ('=' * (int(current * 20 / total)), (current * 100 / total)))
    if msg.text != progress:
        try:
            await msg.edit(text="uploading \n" + (
                    "[%-20s] %.1f%%" % ('=' * (int(current * 20 / total)), (current * 100 / total))))
        except FloodWait as e:
            print("error upload progress")
            await asyncio.sleep(e.x)


async def add_queue(msg: []):
    print("add_queue")
    q.append(msg)
    if len(q) == 1:
        await  enc(msg)


async def enc(ls: []):
    msg: Message = ls[0]
    file: Message = ls[1]
    try:
        print("enc")
        video_file = ""
        video_file = await file.download(file_name=str(file.chat.id) + "-" + str(file.message_id), progress=FProgress,
                                         progress_args=(msg))
        print(video_file)
        ttl = get_duration(video_file)
        print("ttl  :" + str(ttl))
        width_high = get_width_height(video_file)
        print("width_high :" + str(width_high))
        thumb = get_thumbnail(video_file, "thumbs//" + str(file.chat.id), 1)
        print("thumb :" + str(thumb))

        enpa = "encode//" + str(file.chat.id)
        os.makedirs(enpa, exist_ok=True)
        basefilepath, extension = os.path.splitext(video_file)
        print("basefilepath : " + basefilepath + " | extension : " + extension)
        output_filepath = basefilepath + '.HEVC' + '.mp4'
        output_filepath = str(output_filepath).replace("downloads", enpa)

        try:
            await msg.edit(text="Encoding", reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="state", callback_data=output_filepath)]]))
        except FloodWait as e:
            await asyncio.sleep(e.x)
            try:
                await msg.reply_text(text="Encoding", reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="state", callback_data=output_filepath)]]))
            except FloodWait as e:
                await asyncio.sleep(e.x)
                print("error reply encoding")
            print("error edit encoding")
        outfile = await encode(video_file, output_filepath)
        try:
            await app.send_video(msg.chat.id, outfile,
                                 progress=UProgress,
                                 progress_args=(msg)
                                 , duration=ttl
                                 , width=width_high[0]
                                 , height=width_high[1]
                                 , thumb=thumb
                                 , supports_streaming=True
                                 )
        except FloodWait as e:
            print("send error")
            await asyncio.sleep(e.x)

        try:
            await msg.edit(text="Done!")
        except FloodWait as e:
            await asyncio.sleep(e.x)
            try:
                await msg.reply_text(text="Done!")
            except FloodWait as e:
                await asyncio.sleep(e.x)
                print("error reply done")
            print("error edit done")
        os.remove(video_file)
        os.remove(outfile)
        os.remove(thumb)
    except:
        print("except")
        await file.reply_text("Error")

    pop()
    if len(q) > 0:
        await enc(q[0])


def pop():
    if len(q) != 0:
        q.pop(0)


def empty():
    q = []
