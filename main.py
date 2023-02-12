from pyrogram import Client, filters
from pytube import YouTube
import os, info
from datetime import datetime

download_start_time = datetime.now()

def downloadCallback(stream, chunk, bytes_remaining):
        global download_start_time
        seconds_since_download_start = (datetime.now()-        download_start_time).total_seconds()    
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        speed = round(((bytes_downloaded / 1024) / 1024) / seconds_since_download_start, 2)    
        seconds_left = round(((bytes_remaining / 1024) / 1024) / float(speed), 2)
        print(f"\r percentage_of_completion: {round(percentage_of_completion, 2)} % seconds_since_download_start: { round(seconds_since_download_start, 2)} seconds speed: {round(speed, 2)} Mbps seconds_left: {round(seconds_left, 2)} seconds", end=' ')

app = Client("my_bot", api_id=info.api_id, api_hash=info.api_hash, bot_token=info.bot_token)

@app.on_message(filters.private & filters.command('start'))
async def hello(client, msg):
  await client.send_message(msg.chat.id, f'welcome {msg.from_user.username} to bot')


@app.on_message(filters.private & filters.text)
async def sendvideo(client, msg):
    await client.send_message(msg.chat.id,f'جاري التحميل...')
    yt = YouTube(msg.text)
    video = yt.streams.get_highest_resolution()
    yt.register_on_progress_callback(downloadCallback)
    pathv = video.download()
    await app.delete_messages(msg.chat.id, msg.id + 1)
    await client.send_video(msg.chat.id, pathv, f"@P6SBOT, **{round(video.filesize / 1024 / 1024, 1)} MB**")
    os.remove(pathv)

app.run()
