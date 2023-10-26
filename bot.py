from telegram.ext import Updater, CommandHandler
from time import sleep
import subprocess
import os


TOKEN = 'TELEGRAM_TOKEN'


def take_photo(update, context):
    subprocess.run(['libcamera-still', '-q', '75', '-o', 'image.jpg'])
    with open('image.jpg', 'rb') as photo:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)


def take_video(update, context):
    duration = int(context.args[0]) * 1000
    video_file_h264 = 'video.h264'
    video_file_mp4 = 'video.mp4'
    subprocess.run(
        ['libcamera-vid', '-t', str(duration), '-o', video_file_h264])
    # telegram ei tue h264 prkl (apt install ffmpeg)
    subprocess.run(['ffmpeg', '-y', '-framerate', '25', '-i',
                   video_file_h264, '-c:v', 'copy', video_file_mp4])
    with open(video_file_mp4, 'rb') as video:
        context.bot.send_video(chat_id=update.effective_chat.id, video=video)
        os.remove(video_file_mp4)
        os.remove(video_file_h264)


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('photo', take_photo))
    dp.add_handler(CommandHandler('video', take_video, pass_args=True))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()