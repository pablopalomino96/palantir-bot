import glob, os, psutil, sys, subprocess
from telegram.ext import Updater, CommandHandler
import logging
import datetime

print("---***---")
print("Starting Palantir bot...")
print("---***---")
print("daemonising...")

if os.fork(): exit(0)
os.umask(0)
os.setsid()
if os.fork(): exit(0)

sys.stdout.flush()
sys.stderr.flush()
si = file('/dev/null', 'r')
so = file('/tmp/palantir-output.txt', 'a+')
se = file('/tmp/palantir-errors.txt', 'a+', 0)
os.dup2(si.fileno(), sys.stdin.fileno())
os.dup2(so.fileno(), sys.stdout.fileno())
os.dup2(se.fileno(), sys.stderr.fileno())

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

chat_id = os.environ['TELEGRAM_ID']
bot_token = os.environ['PALANTIR_TOKEN']
updater = Updater(token=bot_token)
dispatcher = updater.dispatcher

bot_path = os.environ['HOME'] + '/palantir-bot'
pics_path =  bot_path + "/pics"

def take_snap(bot, update):
  if not owner(update):
    send_not_authorized_message(bot, update)
    return

  bot.send_message(chat_id, text="Taking a look, please wait...")
  filename = '01-' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
  res = subprocess.Popen(["raspistill", "-v", "-o", filename], shell=False, stdout=subprocess.PIPE, cwd=pics_path);
  res.wait()
  bot.send_photo(chat_id, photo=open(pics_path + "/" + filename, "rb"))

def clear_photos(bot, update):
  if not owner(update):
    send_not_authorized_message(bot, update)
    return

  os.chdir(pics_path)
  files=glob.glob('*.jpg')
  if not files:
    bot.send_message(chat_id, text="There isn't any photo")
    return

  for filename in files:
    os.remove(filename)
  bot.send_message(chat_id, text="All pictures deleted!")

def clear_videos(bot, update):
  if not owner(update):
    send_not_authorized_message(bot, update)
    return

  os.chdir(pics_path)
  files=glob.glob('*.avi')
  if not files:
    bot.send_message(chat_id, text="There isn't any video")
    return

  for filename in files:
    os.remove(filename)
  bot.send_message(chat_id, text="All videos deleted!")

def start(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="I'm the Palantir. You can see everything, but... look out! We won't know who might be watching")
  print(update.message.chat_id)

def start_motion(bot, update):
  if not owner(update):
    send_not_authorized_message(bot, update)
    return

  res = subprocess.Popen(["motion", "-c " + bot_path + "/motion.conf"], shell=False, stdout=subprocess.PIPE, cwd=bot_path)
  bot.send_message(chat_id, text='"The inside of the ball has gone up in flames". Motion detection enabled')

def stop_motion(bot, update):
  if not owner(update):
    send_not_authorized_message(bot, update)
    return

  PROCNAME = "motion"

  for proc in psutil.process_iter():
    if proc.name() == PROCNAME:
      proc.kill()

  bot.send_message(chat_id, text='"Gandalf cast his cloak over the Palantir". Motion detection disabled')

def check_motion(bot, update):
  if not owner(update):
    send_not_authorized_message(bot, update)
    return

  ps = subprocess.check_output(('ps'))
  if (ps.find("motion")) == -1:
    bot.send_message(chat_id, text='"The inside of the ball is dark". Motion detection is disabled')
  else:
    bot.send_message(chat_id, text='"The inside of the ball is in flames". Motion detection is enabled')

def send_last_photo(bot, update):
  if not owner(update):
    send_not_authorized_message(bot, update)
    return

  list_of_photos = glob.glob(pics_path + '/*.jpg')

  if not list_of_photos:
    bot.send_message(chat_id, text="I haven't captured any photo so far")
    return

  latest_photo = max(list_of_photos, key=os.path.getctime)
  file_handler = open(latest_photo, 'rb')

  bot.send_message(chat_id, text=("Lastest photo, captured at " + extract_date(latest_photo, '.jpg')))
  bot.send_photo(chat_id, photo=file_handler)

def send_last_video(bot, update):
  if not owner(update):
    send_not_authorized_message(bot, update)
    return

  list_of_videos = glob.glob(pics_path + '/*.avi')

  if not list_of_videos:
    bot.send_message(chat_id, text="I haven't captured any video so far")
    return

  latest_video = max(list_of_videos, key=os.path.getctime)
  file_handler = open(latest_video, 'rb')

  bot.send_message(chat_id, text=("Lastest video, captured at " + extract_date(latest_video, '.avi')))
  bot.send_video(chat_id, video=file_handler)

def owner(update):
  if update.message.chat_id == int(chat_id):
    return True
  else:
    return False

def extract_date(filename, extension):
  time_at = filename.replace(pics_path + '/', '').replace(extension, '').split('-')[1]
  date = time_at[6:8] + '-' + time_at[4:6] + '-' + time_at[:4]
  time = time_at[8:10] + ':' + time_at[10:12] + ':' + time_at[12:14]
  return  time + ', ' + date

def send_not_authorized_message(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="You are not the bot owner. Go the way you came :)")

# --- HANDLERS ---
send_last_photo_handler = CommandHandler('lastphoto', send_last_photo)
dispatcher.add_handler(send_last_photo_handler)

send_last_video_handler = CommandHandler('lastvideo', send_last_video)
dispatcher.add_handler(send_last_video_handler)

take_snap_handler = CommandHandler('snap', take_snap)
dispatcher.add_handler(take_snap_handler)

clean_photos_handler = CommandHandler('clearphotos', clear_photos)
dispatcher.add_handler(clean_photos_handler)

clean_videos_handler = CommandHandler('clearvideos', clear_videos)
dispatcher.add_handler(clean_videos_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

start_motion_handler = CommandHandler('see', start_motion)
dispatcher.add_handler(start_motion_handler)

stop_motion_handler = CommandHandler('stop', stop_motion)
dispatcher.add_handler(stop_motion_handler)

check_motion_handler = CommandHandler('check', check_motion)
dispatcher.add_handler(check_motion_handler)

if __name__ == '__main__':
  updater.start_polling()
  updater.idle()
