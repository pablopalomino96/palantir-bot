import requests, glob, os
import sys

url = 'https://api.telegram.org/bot' + os.environ['PALANTIR_TOKEN'] + '/'

r1 = requests.post(url+'sendMessage', data={"chat_id": os.environ['TELEGRAM_ID'], "text": "Motion detected! Taking photos and recording a video... Type /lastphoto or /lastvideo if you want to see it."})
